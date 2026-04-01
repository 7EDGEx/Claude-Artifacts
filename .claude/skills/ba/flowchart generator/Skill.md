---
name: flowchart-generator
description: >
  Generates a clear Mermaid flowchart from a Jira user story or task, showing both the ideal
  (happy path) and non-ideal (error/edge case) scenarios to simplify development planning.
  Trigger when the user provides a Jira card number (e.g. PC-123) or a Jira issue URL and asks
  for a flowchart, flow diagram, or wants to understand the flow of a ticket. Do NOT ask
  clarifying questions — fetch the card and generate the flowchart automatically.
compatibility: "Requires Atlassian MCP connected in Claude.ai Settings → Connectors."
---

# Flowchart Generator Skill

Reads a Jira user story or task and produces a structured Mermaid flowchart covering both the
ideal flow and non-ideal (error/edge case) paths — so developers have a clear picture before
writing a single line of code.

---

## Workflow

Execute these steps in order without pausing for confirmation.

### Step 1 — Parse the Input

The user will provide one of:
- A Jira issue key (e.g. `PC-123`, `PROJ-456`)
- A Jira issue URL (e.g. `https://yourorg.atlassian.net/browse/PC-123`)

Extract the issue key from whichever format is given.

### Step 2 — Fetch the Jira Issue

Use the Atlassian MCP `getJiraIssue` tool with the extracted issue key.

Collect the following fields:
- **Summary** — the card title
- **Description** — full content (acceptance criteria, job to be done, outcomes, DoD)
- **Issue Type** — Story, Task, Bug, Subtask
- **Status** — current workflow state
- **Priority** — if set
- **Labels / Components** — if any
- **Linked Issues** — dependencies or related tickets (use `getJiraIssueRemoteIssueLinks` if needed)

If the issue cannot be found, stop and tell the user the key was not found.

### Step 3 — Analyse the Story

Before generating the flowchart, silently derive the following from the issue content:

1. **Entry point** — what triggers this flow? (user action, API call, scheduled job, etc.)
2. **Actors** — who or what is involved? (user, system, external service, database)
3. **Core steps** — the main sequence of actions in the happy path
4. **Decision points** — conditions or validations that branch the flow
5. **Ideal outcome** — what success looks like (maps to Definition of Done / Outcomes)
6. **Non-ideal scenarios** — validation failures, errors, missing data, timeouts, unauthorised access, edge cases mentioned in the acceptance criteria or implied by the domain
7. **End states** — all terminal nodes (success, failure, fallback)

### Step 4 — Generate the Mermaid Flowchart

Produce a single Mermaid `flowchart TD` diagram following these rules:

#### Structure rules
- Start with a single `Start` node
- Use `-->` for normal flow, `-- label -->` for labelled edges
- Use diamond shapes `{condition?}` for every decision point
- Use `[Step]` for process steps, `([Start/End])` for terminals, `[(Database)]` for data stores
- Group the **Ideal Path** and **Non-Ideal Paths** with Mermaid `subgraph` blocks for visual clarity
- Colour-code with `style` directives:
  - Ideal path nodes: `fill:#d4edda,stroke:#28a745,color:#155724`
  - Non-ideal / error nodes: `fill:#f8d7da,stroke:#dc3545,color:#721c24`
  - Decision nodes: `fill:#fff3cd,stroke:#ffc107,color:#856404`
  - Neutral / process nodes: `fill:#d1ecf1,stroke:#17a2b8,color:#0c5460`

#### Content rules
- Keep node labels short (≤ 8 words) and action-oriented (verb + noun)
- Every decision diamond must have at least a `Yes` and `No` branch
- Every non-ideal branch must lead to a clearly labelled error or fallback end state
- Do not add steps not implied by the issue; if a step is ambiguous, make a reasonable assumption and note it

### Step 5 — Format the Output

Respond with the following structure:

---

## Flowchart — [Issue Key]: [Summary]

**Issue Type:** [type] | **Priority:** [priority] | **Status:** [status]

### What this flow covers
[2–3 sentences explaining what the flowchart represents, the trigger, and who the actors are.]

### Ideal Path Summary
[Bullet list of the core happy-path steps in plain English — max 6 bullets.]

### Non-Ideal Scenarios Covered
[Bullet list of each error/edge case branch shown in the diagram.]

### Mermaid Diagram

```mermaid
flowchart TD
    ...
```

### Assumptions & Notes
[Any steps inferred because the ticket was silent on them. Keep this short.]

---

## Error Handling

| Situation | Action |
|---|---|
| Atlassian MCP not connected | Tell user to connect Atlassian in Settings → Connectors, then stop. |
| Issue key not found | Tell user the key was not found and ask them to verify it. |
| Description is empty or very sparse | Generate a minimal flowchart from the summary alone and flag that the ticket lacks detail. |
| Issue is a subtask | Fetch the parent issue as well for broader context before generating the chart. |
| Linked blockers or dependencies exist | Include them as an entry condition or external system node in the diagram. |

---

## Notes

- Always generate the flowchart from the issue content — never ask the user to describe the flow manually.
- If the ticket has multiple acceptance criteria covering distinct sub-flows, produce one combined diagram with subgraphs for each sub-flow.
- Do not embed the Mermaid diagram in HTML — output it as a fenced code block so it renders in the IDE preview.
- If the issue type is **Bug**, frame the flowchart as: current broken flow → detection point → fix path → verification.
