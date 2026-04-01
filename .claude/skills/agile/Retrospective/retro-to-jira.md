Convert a retrospective improvement item into a Jira Improvement issue.

The description format depends on who raised the item:
- **Team-identified action** → SMART goal (Specific, Measurable, Achievable, Relevant, Time-bound)
- **Facilitator-proposed suggestion** → Behavioural nudge using Atomic Habits framing (James Clear)

---

## Instructions

### 1. Ask for the retro item
If the user hasn't pasted it yet, ask:
> "Please paste the retrospective item or notes you'd like to turn into a Jira issue."

### 2. Clarify the source
Ask:
> "Was this action identified by the team during the retro, or is this a suggestion you're making as the facilitator?"

- **Team-identified** = the team discussed, agreed on, and owns this action → use SMART format
- **Facilitator-proposed** = a behavioural nudge you're suggesting → use Atomic Habits format

### 3. Ask for the Jira project name
Ask:
> "Which project should I create this in? Please give me the project name."

Then use `getVisibleJiraProjects` to match the name to a project key. If multiple matches exist, show them and ask the user to confirm.

---

## Description Formats

### SMART Goal (Team-Identified)

Use this structure in the Jira description:

```
🎯 SMART Goal

**Specific**
[What exactly will be done? By whom? In what context?]

**Measurable**
[What metric or observable outcome defines success?]

**Achievable**
[Why is this realistic given current team capacity?]

**Relevant**
[How does this connect to team health, delivery, or the retro theme?]

**Time-bound**
[Target sprint, date, or number of cycles — must be concrete, not "soon".]

---
📌 Retro Source
[Original retro statement]
```

**Rules:**
- All five sections are mandatory.
- Measurable must name a real metric or checkable outcome.
- Time-bound must include a sprint number or date — never "ongoing" or "soon".
- If the input is vague, infer reasonable specifics and flag with *(assumed — please confirm)*.

---

### Atomic Habits (Facilitator-Proposed)

Use this structure in the Jira description:

```
🧠 Behavioural Improvement (Atomic Habits)

**Identity Shift**
[Reframe as identity. E.g. "We are a team that ships with confidence."]

**The Tiny Habit (1% Better)**
[The smallest possible action that moves in the right direction — make it almost too easy.]

**Implementation Intention**
[When [CUE] happens, we will [ROUTINE].]

**Reward / Reinforcement**
[How will the team notice and celebrate the behaviour?]

**Why This Matters**
[Connect to the retro observation or facilitator's concern.]

---
📌 Facilitator Note
[The original observation or suggestion]
```

**Rules:**
- Identity Shift must be phrased as "We are..." or "We are a team that...".
- Tiny Habit must be one concrete, small action — not a project or outcome.
- Implementation Intention must follow exactly: *"When X happens, we will Y."*
- Reward must be immediate and practical, not aspirational.

---

## Jira Issue Fields

| Field | Value |
|---|---|
| **Issue type** | Improvement |
| **Summary** | `[Retro] <action-oriented verb phrase>` — max 80 chars |
| **Description** | SMART or Atomic Habits format (markdown) |
| **Assignee** | Unassigned |
| **Project** | Resolved from user's project name |

**Summary examples:**
- `[Retro] Define PR review SLA and track weekly`
- `[Retro] Build habit of writing acceptance criteria before sprint planning`
- `[Retro] Reduce context-switching by batching async review slots`

---

## Before Creating

Show the user a preview:
- Summary title
- Project name + key
- Issue type
- Full description

Ask: *"Does this look right? Should I create the issue?"*

Only call `createJiraIssue` after the user confirms.

---

## Edge Cases

| Situation | What to do |
|---|---|
| Retro item is a complaint, not an action | Help reframe into an action, then classify |
| Multiple actions in one paste | Split into separate issues, confirm each |
| Unclear if team or facilitator | Always ask — never assume |
| Project name matches multiple projects | List options, ask user to pick |
