#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="$(pwd)"

echo "Installing implementation-post skill into: $TARGET_DIR"

# 1. Copy skill files
mkdir -p "$TARGET_DIR/.claude/skills/implementation-post"
cp "$SCRIPT_DIR/SKILL.md" "$TARGET_DIR/.claude/skills/implementation-post/SKILL.md"
cp "$SCRIPT_DIR/SETUP.md" "$TARGET_DIR/.claude/skills/implementation-post/SETUP.md"
echo "✓ Skill files copied to .claude/skills/implementation-post/"

# 2. Add MCP server to .mcp.json (create if missing, merge if exists)
MCP_FILE="$TARGET_DIR/.mcp.json"
if [ ! -f "$MCP_FILE" ]; then
  cat > "$MCP_FILE" << 'EOF'
{
  "mcpServers": {
    "7edge-community-local": {
      "command": "npx",
      "args": ["-y", "@discourse/mcp@latest", "--profile", "${HOME}/.config/discourse/7edge-profile.json"]
    }
  }
}
EOF
  echo "✓ Created .mcp.json with 7edge-community-local server"
else
  echo "⚠  .mcp.json already exists — please manually add this block if not present:"
  echo ""
  echo '  "7edge-community-local": {'
  echo '    "command": "npx",'
  echo '    "args": ["-y", "@discourse/mcp@latest", "--profile", "${HOME}/.config/discourse/7edge-profile.json"]'
  echo '  }'
fi

# 3. Create/update settings.local.json
SETTINGS_LOCAL="$TARGET_DIR/.claude/settings.local.json"
mkdir -p "$TARGET_DIR/.claude"
if [ ! -f "$SETTINGS_LOCAL" ]; then
  cat > "$SETTINGS_LOCAL" << 'EOF'
{
  "enabledMcpjsonServers": ["7edge-community-local"],
  "enableAllProjectMcpServers": true
}
EOF
  echo "✓ Created .claude/settings.local.json"
else
  echo "⚠  .claude/settings.local.json already exists"
  echo "   Ensure it contains: \"enabledMcpjsonServers\": [\"7edge-community-local\"]"
fi

# 4. Set up credentials
PROFILE_FILE="$HOME/.config/discourse/7edge-profile.json"
if [ -f "$PROFILE_FILE" ]; then
  echo "✓ Credentials already exist at: $PROFILE_FILE"
else
  echo ""
  echo "────────────────────────────────────────────────────────────────"
  echo "Set up your 7EDGE Community credentials"
  echo ""
  echo "You need a Discourse API key. Get one at:"
  echo "  https://community.7edge.com/u/YOUR_USERNAME/preferences/api-keys"
  echo "────────────────────────────────────────────────────────────────"
  echo ""
  read -p "Your Discourse username: " DISCOURSE_USERNAME
  read -p "Your API key: " DISCOURSE_API_KEY
  echo ""

  if [ -z "$DISCOURSE_USERNAME" ] || [ -z "$DISCOURSE_API_KEY" ]; then
    echo "⚠  Skipped credentials setup (username or key was empty)."
    echo "   Create ~/.config/discourse/7edge-profile.json manually before publishing."
  else
    mkdir -p "$HOME/.config/discourse"
    cat > "$PROFILE_FILE" << EOF
{
  "site": "https://community.7edge.com",
  "auth_pairs": [
    {
      "site": "https://community.7edge.com",
      "api_key": "$DISCOURSE_API_KEY",
      "api_username": "$DISCOURSE_USERNAME"
    }
  ],
  "read_only": false,
  "allow_writes": true
}
EOF
    chmod 600 "$PROFILE_FILE"
    echo "✓ Credentials saved to: $PROFILE_FILE"
  fi
fi

echo ""
echo "✓ Installation complete! Restart Claude Code in this directory to activate the skill."
