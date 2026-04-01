# Push My Changes

Save your work and push it to GitHub. Run this when you are done making changes and want to save them.

## Steps

1. Check we are inside the Claude-Artifacts repo:
   ```bash
   git remote -v
   ```
   If `Claude-Artifacts` does not appear, tell the user: "You are not inside the Claude-Artifacts folder. Please open your terminal inside that folder and try again."

2. Check what files have been changed:
   ```bash
   git status
   ```
   - If there are **no changes**, tell the user: "There are no new changes to push. Make some edits first, then run /push-code again." and stop.
   - If there are changes, list them clearly: "I found changes in these files: [list them]. I will push all of them."

3. Ask the user for a short description of their changes. Say:
   "Please describe what you changed in one sentence (e.g. 'Added pull-code command for DevOps team'). This will be saved as the commit message."

   Wait for the user's reply. Use their reply as the commit message. If they say something very vague like "changes" or "stuff", suggest a better message based on the files changed.

4. Stage all changes:
   ```bash
   git add .
   ```

5. Commit with the user's message:
   ```bash
   git commit -m "[USER_MESSAGE]"
   ```
   Replace `[USER_MESSAGE]` with what the user said.

6. Push to their fork:
   ```bash
   git push origin main
   ```
   - If this gives an **authentication error**, tell the user: "GitHub needs to verify who you are. Please run this command and follow the steps: `gh auth login`  — choose GitHub.com → HTTPS → Login with a web browser. Once done, run /push-code again."
   - If the push asks to **set upstream**, run: `git push --set-upstream origin main`
   - If it succeeds, confirm: "✅ Your changes have been saved to GitHub! Your fork is updated."

7. Show the user their commit:
   ```bash
   git log --oneline -3
   ```
   Say: "Your latest save is now on GitHub. Run /raise-pr when you want the 7EDGE team to review and merge your changes."

## Notes
- This command saves ALL changed files. If you only want to save specific files, ask for help.
- It pushes to YOUR fork, not directly to the 7EDGE repo. The 7EDGE repo is only updated after a PR is merged.
- You can push as many times as you like — it will not break anything.