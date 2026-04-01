---
name: Jira to User Flows
domain: product-design
role: product-designer
scope: design
output: user-flows
triggers:
  - user flows from jira
  - jira card user flow
  - convert jira to user flows
  - acceptance criteria user flows
  - COS to user flows
  - jira ticket flows
  - design flows from ticket
description: >
  Fetches a Jira card by ticket number, extracts the Conditions of Satisfaction
  (COS) and Acceptance Criteria, and converts them into structured user flows
  covering happy paths, unhappy paths, and edge cases.
---

## Purpose

Transform a Jira card's Conditions of Satisfaction (COS) and Acceptance Criteria
into actionable, structured user flows that design and engineering teams can use
to validate implementation and inform UX decisions.

---

## Prerequisites

The following environment variables must be set before running this skill:

| Variable | Description |
|---|---|
| `JIRA_BASE_URL` | Your Jira instance URL (e.g. `https://yourorg.atlassian.net`) |
| `JIRA_EMAIL` | Atlassian account email used for API auth |
| `JIRA_API_TOKEN` | Jira API token (generate at id.atlassian.com → Security → API tokens) |

If any variable is missing, stop and ask the user to provide it before continuing.

---

## Core Workflow

### Step 1 — Receive Input

Accept a Jira card number from the user (e.g. `PC-123`, `PROJ-456`).

### Step 2 — Fetch the Jira Card

Call the Jira REST API to retrieve the issue:

```bash
curl -s \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_BASE_URL/rest/api/3/issue/$JIRA_CARD_NUMBER"
```

Extract the following fields from the response:

| Field | JSON Path | Purpose |
|---|---|---|
| Summary | `fields.summary` | Card title |
| Description | `fields.description` | May contain COS and context |
| Acceptance Criteria | `fields.customfield_*` | Check for custom AC field |
| Story / Issue Type | `fields.issuetype.name` | Provides flow context |
| Labels / Components | `fields.labels`, `fields.components` | Domain context |

> **Note:** Jira instances vary. If `fields.description` contains the COS and AC
> (common when using Atlassian Document Format / ADF), parse both the plain text
> and ADF `content` array. If a dedicated custom field exists for Acceptance
> Criteria, prefer that field.

### Step 3 — Extract COS and Acceptance Criteria

Identify and separate:

1. **Conditions of Satisfaction (COS)** — High-level business outcomes. Usually
   phrased as "The system should…", "Users must be able to…", or listed under a
   "COS" heading in the description.

2. **Acceptance Criteria (AC)** — Specific, verifiable conditions. Often written
   in Given/When/Then (Gherkin) format or as a checkbox list under "Acceptance
   Criteria" or "Definition of Done".

If neither section is explicitly labelled, infer COS from outcomes-oriented
statements and AC from specific, testable conditions.

### Step 4 — Generate User Flows

For each distinct COS item and AC scenario, produce a user flow with the structure below.

Analyse for all possible paths:
- **Happy Path** — The intended, successful journey
- **Unhappy Path** — User errors, validation failures, system errors
- **Edge Cases** — Boundary conditions, empty states, concurrent actions, timeouts

### Step 5 — Output

Produce the full output document as specified in the Output Format section.

---

## Output Format

```
# User Flows — [JIRA_CARD_NUMBER]: [Card Summary]

## Card Context
- **Type:** [Story / Task / Bug]
- **Jira Card:** [JIRA_CARD_NUMBER]
- **Fetched:** [date]

---

## Conditions of Satisfaction

> (Extracted verbatim or summarised from the card — do not paraphrase intent)

1. [COS item 1]
2. [COS item 2]
...

---

## Acceptance Criteria

> (Extracted verbatim or summarised from the card)

- [ ] [AC item 1]
- [ ] [AC item 2]
...

---

## User Flows

### Flow [N] — [Short Flow Name]

**Derived from:** [COS item / AC item reference]
**Actor:** [Who performs this action — e.g. Logged-in User, Admin, Guest]
**Entry Point:** [Where the flow starts — e.g. Dashboard, Email link, Settings page]

#### Happy Path

1. [Step 1 — user action or system event]
2. [Step 2]
3. ...
**Outcome:** [What the user achieves or sees]

#### Unhappy Paths

| Scenario | Trigger | System Response |
|---|---|---|
| [Error scenario 1] | [What the user did wrong] | [What the system shows or does] |
| [Validation failure] | [Invalid input] | [Error message / block] |
| [System error] | [Service unavailable] | [Fallback / retry / message] |

#### Edge Cases

- **[Edge case 1]:** [Description and expected behaviour]
- **[Edge case 2]:** [Description and expected behaviour]

---

(Repeat for each additional Flow)

---

## Coverage Matrix

| AC / COS Item | Flow(s) Covered | Happy Path | Unhappy Path | Edge Cases |
|---|---|---|---|---|
| [AC item 1] | Flow 1 | ✅ | ✅ | ✅ |
| [COS item 2] | Flow 2, Flow 3 | ✅ | ✅ | ⚠️ partial |

---

## Open Questions

List any ambiguities in the card that could affect flow design:

- [ ] [Question 1 — e.g. "Is the user redirected or shown an inline confirmation?"]
- [ ] [Question 2]
```

---

## Constraints

### MUST DO
- Fetch the card live via the Jira API; do not ask the user to paste content manually
- Extract both COS and AC separately — do not merge them
- Cover at least one unhappy path per happy path
- Flag missing or ambiguous criteria in the Open Questions section
- Map every AC item to at least one flow in the Coverage Matrix
- Keep flow steps atomic — one action or one system response per step
- Use plain, jargon-free language in flow steps

### MUST NOT DO
- Invent requirements not present in the card
- Skip the Coverage Matrix
- Treat COS and AC as identical concepts
- Generate flows without first confirming the card was successfully fetched
- Omit edge cases for flows involving forms, authentication, or data submission

---

## Error Handling

| Situation | Action |
|---|---|
| Card not found (404) | Inform user, ask to verify the card number |
| Auth failure (401/403) | Ask user to check `JIRA_EMAIL` and `JIRA_API_TOKEN` |
| Empty description | Note it, ask user to paste COS/AC manually |
| No AC field found | Infer AC from the description and label as "(inferred)" |
| ADF format in description | Parse ADF `content` array to extract plain text |

---

## Knowledge Reference

Jira REST API v3, Atlassian Document Format (ADF), Gherkin / Given-When-Then,
user story mapping, happy/unhappy path analysis, UX flow design, acceptance
criteria best practices, conditions of satisfaction, BDD.

---

## Contributor Information
Domain: Design
Skill Type: Jira Integration → User Flow Generation
