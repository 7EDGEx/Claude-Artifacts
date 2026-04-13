#!/usr/bin/env bash
set -e

# ────────────────────────────────────────────────────────────────────────────
# 🎯 UNIFIED INSTALLATION GUIDE
# ────────────────────────────────────────────────────────────────────────────
#
# This script installs the implementation-post skill for EITHER:
#   - Claude Code (CLI, Web, IDE extensions)
#   - Claude Desktop (native Mac/Windows/Linux app)
#
# ────────────────────────────────────────────────────────────────────────────

echo ""
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║         Implementation-Post Skill Installation                         ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Which version are you installing for?"
echo ""
echo "  1) Claude Code (CLI, Web app, IDE extensions)"
echo "  2) Claude Desktop (native Mac/Windows/Linux app)"
echo ""
read -p "Enter 1 or 2: " PLATFORM_CHOICE </dev/tty || true

case "$PLATFORM_CHOICE" in
  1)
    echo ""
    echo "Installing for Claude Code..."
    PLATFORM="code"
    ;;
  2)
    echo ""
    echo "Installing for Claude Desktop..."
    PLATFORM="desktop"
    ;;
  *)
    echo "Invalid choice. Exiting."
    exit 1
    ;;
esac

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_URL="https://raw.githubusercontent.com/Khaleelibrahimofficial/Claude-Artifacts/implementation-post-local-mcp/.claude/skills/cne/implementation-post"

# ── helper: check if jq is available ────────────────────────────────────────
has_jq() { command -v jq &>/dev/null; }

# ────────────────────────────────────────────────────────────────────────────
# CLAUDE CODE INSTALLATION
# ────────────────────────────────────────────────────────────────────────────
if [ "$PLATFORM" = "code" ]; then

TARGET_DIR="$(pwd)"

# ── Detect installation mode ────────────────────────────────────────────────
if [ "$TARGET_DIR" = "$HOME" ]; then
  INSTALL_MODE="global"
  CONFIG_DIR="$HOME/.claude"
  SETTINGS_LOCAL="$CONFIG_DIR/settings.local.json"
  echo "🌍 Global installation detected (running from home directory)"
  echo "   Config will be installed to: $HOME/.claude/"
  echo ""
  echo "   This will apply to ALL projects when using Claude Code"
  echo ""
else
  INSTALL_MODE="project"
  CONFIG_DIR="$TARGET_DIR/.claude"
  SETTINGS_LOCAL="$CONFIG_DIR/settings.local.json"
  echo "📁 Project installation detected (running from project directory)"
  echo "   Config will be installed to: $TARGET_DIR/.claude/"
  echo ""
  echo "   This will only apply to this project when using Claude Code"
  echo ""
fi

read -p "Continue with $INSTALL_MODE installation? [Y/n]: " CONFIRM </dev/tty || true
CONFIRM="${CONFIRM:-Y}"
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
  echo "Installation cancelled."
  exit 0
fi

echo ""
echo "Installing implementation-post skill..."

# 1. Copy or download skill files
mkdir -p "$TARGET_DIR/.claude/skills/implementation-post"

if [ -f "$SCRIPT_DIR/SKILL.md" ]; then
  cp "$SCRIPT_DIR/SKILL.md" "$TARGET_DIR/.claude/skills/implementation-post/SKILL.md"
  cp "$SCRIPT_DIR/SETUP.md" "$TARGET_DIR/.claude/skills/implementation-post/SETUP.md"
  echo "✓ Skill files copied to .claude/skills/implementation-post/"
else
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
mkdir -p "$CONFIG_DIR"
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

if [ "$INSTALL_MODE" = "global" ]; then
  echo "  🌍 GLOBAL INSTALLATION"
  echo "     The skill is now available to all projects."
  echo ""
  echo "  Next steps:"
  echo "    1. Restart Claude Code"
  echo "    2. Open any project — the implementation-post skill will appear in /skills"
  echo ""
else
  echo "  📁 PROJECT INSTALLATION"
  echo "     The skill is only available in: $TARGET_DIR"
  echo ""
  echo "  Next steps:"
  echo "    1. Open Claude Code from this directory:"
  echo "       cd $TARGET_DIR && code ."
  echo "    2. Or restart if already open — the skill will appear in /skills"
  echo ""
fi

echo "  ℹ️  Configuration saved to: $([ "$INSTALL_MODE" = "global" ] && echo "$HOME/.claude" || echo "$TARGET_DIR/.claude")"

# ────────────────────────────────────────────────────────────────────────────
# CLAUDE DESKTOP INSTALLATION
# ────────────────────────────────────────────────────────────────────────────
else

# Detect OS and find Desktop config path
case "$OSTYPE" in
  darwin*)
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
    OS_NAME="macOS"
    ;;
  linux*)
    CONFIG_DIR="$HOME/.config/claude"
    OS_NAME="Linux"
    ;;
  msys*|cygwin*|mingw*)
    CONFIG_DIR="$APPDATA/Claude"
    OS_NAME="Windows"
    ;;
  *)
    echo "Unknown OS: $OSTYPE"
    echo "Please manually set up your Claude Desktop config."
    exit 1
    ;;
esac

CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"
mkdir -p "$CONFIG_DIR"

echo "Detected OS: $OS_NAME"
echo "Config path: $CONFIG_FILE"
echo ""

# Create or update the config file
PROFILE_PATH="$HOME/.config/discourse/7edge-profile.json"

if [ ! -f "$CONFIG_FILE" ]; then
  cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "7edge-community-local": {
      "command": "npx",
      "args": ["-y", "@discourse/mcp@latest", "--profile", "$PROFILE_PATH"]
    }
  }
}
EOF
  echo "✓ Created Claude Desktop config: $CONFIG_FILE"
elif grep -q "7edge-community-local" "$CONFIG_FILE"; then
  echo "✓ 7edge-community-local already in config"
else
  echo "⚠  Claude Desktop config exists but is missing 7edge-community-local."
  if has_jq; then
    jq '.mcpServers["7edge-community-local"] = {
      "command": "npx",
      "args": ["-y", "@discourse/mcp@latest", "--profile", "'$PROFILE_PATH'"]
    }' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    echo "✓ Auto-patched config with 7edge-community-local"
  else
    echo "   jq not found — please manually add this to mcpServers in:"
    echo "   $CONFIG_FILE"
    echo ""
    echo "    \"7edge-community-local\": {"
    echo "      \"command\": \"npx\","
    echo "      \"args\": [\"-y\", \"@discourse/mcp@latest\", \"--profile\", \"$PROFILE_PATH\"]"
    echo "    }"
  fi
fi

# Set up credentials
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
echo "  🖥️  CLAUDE DESKTOP INSTALLATION"
echo "     MCP server is configured in: $CONFIG_FILE"
echo ""
echo "  Next steps:"
echo "    1. Restart Claude Desktop"
echo "    2. Open or create a project"
echo "    3. Go to Project Settings → Instructions"
echo "    4. Copy and paste the contents of SKILL.md"
echo "    5. Save and restart Claude Desktop"
echo ""
echo "  ℹ️  Config saved to: $CONFIG_FILE"

fi

echo ""
