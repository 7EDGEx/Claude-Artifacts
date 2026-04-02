---
name: prd-generator
description: >
  Generates a structured PRD section from a feature brief. Use when the user
  provides a feature idea, requirement, or brief and wants a full PRD section
  including problem statement, goals, user roles, assumptions, out-of-scope items,
  user stories, and conditions of satisfaction.
trigger: /prd
arguments: $FEATURE_BRIEF
---

## What This Skill Does

Takes a feature brief (plain text description of a feature or requirement) and generates a complete, structured PRD section ready for review or handoff.

---

## Output Structure

Generate the following sections in order. Infer all content from `$FEATURE_BRIEF`. If critical information is missing, flag it with ⚠️ rather than skipping the section.

---

### 1. 📌 Feature Overview
- **Feature Name:** [Infer a clear, concise name]
- **Product / Module:** [Infer or flag ⚠️ if unknown]
- **Author:** [Leave blank for user to fill]
- **Date:** [Leave blank for user to fill]
- **Version:** 1.0

---

### 2. 🧩 Problem Statement
Write 2–4 sentences describing:
- The current pain point or gap
- Who is affected
- What the impact is if this is not addressed

> Format: Plain paragraph. No bullet points. Be specific.

---

### 3. 🎯 Goals
List 3–5 measurable goals this feature aims to achieve.

> Format: Numbered list. Each goal should be outcome-oriented, not task-oriented.
> Example: "Reduce manual data entry time for merchants by at least 50%"

---

### 4. 👥 User Roles
List all user roles that interact with this feature.

| Role | Description | Primary or Secondary |
|------|-------------|----------------------|
| [Role] | [What they do in context of this feature] | Primary / Secondary |

---

### 5. ✅ Assumptions
List all assumptions made while writing this PRD section.

> Format: Numbered list. Flag any assumption that carries risk with ⚠️.

---

### 6. 🚫 Out of Scope
List what is explicitly NOT included in this feature to prevent scope creep.

> Format: Bullet list. Be specific.

---

### 7. 📖 User Stories

Generate one user story per key user role and per key interaction identified in the brief.

For each story use this format:

**Story [X.Y] – [Short Title]**

> As a **[role]**,
> I want to **[action]**,
> So that **[outcome/value]**.

---

### 8. ✔️ Conditions of Satisfaction

For each user story above, list its Conditions of Satisfaction (CoS).

**Story [X.Y] – [Short Title]**
- [ ] [Condition 1 — specific, testable, written from system/user perspective]
- [ ] [Condition 2]
- [ ] [Condition 3]
- [ ] (Edge case or error handling condition)

> Rules for CoS:
> - Each condition must be independently testable
> - Include at least one edge case or error state per story
> - Avoid vague language like "should work correctly" or "should be fast"
> - Use "The system should…" or "The user should be able to…" format

---

### 9. 🔗 Dependencies
List any other features, systems, APIs, or teams this feature depends on.

> Format: Bullet list. Flag blockers with 🔴 and risks with 🟡.

---

### 10. ❓ Open Questions
List any questions that need answers before development can begin.

> Format: Numbered list. Include the question and who should answer it (role/team).

---

## Rules for Generating Output

1. **Infer intelligently** — fill in reasonable details from the brief. Do not ask clarifying questions before generating; flag gaps with ⚠️ inline.
2. **Be specific** — avoid generic filler content. Every line should reflect the actual feature described.
3. **Stay BA-focused** — write for a product/engineering audience. Avoid marketing language.
4. **User stories must be value-driven** — the "so that" clause must state real user or business value, not just restate the action.
5. **CoS must be testable** — if a QA engineer couldn't write a test case from it, rewrite it.
6. **Flag missing info** — use ⚠️ Missing: [what's needed] rather than leaving a section blank or making risky assumptions silently.
7. **Keep it concise** — each section should be complete but not padded. Quality over length.

---

## Example Invocation

```
/prd The merchant should be able to upload products in bulk using an Excel template.
The template should support simple and variant products with Color and Size fields.
A Reference Id groups variant rows to a base product. Invalid rows should be flagged
with error reasons and a downloadable error report should be provided.
```

Claude will generate all 10 sections from that brief.