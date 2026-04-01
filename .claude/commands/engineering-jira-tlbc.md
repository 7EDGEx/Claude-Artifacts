You are helping the user manage their JIRA workflow and git branching. Follow these steps precisely.

**User:** Sonal Monis
**Department:** CNE-3

## Step 1: Fetch JIRA Tasks from Ready Column

Use the Atlassian MCP tool to search for JIRA issues in the project. Query for issues in the "Ready" status/column with priorities: Sev1, Sev2, Sev3, or WP (Weekly Plan).

Use `mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql` with a JQL query like:
```
project = "$ARGUMENTS" AND status = "Ready" AND priority in ("Sev1", "Sev2", "Sev3", "WP") ORDER BY priority ASC
```

If `$ARGUMENTS` is empty, ask the user: "Which JIRA project key should I use? (e.g. TLBC)"

## Step 2: Display the Task List

Present the results in a clean table format grouped by priority:

```
Priority | Type    | Card #   | Title
---------|---------|----------|------------------------
Sev1     | Bug     | TLBC-123 | Critical login failure
Sev2     | Feature | TLBC-124 | Add export functionality
Sev3     | Task    | TLBC-125 | Update documentation
WP       | Feature | TLBC-126 | Weekly dashboard widget
```

Map issue types to labels:
- Bug → `Bug`
- Story → `Feature`
- Task → `Task`

## Step 3: Ask the User to Select a Card

After displaying the list, ask:
> "Which card number would you like to start working on?"

Wait for the user's response with a card number (e.g. `TLBC-123`).

## Step 4: Determine Branch Type Prefix

Determine the branch type prefix from the card's **issue type** and **priority**:

| Condition                              | Branch Prefix |
|----------------------------------------|---------------|
| Priority = Sev1 (any issue type)       | `hotfix`      |
| Issue type = Story                     | `feature`     |
| Issue type = Task                      | `task`        |
| Issue type = Bug (non-Sev1)            | `bugfix`      |

## Step 5: Determine Base Branch and Create Branch

Format the card title for the branch name: lowercase, spaces replaced with hyphens, special characters removed.
Branch format: `{type}/{card-number-lowercase}-{card-title-slugified}`
Example: `hotfix/tlbc-123-fix-login-failure`, `feature/tlbc-124-add-export-functionality`

**If priority is Sev1:**
1. Run: `git checkout master`
2. Run: `git pull origin master`
3. Run: `git checkout -b hotfix/{card-number-lowercase}-{card-title-slugified}`
4. Run: `git commit --allow-empty -m "{CARD_NUMBER} Initial Commit"`

**If priority is Sev2, Sev3, or WP:**
1. Run: `git checkout qa`
2. Run: `git pull origin qa`
3. Run: `git checkout -b {type}/{card-number-lowercase}-{card-title-slugified}` (type = `feature`, `task`, or `bugfix`)
4. Run: `git commit --allow-empty -m "{CARD_NUMBER} Initial Commit"`

Commit message format: `{CARD_NUMBER} Initial Commit` (uppercase card number, e.g. `TLBC-123 Initial Commit`).

## Step 6: Confirm Completion

Report back to the user:
```
✓ Checked out from [master|qa]
✓ Created branch: {branch-name}
✓ Initial commit: "{CARD_NUMBER} Initial Commit"

Ready to start work on {CARD_NUMBER}: {Card Title}
```

## Notes
- Always pull the latest from the base branch before creating the new branch.
- If git commands fail (e.g. branch already exists, merge conflicts), report the error clearly and ask the user how to proceed.
- Do not push the branch unless the user explicitly asks.
