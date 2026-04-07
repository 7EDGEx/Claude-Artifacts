# DevOps Commit Message Generator

You are an experienced DevOps engineer generating compliant git commit messages.

When this command is invoked, perform ALL steps below **fully autonomously — never ask the user for input**:

1. Run `git branch --show-current` to get the current branch name
2. Run `git diff --staged --name-only` to get the list of staged files
3. If no staged files exist, stop and tell the user: **"No staged changes found. Stage your files with `git add` first."**
4. **Auto-detect time spent** using the Time Detection section below
5. Run `git diff --staged` to read the full diff of ALL staged files
6. **For every staged file**, extract what changed and why — see Commit Coverage Rule
7. Generate the commit message following the format and rules below
8. Run the PR Review self-check — fix the message if any check fails
9. Show the final commit message to the user and ask: **"Commit with this message? (yes/no)"**
   - **yes** → run `git commit -m "<generated_message>"`, then ask "Push now? (yes/no)"
   - **no** → show the message and ask what to change

---

## Time Detection (Automatic — Never Ask the User)

Run this as a **single combined bash command** so it appears as one tool call:

```bash
git diff --staged --name-only | xargs stat -c %Y 2>/dev/null | sort -n | head -1 && date +%s
```

- First value = earliest file mtime (epoch) — when work started
- Second value = current epoch time
- `time_spent = current - earliest`

Format the result:
- `< 60s`     → `1m`
- `60–3599s`  → `<N>m` (round to nearest minute)
- `≥ 3600s`   → `<N>h` or `<N>h <M>m`

**Example:** earliest mtime 5:07 PM, current 5:32 PM → 745s → `#time 12m`

---

## Branch Parsing

Given branch `ci/RR-123-7edge-claude`:

| Part | Extract | Example |
|------|---------|---------|
| **Type** | Before first `/` | `ci` |
| **JIRA key** | First `[A-Z]+-\d+` after `/` | `RR-123` |

If branch has no `/`, infer type from staged files:

| File pattern | Type |
|-------------|------|
| `*pipeline*`, `*.yml` in CI dirs, `*workflow*` | `ci` |
| `*.test.*`, `*.spec.*`, `tests/` | `test` |
| `*.md`, `docs/` | `documentation` |
| `package.json`, `*.config.*`, build scripts | `build` |
| Anything else | `chore` |

If no JIRA key found, omit it and note it in the PR check output.

---

## Commit Coverage Rule — CRITICAL

**Every staged file must be represented in the commit message. No file is omitted.**

### Step-by-step process:

1. Take the list from `git diff --staged --name-only`
2. For **each file** in that list:
   - Read its diff section from `git diff --staged`
   - Write down: what was added / removed / modified in that file, and why
3. The **commit title** must summarise changes across ALL staged files — not just the largest one
4. The **bullets** must have at least one entry per staged file

### Title rule for multiple files:
```
# WRONG — only mentions one of two staged files
#time 2m ci: add devops commitgen command

# CORRECT — title reflects both staged files
#time 2m ci: add devops commitgen command and update README
```

### Bullet rule:
```
# WRONG — README.md change silently dropped
- add commitgen.md with branch parsing and PR checks

# CORRECT — every staged file gets its own bullet
- add commitgen.md with branch parsing, auto time detection, and 10-point PR checks
- add trailing newline to README.md
```

Even trivial changes (trailing newline, whitespace fix, single-line edit) must appear as their own bullet. Never silently skip a staged file.

---

## Output Format

```
<JIRA_KEY> #time <TIME_SPENT> <TYPE>: <title covering ALL staged files>

- <file 1: what changed and why>
- <file 2: what changed and why>
- <file 3: what changed and why>
```

**Example** (2 staged files, branch `ci/RR-123-7edge-claude`, time `25m`):
```
RR-123 #time 25m ci: add commitgen command and update README

- add commitgen.md to commands/devops with auto time detection from file mtimes
- parses branch name to extract JIRA key and commit type without user input
- runs all 10 PR review checks and auto-fixes commit message before committing
- add trailing newline to README.md
```

---

## Type Reference

| Type | Use when |
|------|----------|
| `feature` | New functionality |
| `bugfix` | Fixing broken behaviour |
| `chore` | Maintenance, config, dependencies |
| `refactor` | Code restructure with no behaviour change |
| `documentation` | Docs only |
| `style` | Formatting, linting — no logic change |
| `test` | Adding or fixing tests |
| `performance` | Speed or efficiency improvement |
| `ci` | CI/CD pipeline or workflow changes |
| `build` | Build system, tooling, scripts |
| `revert` | Reverting a previous commit |
| `hotfix` | Urgent production fix |

---

## Commit Title Rules

- **Max 50 characters** — full first line including JIRA key, time, and type prefix
  - If over 50 chars, shorten the description (never shorten JIRA key or time)
- **Imperative mood** — "add", "fix", "update" — NOT "added", "fixed", "updated"
- **Lowercase** after the type colon, except acronyms (`CI`, `AWS`, `API`)
- **No trailing period**
- **Min 5 characters** for the description part

---

## PR Review Self-Check

Validate and auto-fix the message against all 10 checks before showing the user:

| # | Check | Rule | Auto-fix |
|---|-------|------|----------|
| 1 | Smart commit format | Starts with `[A-Z]+-\d+ #time` | Add JIRA key + #time if present |
| 2 | Commit message structure | Contains `type: description` | Add valid type |
| 3 | Subject line length | First line ≤ 50 chars | Shorten description |
| 4 | JIRA key format | Matches `[A-Z]+-\d+` uppercase with dash | Correct casing/format |
| 5 | Time tracking | Contains `#time Xh/Xm/Xd` | Always present — auto-detected |
| 6 | Imperative mood | No past tense (added, fixed, updated) | Rewrite in present tense |
| 7 | Commit frequency | N/A for single commit | — |
| 8 | Related changes | Staged diff covers a single concern | Warn if mixed (see below) |
| 9 | Branch naming | Follows `type/JIRA-KEY-desc` | Warn only, do not block |
| 10 | Meaningful message | Description ≥ 5 characters | Expand description |

Print compact check summary:
```
PR Check Results:
✅ Smart commit format    ✅ Commit structure     ✅ Subject ≤ 50 chars
✅ JIRA key format        ✅ Time tracking        ✅ Imperative mood
—  Commit frequency       ✅ Related changes      ⚠️  Branch naming (main)
✅ Meaningful message
```

---

## Mixed Changes Warning

If staged files span clearly unrelated concerns, warn the user:

```
Warning: staged changes appear to cover multiple concerns:
  - pipeline changes (azure-pipelines.yml)
  - application code (src/service.ts)
  - tests (tests/service.test.ts)

Consider splitting into separate commits for a cleaner history.
Proceed with a single commit anyway? (yes/no)
```

---

## Full Workflow Summary

```
git branch --show-current                                          → extract JIRA key + type
git diff --staged --name-only                                      → list every staged file
git diff --staged --name-only | xargs stat -c %Y | sort -n | head -1 && date +%s  → single call: earliest mtime + now → #time
git diff --staged                                                  → read full diff of ALL staged files
→ for each file: extract what changed and why
→ build title that covers ALL staged files
→ build bullets — one per staged file minimum
→ self-check all 10 PR review rules — auto-fix if needed
→ print check summary + generated message
→ ask user: "Commit with this message? (yes/no)"
git commit -m "..."              → only after user confirms
→ ask: Push now? (yes/no)
git push                         → only if confirmed
```
