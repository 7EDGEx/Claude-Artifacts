Fetch the skill usage report and display it as a formatted table.

Run this command:

```bash
curl -s https://uwrttdldcuzwczvaihwb.supabase.co/functions/v1/skill-report
```

Parse the JSON response and display:
1. A table with columns: Skill | Total Uses | Last Used — sorted by most used
