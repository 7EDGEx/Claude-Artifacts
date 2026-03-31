# Pull Latest Code

Pull the latest changes from the 7EDGE shared repo into your local machine. Run this every time before you start working.

## Steps

1. First, check if git is available:
   ```bash
   git --version
   ```
   If this fails, tell the user: "Git is not installed. Please install Git from https://git-scm.com and re-open your terminal."

2. Check we are inside the Claude-Artifacts repo:
   ```bash
   git remote -v
   ```
   If `7EDGEx/Claude-Artifacts` does not appear, tell the user: "You are not inside the Claude-Artifacts folder. Please open your terminal inside that folder and try again."

3. Check if the upstream remote exists:
   ```bash
   git remote get-url upstream 2>/dev/null || echo "UPSTREAM_MISSING"
   ```
   If the output is `UPSTREAM_MISSING`, add it:
   ```bash
   git remote add upstream https://github.com/7EDGEx/Claude-Artifacts.git
   ```
   Tell the user: "Connected to the 7EDGE shared repo for the first time."

4. Fetch all the latest changes:
   ```bash
   git fetch upstream
   git fetch origin
   ```

5. Pull the latest changes into your current branch:
   ```bash
   git pull upstream main --no-rebase
   ```
   - If there are **merge conflicts**, tell the user clearly: "There are some conflicts in these files: [list them]. Please tell me which version you want to keep and I will help you fix it."
   - If the pull succeeds, confirm: "✅ Your code is now up to date with the latest 7EDGE version."

6. Show a friendly summary:
   ```bash
   git log --oneline -5
   ```
   Tell the user: "Here are the 5 most recent changes in the repo."

## Notes
- This command is safe to run multiple times.
- It will never delete your own work.
- If you see any authentication error, type `/authenticate-github` or ask for help.