# /standup — Kanban Daily Standup Briefing

**Author:** Sagar Gupta · Senior Agile Business Analyst · 7EDGE  
**Command:** `/PM/standup [board-name]`  
**Category:** Project Management  
**Integrations:** Atlassian Jira (via MCP)

---

## Overview

This command generates a pre-meeting standup briefing for any Jira Kanban board. Run it before your daily kanban call to know the exact status of every active card — who it's pending on, what's aging, what's blocked, and what needs to be discussed in the room.

It pulls live data from Jira via the Atlassian MCP and produces a structured report covering cards in all active statuses (Ready → Done), with comment analysis, aging flags, blocker detection, and a facilitator summary ready to use as meeting notes.

---

## Usage

```
/PM/standup [board-name]
```

**Examples:**
- `/PM/standup CC` — Briefing for the Continuous Crusaders board
- `/PM/standup PHOENIX` — Briefing for the Phoenix project board
- `/PM/standup MQR` — Briefing for the Maison QR board

The board name should match the Jira project key as it appears in your Atlassian workspace.

---

## What It Does

### Step 1 — Connect to Jira

Use the Atlassian MCP to authenticate and resolve the board name to its project key and cloud ID. If the board name cannot be resolved, ask the user to confirm the exact project key from their Jira instance.

### Step 2 — Fetch Active Cards

Query all issues from the board where status falls in the active range:

**Include:** `Ready`, `In Queue`, `Queue`, `In Progress`, `In Design`, `Design`, `Review`, `In Review`, `Code Review`, `QA`, `In QA`, `Testing`, `UAT`, `Done`

**Exclude:** `Backlog`, `Deployed`, `Cancelled`, `Rejected`, `Won't Fix`, `Closed`

For each issue retrieve:
- Key, summary, status, priority
- Assignee (display name)
- Reporter (display name)
- Created date and last updated date
- All comments (author, timestamp, body text)

### Step 3 — Compute Age and Flag Aging Cards

For every card, compute age in days = today's date minus the card's **created** date. Flag as aging if age > 3 days.

Age severity:
- 🔴 > 7 days — critical, must be discussed
- 🟠 4–7 days — aging, ask for update
- 🟡 1–3 days — recent, no flag needed
- 🟢 0 days — brand new today

### Step 4 — Analyse Comments for Pending Owner and Blockers

For each card with comments, apply the following logic:

**Pending On (who is the card waiting for?):**
1. Find the most recent comment on the card
2. If that comment @mentions someone, that person is who the card is pending on
3. If the commenter is reporting completion and tagging someone to act (e.g. "@Shafana please review", "@Arpith please move to done"), the mentioned person is the pending owner
4. If no clear mention exists, default to the assignee — if they haven't commented recently, the card is pending on them
5. If a comment says "ready to test", "please move to QA", or similar, flag the card as needing a status change, not just a discussion

**Blocker / Dependency detection:**  
Scan all comment text for the following keywords and phrases:
- `blocked`, `waiting on`, `dependency`, `need input from`, `pending client`, `pending customer`, `client review`, `customer approval`, `cannot proceed`, `on hold`, `waiting for confirmation`, `external dependency`

If any are found, extract the relevant sentence and mark the card as having a blocker or external dependency.

### Step 5 — Produce the Standup Report

Output a structured report in the sections below.

---

## Output Format

### Board Overview

Display a summary table of card counts by status:

| Status | Count |
|---|---|
| Ready | N |
| Queue | N |
| In Progress | N |
| In Design | N |
| QA | N |
| Done | N |
| **Total active** | **N** |

Also display:
- Total cards aging > 3 days
- Total cards with detected blockers or external dependencies

---

### Facilitator Notes

A concise 2–4 sentence summary for the person running the meeting. Highlight:
- The most critical aging cards by name
- Any patterns (e.g. multiple cards stalled on the same person or waiting on the same client)
- What the facilitator should focus on or probe in the meeting

---

### 🔴 Action Items — Ask the Team Today

For each card that is **aging AND has a pending owner identified from comments**, list:

```
[CARD-KEY] — Card title · Status · Assignee
- Age: X days
- Latest comment: who said what, on what date
- Pending on: [Name] — reason (e.g. asked to review design, card is ready to be tested)
- Ask: the specific question to raise in the standup
```

---

### 🟡 Customer / Client Dependency Blockers

For each card where comments indicate an external client or customer action is needed:

```
[CARD-KEY] — Card title · Status · Assignee
- Age: X days
- Dependency: [what is being waited on and from whom]
- Ask: whether there is a timeline or a recent update from the client
```

---

### 🟠 Aging Cards with No Recent Comments

Cards that are aging but have had no comment activity — these are stale and need a live status check from the team. Display as a table:

| Card | Summary | Status | Age | Assignee |
|---|---|---|---|---|
| CC-XXXX | title here | In Progress | 15d | Name / Unassigned |

---

### 🟢 New Cards (created today)

Any cards created on the day the command is run, with their assignee and current status. Flag any that are unassigned so they can be picked up in the meeting.

---

### Full Card Listing (grouped by status)

All active cards, grouped in this order:  
In Progress → In Design → QA → Review → Queue → Ready → Done

For each card:
```
[KEY] Summary
Assignee: Name | Status: X | Priority: Y | Age: Xd | Reporter: Name
Latest update: [Author, Date] — one-line comment summary
```

---

## Rules

- Always use the Atlassian MCP — never hardcode project keys, account IDs, or board names
- Always include direct Jira ticket links: `https://[workspace].atlassian.net/browse/[KEY]`
- Age is calculated from the card's **created** date, not the last updated date
- Aging threshold is 3 days — any card older than this is flagged
- For cards with no comments, the pending owner defaults to the current assignee
- Unassigned cards must be explicitly flagged and called out
- Cards in Done status are included in the count but not individually listed unless they are relevant to an active blocker discussion
- If the board name cannot be resolved, clearly say so and ask for the exact Jira project key
- If no active cards are found, output: "✅ Board is clear — no active cards in the standup range."
- Never include cards in Backlog, Deployed, Cancelled, Rejected, Closed, or Won't Fix — these statuses are out of scope for kanban standups

---

## Design Notes

This command was built for the daily kanban standup ritual at 7EDGE, where the PM/BA reviews all active cards with the team before or during the meeting. Key design decisions:

1. **Pre-meeting use** — run this *before* the call to know exactly what to ask and whom to ask it, so the meeting is focused rather than exploratory
2. **Comment intelligence** — most stall signals are buried in card comments, not status fields; this command reads and surfaces them so nothing is missed
3. **Aging from created date** — a card's age since creation is a more reliable stagnation indicator than its last-updated timestamp, which can be triggered by minor field changes
4. **Board-scoped, not person-scoped** — unlike `/PM/jira-update` (which is person-centric), this command gives a complete team view of what is live on the board

**Companion command:** `/PM/jira-update` — person-centric Jira check (assigned cards + unacknowledged mentions for an individual)
