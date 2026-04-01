---
name: plan-my-day
description: >
  Reads the user's Google Calendar for today, builds a chronological action plan with one-line
  meeting descriptions, and saves it as a Gmail draft. Trigger immediately whenever the user says
  "plan my day", "plan my day today", "what's my day look like", "create my daily plan",
  "draft my day plan", or any similar phrase requesting a structured overview of today's calendar
  sent to Gmail. Do NOT ask clarifying questions — execute the full workflow automatically.
compatibility: "Requires Google Calendar MCP (https://gcal.mcp.claude.com/mcp) and Gmail MCP (https://gmail.mcp.claude.com/mcp) connected in Claude.ai Settings → Connectors."
---

# Plan My Day Skill

Automates daily planning by pulling today's calendar events and drafting a structured action plan to Gmail.

---

## Workflow

Execute these steps in order. Do not pause or ask for confirmation between steps.

### Step 1 — Fetch Today's Calendar Events

Use the Google Calendar MCP tool to list all events for today (from 00:00 to 23:59 in the user's local time).

- Call `gcal_list_events` with today's date range.
- If multiple calendars are present, fetch from all of them.
- Include: event title, start time, end time, location (if any), attendees (if any), and description/notes (if any).

### Step 2 — Build the Action Plan

Sort all events strictly by start time (chronological order).

For each event, produce one line in this format:

```
HH:MM – HH:MM | [Event Title] — [One-line description]
```

Rules for the one-line description:
- If the event has a description/agenda in the calendar, summarize it in ≤12 words.
- If no description exists but attendees are present, write: "Meeting with [names or count]."
- If it's a solo block (no attendees, no description), write what the title implies, e.g. "Focus block", "Lunch break", "Travel time", etc.
- Keep it crisp — no fluff.

If there are no events today, the action plan body should say: "No meetings scheduled today. Clear calendar."

### Step 3 — Format the Gmail Draft

Compose the draft with this structure:

```
Subject: My Day Plan — [Today's Date, e.g. Monday, March 30, 2026]

Good morning,

Here's your action plan for today:

──────────────────────────────
[Chronological event list, one per line, as formatted above]
──────────────────────────────

Total meetings: [N]
First meeting: [HH:MM]
Last meeting ends: [HH:MM]

Have a productive day.
```

- "To" field: the user's own Gmail address (fetch via `gmail_get_profile`).
- Do not CC or BCC anyone.
- Save as draft — do NOT send.

### Step 4 — Confirm to User

After creating the draft, reply in chat:

> "Done. Draft saved to your Gmail — '[Subject line]'. [N] meetings on your calendar today, from [first time] to [last end time]."

If there are zero events:

> "Done. Draft saved — no meetings on your calendar today."

---

## Error Handling

| Situation | Action |
|---|---|
| Google Calendar MCP unavailable | Tell user to connect Google Calendar in Settings → Connectors, then stop. |
| Gmail MCP unavailable | Tell user to connect Gmail in Settings → Connectors, then stop. |
| Cannot determine user's timezone | Default to UTC and note this in the draft. |
| Events fetched but all-day events only | Include them at the top of the list labeled `All Day` with no time range. |

---

## Notes

- Never send the email. Always save as draft only.
- If the user says "plan my day" without a date, always assume today.
- If the user says "plan my day for tomorrow" — adjust the date range to tomorrow accordingly, and update the subject line.
