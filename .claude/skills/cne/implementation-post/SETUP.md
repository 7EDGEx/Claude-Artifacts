# Setup Guide: Implementation Post Skill

This skill helps you document implementations and publish them to the 7EDGE Community. It works with **Claude Code** and **Claude Desktop** on all platforms (Mac, Windows, Linux).

**Prerequisite:** You need a Discourse API key from `https://community.7edge.com`. If you don't have one, generate it in your user preferences (or contact an admin).

---

## Quick Start: One Unified Installer

We've combined Claude Code and Claude Desktop into a **single `install.sh` script** that automatically detects which platform you're using.

### Step 1: Download the Script

```bash
curl -fsSL https://raw.githubusercontent.com/Khaleelibrahimofficial/Claude-Artifacts/implementation-post-local-mcp/.claude/skills/cne/implementation-post/install.sh -o install.sh
chmod +x install.sh
```

### Step 2: Run It From Your Platform

#### 🍎 **macOS** (Terminal app)
```bash
./install.sh
# Follow the prompts to choose Claude Code or Claude Desktop
```

#### 🪟 **Windows** (PowerShell)
```powershell
# Open PowerShell and navigate to where you saved install.sh
bash install.sh

# If bash isn't recognized, you have a few options:
# 1. Install Git for Windows (includes bash)
# 2. Use Windows Subsystem for Linux (WSL)
# 3. Install Node directly and use the installer this way
```

#### 🐧 **Linux** (Terminal/Bash)
```bash
bash install.sh
```

### Step 3: Choose Your Platform

The script will ask:
```
Which version are you installing for?
  1) Claude Code (CLI, Web app, IDE extensions)
  2) Claude Desktop (native Mac/Windows/Linux app)
```

---

## Installation Paths

### For Claude Code

If you choose **Claude Code**, the script will ask where to run from:

**Global Installation** (available in all projects):
```bash
cd ~                    # Go to home directory
bash install.sh         # Installs to ~/.claude/
```

**Project Installation** (available only in this project):
```bash
cd /path/to/my/project  # Go to your project
bash install.sh         # Installs to ./. claude/
```

Then restart Claude Code and the skill appears in `/skills`.

### For Claude Desktop

If you choose **Claude Desktop**, the script will:
- Detect your OS and find the right config location
- Add the MCP server to `claude_desktop_config.json`
- Ask for credentials

Then:
1. Open Claude Desktop
2. Create or open a **Project**
3. Go to Project Settings → **Instructions**
4. Paste the full contents of `SKILL.md`
5. Save and restart Claude Desktop

**Config locations:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/claude/claude_desktop_config.json`

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
2. They run `bash install.sh` on their machine
3. The script will ask if they're using Claude Code or Claude Desktop
4. Their credentials will be saved in `~/.config/discourse/7edge-profile.json`

Each person's posts will appear under their own name on the community.

---

## What Doesn't Work Where

| Feature | Claude Code | Claude Desktop | Claude Web |
|---|---|---|---|
| Automatic skill loading | ✅ Yes | ⚠️ Manual setup | ❌ Not supported |
| Publish to Discourse | ✅ Automatic | ✅ Automatic | ⚠️ Manual copy-paste |
| MCP server support | ✅ Full | ✅ Full | ❌ No local MCP |

For Claude Web (claude.ai), you'll need to manually paste the output to https://community.7edge.com or use a curl command.
