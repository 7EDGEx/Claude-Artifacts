---
name: implementation-post
description: Creates a comprehensive, narrative-style technical post documenting how something was implemented — including the journey, decisions, failures, trade-offs, and lessons learned. Use this skill whenever the user says "write a post", "write a post about what I built", "write a post about the implementation", "document this implementation", "create an implementation write-up", or wants to capture and communicate what was built in blog/guide format. Always begin by asking the user what implementation they want to document before exploring any code.
---

# Implementation Post Generator

> **Setup needed?** See `SETUP.md` in this folder for plug-and-play installation on Claude Code CLI, Claude Desktop, or Claude Web. The skill works best with the Discourse MCP server configured, but has a fallback for publishing without it.

Your job is to produce a narrative-driven technical post that reads like a developer's guide written by someone who actually lived through the implementation — not a dry reference document.

Your job is to produce a narrative-driven technical post that reads like a developer's guide written by someone who actually lived through the implementation — not a dry reference document.

---

## Step 1: Ask First

Before doing anything else, ask the user these questions:

1. **What implementation would you like to document?** (e.g., a specific feature, a set of recent changes, a workflow, a system design, something built in Claude Web/Desktop, etc.)

2. **Do you have code to reference?**
   - "Yes, it's in the current directory" → proceed to Step 2 (code exploration)
   - "No, but it's somewhere I can point to" → ask for path/repo link
   - "No, I built it in Claude Web/Desktop or don't have code access" → use Step 2 (no-code approach)
   - "It's a mix" → use both approaches

Wait for their answers before exploring anything.

## Step 2: Gather Context

**If the user has code to reference:**
- Read the relevant source files
- Check recent git history if helpful: `git log --oneline -20`
- Look at the folder/module structure for the area in question
- Identify key components, architectural decisions, and how things connect
- Look for evidence of failed attempts, workarounds, or pivots (comments, dead code, multiple versions of the same thing)

**If the user has NO code (Claude Web/Desktop, external project, or lost access):**
- Ask them to describe:
  - What problem they solved or what they built
  - Key decisions they made and why
  - What they tried first vs. what actually worked
  - Challenges encountered and how they overcame them
  - The final solution or approach
  - What surprised them or what they'd do differently
  - Tools, libraries, or techniques they used

**For both scenarios:**
- Stay scoped to what the user described
- Ask follow-up questions to fill gaps
- Focus on the *story* (decisions, pivots, learnings) not just the artifacts

## Step 3: Write the Post

This should read like a **real developer's guide** — the kind written by someone who spent weeks on this and wants to save others the pain. It has a narrative arc, not just a list of steps.

### Tone and Style

- **First-person, honest voice** — "we tried X and it didn't work," "this took longer than expected," "the solution was simpler than we made it"
- **Humor where appropriate** — self-deprecating observations about the complexity of the path taken
- **Explain the why, not just the what** — every architectural decision should come with the reasoning and trade-offs considered
- **Acknowledge the journey** — what was tried before the final solution, what failed, what surprising constraints appeared
- **Mixed audience** — technical readers get the depth; non-technical readers understand the problem and value

### Structure

Use this structure, adapting sections to what actually applies. Don't include sections that have nothing to say.

```markdown
# [Descriptive Title — What Was Built and Why It's Interesting]
A subtitle or one-line hook that sets the scene.

## What is [the thing]?
Brief explanation of the technology/feature/system for context. What problem does it solve?

## Prologue / Background
The origin story. Why did this need to be built? What was the starting assumption, and how did it change?
Include failed attempts, unexpected constraints, and the moment of clarity that led to the actual solution.

## Prerequisites
What was needed before starting. Tools, services, permissions, context.

## [Step-by-step sections]
Each major phase of the implementation, in narrative order.
For each step:
- What you did and why
- What you expected vs. what actually happened
- Key configuration decisions and the reasoning behind them
- Code or architecture snippets where useful

## Lessons Learned / Best Practices
What you'd do differently. What worked well. What to watch out for.

## Troubleshooting
Real problems encountered and how they were solved.
Not a generic list — specific issues from this implementation.

## Epilogue
Reflection on the journey. Was the final solution what you expected? What trade-offs were accepted?
What's still imperfect and why that's OK?
```

### What Makes This Different From Documentation

| Documentation | This Post |
|---|---|
| "Configure X by setting Y to Z" | "We tried setting Y to Z, but discovered Z only works when..." |
| Lists steps | Tells a story with steps |
| Assumes success | Acknowledges failures and pivots |
| Neutral voice | Personal, honest voice |
| Reference material | A guide you'd actually want to read |

