---
name: Skill Usage Report
domain: analytics
scope: reporting
triggers:
  - skill report
  - skill usage
  - which skills are being used
  - skill analytics
  - usage report
description: >
  Fetches and displays a report of which Claude skills have been used and how many times.
---

Fetch the skill usage report and display it as a formatted table.

Run this command:

```bash
curl -s https://uwrttdldcuzwczvaihwb.supabase.co/functions/v1/skill-report
```

Parse the JSON response and display a table with columns:

| Skill | Total Uses | Last Used |

Sort by most used. Format Last Used as a readable date.
