# Jira Card Creation — Command File

---

## Card Template

When asking Claude to create a Jira card, use the following command structure:

```
Create a [ISSUE TYPE] titled "[TITLE]"
- Description: [brief summary of the work]
- Assign to: [me / name]
- Priority: [Low / Medium / High] (optional, defaults to Medium)
- Project: [PC or specify another] (optional, defaults to PC)
```

---

## Description Structure (Auto-applied)

Claude will automatically generate a structured description using this format:

### Job to be Done
> When [situation], I need to [action], so that [outcome].

### Outcomes
- What success looks like — measurable or observable results.

### Dependencies *(if applicable)*
- People, teams, data, or approvals required.

### Definition of Done (DoD)
- [ ] Checklist of specific, verifiable criteria that must be met before the ticket is closed.

---

## Issue Types Available
| Type | Use For |
|------|---------|
| **Task** | A specific, distinct piece of work |
| **Story** | A user-facing goal or broader piece of work |
| **Bug** | Something broken that needs fixing |
| **Subtask** | A smaller piece of work under a parent issue |

---

## Example Commands

**Example 1 — Task:**
> Create a task titled "Onboarding Revamp" — to redesign the onboarding experience for new joiners, ensuring they are set up and productive within their first 30 days. Assign to me.

**Example 2 — Story:**
> Create a story titled "Q2 Hiring Plan" — to plan and execute hiring for Q2 2026 across all open roles. Assign to me.

**Example 3 — With Priority:**
> Create a high priority task titled "Exit Interview Process Update" — to update the exit interview template and process. Assign to me.

---
