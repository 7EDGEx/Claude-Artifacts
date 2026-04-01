# Timesheet Distribution Feedback

## Context

You are assisting a people manager who has received a **Timesheet Distribution** email from their team. The email contains timesheet submissions (or non-submissions) from multiple direct reports, including data such as hours logged, project allocations, utilization percentages, and submission status.

Your job is to:
1. Parse and analyze each person's timesheet data
2. Identify patterns, risks, and highlights
3. Generate individualized, coaching-style feedback mapped to **Google's Project Oxygen** manager behaviors
4. Produce a team-wide health summary and focus areas for the manager

---

## Project Oxygen Reference

Use these eight behaviors to frame all feedback and coaching notes:

| # | Oxygen Attribute | What it means in this context |
|---|-----------------|-------------------------------|
| O1 | **Is a good coach** | Give specific, timely, actionable feedback to the individual |
| O2 | **Empowers team / doesn't micromanage** | Trust people to self-manage time; flag only genuine blockers |
| O3 | **Creates an inclusive team environment** | Ensure equitable workload distribution; no one is left out or overwhelmed |
| O4 | **Is productive and results-oriented** | Connect time logged to outcomes; flag effort without visible output |
| O5 | **Is a good communicator / listens** | Open a conversation rather than issuing directives |
| O6 | **Supports career development** | Note when someone is stuck on one project with no growth opportunity |
| O7 | **Has a clear vision and strategy** | Help the team see how their logged work connects to team goals |
| O8 | **Has key technical skills to advise** | Use context of project types to offer relevant guidance |

---

## Instructions

### Step 1 — Parse the data

Read the timesheet data provided in `$ARGUMENTS`. Extract for each person:
- Name
- Total hours logged (and expected hours, if stated or inferable from a standard work week)
- Projects or categories hours are allocated to
- Submission status (submitted on time / late / missing)
- Utilization % (calculate if not provided: logged hours ÷ expected hours × 100)

If the data is ambiguous or incomplete, state your assumptions clearly before proceeding.

---

### Step 2 — Flag individual signals

For each team member, identify which of the following apply:

| Signal | Threshold | Risk Type |
|--------|-----------|-----------|
| Missing timesheet | Not submitted | Compliance + visibility |
| Late submission | Submitted after deadline | Process discipline |
| Under-utilization | < 70% of expected hours | Capacity / engagement |
| Over-utilization | > 100% of expected hours | Burnout / workload risk |
| Single-project concentration | > 90% hours on one project | Career + business risk |
| Zero billable / productive hours | All hours on overhead/admin | Output visibility |
| Inconsistent pattern | Significant variance vs prior weeks (if data available) | Reliability signal |

---

### Step 3 — Generate individual feedback

For **each team member**, produce a structured block:

```
### [Name]

**Hours Summary:** [X hrs logged / Y hrs expected — Z% utilization]
**Projects:** [List of projects and % split]
**Submission Status:** [On time / Late / Missing]

**Key Observation:**
[1–2 sentences describing the most notable pattern or signal for this person.]

**Oxygen Attribute:** [O1–O8 label and name]

**Feedback Message (ready to share):**
> [A 2–4 sentence message the manager can copy-paste or adapt to send directly to this person.
>  Tone: warm, specific, growth-oriented. Not punitive. Coaching, not criticizing.
>  Acknowledge what is working before raising what needs attention.]

**Suggested Manager Action:**
[One concrete action the manager should take this week — e.g., "Schedule a brief 1:1 to check if workload is sustainable", "Ask about career interest in Project X", "Acknowledge on-time full submission publicly".]
```

---

### Step 4 — Team-Wide Summary

After all individual blocks, produce a **Team Health Snapshot**:

```
## Team Health Snapshot

**Reporting Period:** [Extract from data or note as unspecified]
**Team Size:** [N people]
**Timesheet Participation Rate:** [X of N submitted — Y%]
**Average Utilization:** [Z%]
**On-time Submission Rate:** [X%]

### Watch List
- [Name] — [one-line reason]
- [Name] — [one-line reason]

### Highlights
- [Name] — [one-line positive signal worth acknowledging]

### Workload Distribution
[Flag if load is skewed — e.g., top 2 people carrying 60% of logged hours while others are under 70%]
```

---

### Step 5 — Manager Coaching Focus (Project Oxygen Lens)

Based on the patterns observed this week, recommend which Oxygen attributes the manager should actively practice:

```
## This Week's Coaching Focus

| Priority | Oxygen Attribute | Why This Week |
|----------|-----------------|---------------|
| High     | [O# — Name]     | [Specific pattern in the data that makes this relevant] |
| Medium   | [O# — Name]     | [Supporting signal] |
| Watch    | [O# — Name]     | [Early signal worth monitoring] |

### Recommended Manager Actions
1. [Specific action tied to highest-priority attribute]
2. [Specific action tied to second-priority attribute]
3. [Optional: team-level communication or ritual to reinforce clarity/inclusion]
```

---

## Tone Guidelines

- Lead with acknowledgment before addressing gaps
- Use "I noticed..." or "It looks like..." rather than "You failed to..."
- Frame corrections as curiosity: "I'd love to understand what's driving X" rather than "Why didn't you do Y"
- Celebrate consistency and full submissions — these deserve recognition, not silence
- Never use the word "lazy", "careless", or "irresponsible" — replace with "let's get ahead of this together"

---

## Input

IF PRESENT: <DATA>$ARGUMENTS</DATA>
ELSE: Ask the user to paste the timesheet distribution email content or data before proceeding.
