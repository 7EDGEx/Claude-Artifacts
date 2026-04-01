---
name: Jira Task Creation
domain: product-management
role: product-manager
scope: task-description
output: jira-card
triggers:
  - create jira task
  - jira card
  - write a task
  - task description
  - jira ticket
  - task card
  - create a ticket
description: >
  Produces a clear, well-structured Jira task card description using a
  consistent four-section format: Job to be Done, Outcomes, Dependencies,
  and Definition of Done.
---

## Core Workflow

1. **Understand the request** — Read the task title or brief provided by the user
2. **Infer context** — Identify what type of work this is (frontend, backend, data, infra, etc.) and who it's for
3. **Draft all four sections** — Follow the output format below exactly
4. **Flag assumptions** — If you inferred anything non-obvious, add a brief note after the card

---

## Output Format

Always produce the description using exactly these four sections in this order.

### 1. Job to be Done
A concise statement of what needs to be accomplished and why. Focus on the problem or goal, not the solution. One to three sentences. Written from the perspective of who is doing the work and what outcome they are driving toward.

### 2. Outcomes
The expected results or impact once the task is completed. Can be qualitative (e.g., improved developer experience) or quantitative (e.g., reduce page load time by 30%). Use bullet points when there are multiple outcomes. Be specific where possible.

### 3. Dependencies
*(Omit this section entirely if there are no known dependencies — do not write "None.")*

People, data, tools, systems, or approvals needed before or during execution that could block or delay the task. List as bullets.

### 4. Definition of Done
A clear, measurable checklist of conditions that must all be true for the task to be considered complete. Write as a checkbox list using `- [ ]` markdown. Each item must be specific and verifiable — answerable with yes/no.

---

## Writing Guidelines

- **Be specific, not generic.** Avoid filler phrases like "ensure quality" or "as needed." Every line should mean something concrete.
- **Job to be Done = problem/goal, not solution.** E.g., "We need to reduce checkout drop-off caused by slow address validation" — not "Build a new address validation API."
- **Outcomes = value delivered, not activity.** Think: what is measurably better after this is done?
- **Definition of Done items are verifiable.** Each one should be answerable with yes/no. If it can't be checked off, rewrite it.
- **Tone:** Professional and clear. Present or future tense. Avoid jargon unless clearly domain-specific.
- **Length:** Thorough but not padded. A focused card beats a bloated one.

---

## Handling Incomplete Input

If the user provides only a vague title or one-line description:

- Make reasonable inferences based on common patterns for that type of work
- Write a complete card using those inferences
- Add a short note at the end flagging what was assumed (e.g., *"Assumed this is for a web frontend — let me know if it's backend or mobile."*)
- Only ask for clarification if the input is so vague that no meaningful output is possible

---

## Example

**Input:** "Add email notifications when a report is exported"

---

**1. Job to be Done**
Users currently have no way of knowing when a long-running report export has finished. We need to notify them via email when their export is ready so they don't have to stay on the page or manually check back.

**2. Outcomes**
- Users receive a timely email notification with a download link when their export completes
- Reduction in support tickets related to "where is my export?"
- Improved satisfaction for users running large or scheduled exports

**3. Dependencies**
- Transactional email provider configured and accessible (e.g., SendGrid, SES)
- Email template design approved by Product/Design
- Export job completion event available in the backend event system

**4. Definition of Done**
- [ ] Email is sent to the user within 60 seconds of export job completion
- [ ] Email contains a working, authenticated download link
- [ ] Link expires after 24 hours and shows a clear expiry message
- [ ] Notification is sent only once per export job (no duplicates)
- [ ] Feature is covered by unit and integration tests
- [ ] Tested end-to-end in staging environment
- [ ] Product owner has reviewed and signed off
