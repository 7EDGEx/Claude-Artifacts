Generate and open the full Claude Code observability HTML report.

Run this command and show the output:

```bash
python3 "$(pwd)/.claude/hooks/generate-report.py" 2>&1
```

If the script outputs "Report generated" — the report is ready. Do NOT try to read or parse the HTML file. Do NOT install any packages. Just confirm it opened successfully and say "Report opened at ~/.claude/observability-report.html".
