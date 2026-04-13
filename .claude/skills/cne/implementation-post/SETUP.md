# Setup Guide: Implementation Post Skill

This skill helps you document implementations and publish them to the 7EDGE Community. It works across **Claude Code CLI**, **Claude Desktop**, and **Claude Web**.

**Prerequisite:** You need a Discourse API key from `https://community.7edge.com`. If you don't have one, generate it in your user preferences (or contact an admin).

---

## Quick Start

### Claude Code CLI — Plug & Play

Run this from the root of any project:

```bash
bash .claude/skills/implementation-post/install.sh
```

The script will:
- Copy the skill into `.claude/skills/implementation-post/`
- Set up the Discourse MCP server in `.mcp.json`
- Configure `.claude/settings.local.json`

Then restart Claude Code in that directory. Done!

---

### Claude Desktop — Plug & Play

Run this once (on your machine):

```bash
bash /path/to/implementation-post/install-desktop.sh
```

The script will:
- Detect your OS and find the right config location
- Add the Discourse MCP server to `claude_desktop_config.json`
- Print instructions for the next step

Then:
1. Open Claude Desktop
2. Create or open a **Project**
3. Go to Project Settings → **Instructions** (or Custom Instructions)
4. Paste the full contents of `SKILL.md`
5. Save and restart Claude Desktop

---

### Claude Web (claude.ai) — No MCP (Manual Publish)

Claude Web doesn't support local MCP servers, but you can still use the skill:

1. Go to **claude.ai** and create or open a Project
2. Go to **Project Instructions**
3. Paste the full contents of `SKILL.md`
4. Save

When publishing, the skill will give you the finished post. You'll either:
- Go to `https://community.7edge.com/new-topic`, select a category, and paste
- Or run a curl command to publish (see the SKILL.md fallback instructions)

---

## Setting Up Your Credentials

Before publishing posts, you need a credentials file on your machine.

**Create this file:**
```
~/.config/discourse/7edge-profile.json
```

**With this content** (replace with your actual credentials):
```json
{
  "site": "https://community.7edge.com",
  "auth_pairs": [
    {
      "site": "https://community.7edge.com",
      "api_key": "YOUR_API_KEY_HERE",
      "api_username": "YOUR_DISCOURSE_USERNAME"
    }
  ],
  "read_only": false,
  "allow_writes": true
}
```

**To get your API key:**
1. Go to `https://community.7edge.com/u/YOUR_USERNAME/preferences`
2. Click **API keys**
3. Create a new key
4. Copy it into the file above

---

## Environment Comparison

| | Claude Code CLI | Claude Desktop | Claude Web |
|---|---|---|---|
| Skill loads automatically | ✅ Yes | ❌ Manual (Project Instructions) | ❌ Manual (Project Instructions) |
| Publishes to Discourse | ✅ Yes | ✅ Yes (after MCP setup) | ❌ Manual only |
| Requires credentials file | ✅ ~/.config/discourse/... | ✅ ~/.config/discourse/... | ✅ ~/.config/discourse/... (for curl) |
| Setup time | ~30 seconds | ~1 minute | ~1 minute |

---

## Troubleshooting

**"Could not find Discourse server"**
- Claude Code: Restart Claude Code after running `install.sh`
- Desktop: Restart Claude Desktop after updating the config
- Web: Use the manual curl command

**"API key not found"**
- Make sure `~/.config/discourse/7edge-profile.json` exists
- Check the `api_key` and `api_username` are correct
- Verify the file has read permissions (`chmod 600` on Linux/Mac)

**"Publishing failed with 422"**
- Check your Discourse username matches the one in the credentials file
- Verify you have write permissions on the Discourse community
- Ensure the category ID is correct (the skill fetches this dynamically)

**"I don't know my API key"**
- Go to `https://community.7edge.com/u/YOUR_USERNAME/preferences/api-keys`
- If no keys exist, create one by clicking the button
- Copy the key to your credentials file

---

## For Other Users / Team Members

If someone else on your team wants to use this skill:

1. They need their own Discourse account and API key (see above)
2. They create their own `~/.config/discourse/7edge-profile.json` with their credentials
3. They run `install.sh` in their project (Claude Code) or `install-desktop.sh` (Desktop)
4. The scripts will use their own credentials automatically

Each person's posts will appear under their own name on the community.
