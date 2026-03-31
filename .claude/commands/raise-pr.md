# Raise a Pull Request (PR)

Submit your changes to the 7EDGE team for review. Run this after you have pushed your code with /push-code.

## Steps

1. Check we are inside the Claude-Artifacts repo:
   ```bash
   git remote -v
   ```
   If `Claude-Artifacts` does not appear, tell the user: "You are not inside the Claude-Artifacts folder. Please open your terminal inside that folder and try again."

2. Make sure the latest changes are pushed first:
   ```bash
   git status
   ```
   If there are uncommitted changes, tell the user: "You have unsaved changes. Please run /push-code first, then come back and run /raise-pr."

3. Check if GitHub CLI is installed:
   ```bash
   gh --version
   ```
   - If not installed, tell the user: "We need GitHub CLI to raise PRs. Please install it from https://cli.github.com — it only takes 2 minutes. After installing, run /raise-pr again."

4. Check if the user is authenticated with GitHub CLI:
   ```bash
   gh auth status
   ```
   - If not authenticated, tell the user: "Please authenticate with GitHub first. Run: `gh auth login` → choose GitHub.com → HTTPS → Login with a web browser. Once done, run /raise-pr again."

5. Ask the user two quick questions:
   - "What is the title of your PR? (Short and clear, e.g. 'Add DevOps commands for non-tech users')"
   - "What did you change? Give me 1–2 sentences for the description."

   Wait for replies before continuing.

6. Create the Pull Request:
   ```bash
   gh pr create \
     --repo 7EDGEx/Claude-Artifacts \
     --base main \
     --head YOUR_GITHUB_USERNAME:main \
     --title "[USER_TITLE]" \
     --body "[USER_DESCRIPTION]\n\nRaised using /raise-pr command."
   ```
   Replace `YOUR_GITHUB_USERNAME` with the output of `gh api user --jq .login`, `[USER_TITLE]` with the title they gave, and `[USER_DESCRIPTION]` with the description they gave.

   To get the GitHub username automatically:
   ```bash
   GH_USER=$(gh api user --jq .login)
   ```

   Full command:
   ```bash
   GH_USER=$(gh api user --jq .login)
   gh pr create \
     --repo 7EDGEx/Claude-Artifacts \
     --base main \
     --head "$GH_USER:main" \
     --title "[USER_TITLE]" \
     --body "[USER_DESCRIPTION]\n\nRaised using /raise-pr command."
   ```

7. If the PR is created successfully, show the user the PR link and say:
   "✅ Your Pull Request is live! Here is the link: [PR_URL]
   
   The 7EDGE tech team will now review it. You don't need to do anything else. Once they approve and merge it, everyone at 7EDGE will get your changes the next time they run /pull-code."

8. If a PR already exists for this branch, the CLI will say so. Tell the user: "You already have an open PR from this branch. No need to raise another one. You can keep pushing more changes with /push-code and they will automatically appear in the same PR."

## Notes
- You only raise one PR per batch of changes. Push as many commits as you want to the same PR.
- The reviewer does not need to be you — just raise it and relax.
- If your PR is rejected with comments, fix the files, run /push-code again, and the PR will update automatically.