### Key Elements to Always Include

**The journey arc** — What was the original plan? Where did it break? What was the pivotal insight or suggestion that unlocked the solution?

**Trade-offs made** — Every architectural decision involved giving something up. Name it. "We chose X over Y because Z, even though X comes with the downside of..."

**Cost of complexity** — If the solution is more complicated than expected, say so. Readers appreciate honesty.

**The "aha" moment** — There's usually one. The suggestion from a colleague, the documentation page that changed everything, the realization that reframed the problem.

## Writing Guidelines

**Stay generic** — Don't reference specific project names, company names, or client names. Refer to things as "the client," "the application," "the platform," etc. This also applies to internal code identifiers: don't name specific files (e.g., `view.py`, `auction_view.py`), internal function names, or variable names from the codebase. Describe what something *does* — "the seller dashboard endpoint," "the auction-specific handler" — not what it's called internally. Code snippets are fine, but the surrounding prose should be portable to any reader's context.

**Be concrete** — Vague is forgettable. "This took approximately some hours (days)" is more honest and memorable than "this required significant research time."

**Include the cost / complexity reality** — If something was more expensive, slower, or harder than expected, include that. It's the most valuable part for readers.

**Code snippets are optional** — If you have code, embed it in the narrative with explanation before and after. If you don't have code (Claude Web/Desktop, external project), focus on the *decisions* and *journey* instead. The story is what matters; code is just one way to show it.

**Don't sanitize the story** — If there were two approaches and one failed, say so. The failed path is often more instructive than the success.

## Step 4: Save the File

- Save to `implementation/<specific-case-name>.md` in the project root
  - Use a short, descriptive kebab-case name based on what was documented (e.g., `stripe-payment-flow.md`, `websocket-bidding-engine.md`, `auth-cognito-setup.md`)
  - Create the `implementation/` folder if it doesn't exist
- If the file already exists, ask the user: overwrite or append?

Tell the user the exact path where the file was saved.

## Step 5: Publish to Community (Optional)

After saving, ask the user:

> "Would you like to publish this to the 7EDGE Community?"

If the user wants to publish:

1. **Fetch available categories from Discourse API:**
   - Make a request to `GET https://community.7edge.com/categories.json` with authentication headers
   - Parse the response to extract category names and IDs from `category_list.categories`
   - Discourse returns only active (non-archived) categories by default; filter out any with `archived: true` if present
   - Extract the ID and name for each category

2. **Ask user to select a category:**
   - Present available categories as selectable options via `AskUserQuestion`
   - Format: Single-select (multiSelect: false) with category names as labels and IDs as values
   - Let the user pick one category from the live list
   - Extract the `category_id` from their selection

3. **Condense the content if needed** — ensure the `raw` field is ≤ 30,000 characters. Keep the most valuable sections and trim examples if necessary.

4. **Publish using `discourse_create_topic`** (from the `7edge-community-local` MCP server) with:
   - `title`: from the post
   - `raw`: condensed content
   - `category_id`: the ID from the user's category selection

5. **Inform the user:**
   > "Your post has been published to the 7EDGE Community under [Category Name]. It appears under your own Discourse account and will be live immediately if your trust level permits, or pending review if you're a new poster."

**Note:** Posts are published directly under your Discourse account (authenticated via your personal API key stored locally). Whether the post is live immediately or pending moderation review depends on your Discourse trust level — this is standard Discourse behavior.

**If the MCP server is unavailable** (Claude Web, or MCP not configured):
1. Inform the user: "The MCP server isn't available in this environment. Publishing must be done manually."
2. Provide two options:

   **Option A: Web form (easiest)**
   - Go to `https://community.7edge.com/new-topic`
   - Paste the post content, select a category, and submit

   **Option B: Curl command** (if running from terminal)
   ```bash
   curl -X POST "https://community.7edge.com/posts.json" \
     -H "Api-Key: YOUR_API_KEY" \
     -H "Api-Username: YOUR_USERNAME" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "YOUR_POST_TITLE",
       "raw": "YOUR_POST_CONTENT",
       "category": CATEGORY_ID
     }'
   ```
   - Replace `YOUR_API_KEY`, `YOUR_USERNAME`, `YOUR_POST_TITLE`, `YOUR_POST_CONTENT`, and `CATEGORY_ID` with actual values
   - The category ID can be found by visiting `https://community.7edge.com/categories.json` and looking up the ID for your desired category
