---
name: jira-assignee-updater
description: >
  Automatically updates the assignee field on any Jira project when a card is
  moved to a specific column or status. Use this skill whenever the user says
  things like "move PROJ-123 to Done", "transition this card to QA Ready",
  "card moved to Deployed", "update assignee after status change", or any
  variation of moving/transitioning a Jira issue to a status that has an
  assignment rule. Works across all Jira projects.

  Assignment rules (apply to ALL projects):
  - Moved to "Done"      → assign to Apeksha A
  - Moved to "QA Ready"  → assign to Roopesh
  - Moved to "Deployed"  → assign to Namratha Shettigar
---

# Jira Auto-Assign on Status Transition

When any Jira card is moved to certain statuses, automatically update the
`assignee` field according to the rules below. This works across **all projects**.

---

## Assignment Rules

| Status / Column | Assign To          | Account ID                                    |
|-----------------|--------------------|-----------------------------------------------|
| Done            | User A          | `<ACCOUNT_ID_User_A>`  |
| QA Ready        | User B            | `<ACCOUNT_ID_User_B>`  |
| Deployed        | User C | `<ACCOUNT_ID_User_C>` |

---

## Workflow

### Step 1 — Identify the Issue(s) and Target Status

Extract from the user's message:
- **Issue key(s)** (e.g. `PROJ-123`, `INDY-456`) — ask if not provided
- **Target status** — one of: `Done`, `QA Ready`, `Deployed`

If either is missing, ask the user before proceeding.

For **multiple issues**, process each one in sequence (Steps 2–3) and show a
combined summary at the end.

---

### Step 2 — Resolve the CloudId

Use cloudId: `<YOUR_CLOUD_ID>` for all issues on `<YOUR_SITE>.atlassian.net`.

If you don't know your cloudId, call `Atlassian:getAccessibleAtlassianResources` to find it.

---

### Step 3 — Transition the Issue

Call `Atlassian:getTransitionsForJiraIssue` with the issue key and cloudId.

Find the transition whose `name` matches the target status (case-insensitive).
Then call `Atlassian:transitionJiraIssue` with that transition ID.

> If no matching transition is found, inform the user that the card can't be
> moved to that status from its current state, and skip to the next issue.

---

### Step 4 — Update the Assignee

After a successful transition, call `Atlassian:editJiraIssue`:

```
fields: {
  "assignee": { "accountId": "<account-id-from-table-above>" }
}
```

Use the account ID from the **Assignment Rules** table that matches the target status.

---

### Step 5 — Confirm

After processing all issues, report a summary:

> ✅ **PROJ-123** → Done, assigned to Apeksha A
> ✅ **PROJ-456** → QA Ready, assigned to Roopesh
> ❌ **PROJ-789** → Could not transition (already in Done)

---

## Edge Cases

- **Unknown status**: If the user asks to move to a status not in the rules table
  (e.g. "In Progress"), still perform the transition but do NOT change the assignee.
  Inform the user: "No auto-assignment rule for '[status]' — assignee unchanged."

- **Transition already in target status**: Skip the transition but still update
  the assignee in case it was missed previously.

- **Transition fails**: Report the failure clearly and move on to the next issue
  (don't abort the entire batch).

---

## Quick Reference

- **CloudId**: `<YOUR_CLOUD_ID>` — find via `Atlassian:getAccessibleAtlassianResources`
- **Atlassian site**: `<YOUR_SITE>.atlassian.net`

> 💡 **Setup:** Replace all `<PLACEHOLDER>` values with your own before installing this skill.
> To find account IDs, use `Atlassian:lookupJiraAccountId` with each person's name.