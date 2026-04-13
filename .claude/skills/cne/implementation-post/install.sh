#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="$(pwd)"
BASE_URL="https://raw.githubusercontent.com/Khaleelibrahimofficial/Claude-Artifacts/implementation-post-local-mcp/.claude/skills/cne/implementation-post"

echo "Installing implementation-post skill into: $TARGET_DIR"

# ── helper: check if jq is available ────────────────────────────────────────
has_jq() { command -v jq &>/dev/null; }

# 1. Copy or download skill files
mkdir -p "$TARGET_DIR/.claude/skills/implementation-post"

if [ -f "$SCRIPT_DIR/SKILL.md" ]; then
  # Local files exist — copy them
  cp "$SCRIPT_DIR/SKILL.md" "$TARGET_DIR/.claude/skills/implementation-post/SKILL.md"
  cp "$SCRIPT_DIR/SETUP.md" "$TARGET_DIR/.claude/skills/implementation-post/SETUP.md"
  echo "✓ Skill files copied to .claude/skills/implementation-post/"
else
  # Running via curl | bash — download from GitHub
  echo "Downloading skill files from GitHub..."
  curl -fsSL "$BASE_URL/SKILL.md" -o "$TARGET_DIR/.claude/skills/implementation-post/SKILL.md"
  curl -fsSL "$BASE_URL/SETUP.md" -o "$TARGET_DIR/.claude/skills/implementation-post/SETUP.md"
  echo "✓ Skill files downloaded to .claude/skills/implementation-post/"
fi

# 2. Add MCP server to .mcp.json (create if missing, auto-patch if needed)
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
elif grep -q "7edge-community-local" "$MCP_FILE"; then
  echo "✓ .mcp.json already contains 7edge-community-local — skipping"
else
  echo "⚠  .mcp.json exists but is missing 7edge-community-local."
  if has_jq; then
    jq '.mcpServers["7edge-community-local"] = {
      "command": "npx",
      "args": ["-y", "@discourse/mcp@latest", "--profile", "${HOME}/.config/discourse/7edge-profile.json"]
    }' "$MCP_FILE" > "$MCP_FILE.tmp" && mv "$MCP_FILE.tmp" "$MCP_FILE"
    echo "✓ Auto-patched .mcp.json with 7edge-community-local"
  else
    echo "   jq not found — skipping auto-patch. Install with: sudo apt install jq (or brew install jq)"
    echo "   Then add this entry manually inside the \"mcpServers\" block:"
    echo ""
    echo '    "7edge-community-local": {'
    echo '      "command": "npx",'
    echo '      "args": ["-y", "@discourse/mcp@latest", "--profile", "${HOME}/.config/discourse/7edge-profile.json"]'
    echo '    }'
  fi
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
elif grep -q "7edge-community-local" "$SETTINGS_LOCAL"; then
  echo "✓ settings.local.json already contains 7edge-community-local — skipping"
else
  echo "⚠  .claude/settings.local.json exists but is missing 7edge-community-local."
  if has_jq; then
    jq 'if .enabledMcpjsonServers
          then .enabledMcpjsonServers |= (. + ["7edge-community-local"] | unique)
          else .enabledMcpjsonServers = ["7edge-community-local"]
        end
        | .enableAllProjectMcpServers = true' \
      "$SETTINGS_LOCAL" > "$SETTINGS_LOCAL.tmp" && mv "$SETTINGS_LOCAL.tmp" "$SETTINGS_LOCAL"
    echo "✓ Auto-patched .claude/settings.local.json"
  else
    echo "   jq not found — skipping auto-patch. Install with: sudo apt install jq (or brew install jq)"
    echo "   Then ensure .claude/settings.local.json contains:"
    echo '   "enabledMcpjsonServers": ["7edge-community-local"]'
  fi
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
  read -p "Your Discourse username: " DISCOURSE_USERNAME </dev/tty || true
  read -p "Your API key: " DISCOURSE_API_KEY </dev/tty || true
  echo ""

  if [ -z "$DISCOURSE_USERNAME" ] || [ -z "$DISCOURSE_API_KEY" ]; then
    echo "⚠  Skipped credentials setup (username or key was empty)."
    echo "   Create ~/.config/discourse/7edge-profile.json manually before publishing."
  else
    echo ""
    echo "Validating credentials..."
    RESP=$(curl -s -o /dev/null -w "%{http_code}" \
      -H "Api-Key: $DISCOURSE_API_KEY" \
      -H "Api-Username: $DISCOURSE_USERNAME" \
      "https://community.7edge.com/session/current.json")

    if [ "$RESP" != "200" ]; then
      echo "✗ Invalid credentials (HTTP $RESP). Check your API key and username, then try again."
      exit 1
    fi
    echo "✓ Credentials verified"

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
echo "✓ Installation complete!"
echo ""
echo "  ➜  Open Claude Code from: $(pwd)"
echo "     The skill will appear in /skills once you restart."
