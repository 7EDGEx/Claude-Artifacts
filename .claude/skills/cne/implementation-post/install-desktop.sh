#!/usr/bin/env bash
set -e

# Detect OS and find Desktop config path
case "$OSTYPE" in
  darwin*)  CONFIG_DIR="$HOME/Library/Application Support/Claude" ;;
  linux*)   CONFIG_DIR="$HOME/.config/claude" ;;
  msys*|cygwin*) CONFIG_DIR="$APPDATA/Claude" ;;
  *)
    echo "Unknown OS: $OSTYPE"
    echo "Please manually set up your Claude Desktop config."
    exit 1
    ;;
esac

CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$CONFIG_DIR"

echo "Setting up Claude Desktop for implementation-post skill..."
echo ""

# Function to add MCP server entry
add_mcp_server() {
  local config_file="$1"

  # Check if mcpServers section exists
  if grep -q '"mcpServers"' "$config_file"; then
    # Check if 7edge-community-local already exists
    if grep -q '7edge-community-local' "$config_file"; then
      echo "✓ 7edge-community-local server already in config"
      return 0
    fi

    # Insert the server entry before the closing }
    sed -i '/"mcpServers"/,/^  }/s/^  }/    "7edge-community-local": {\n      "command": "npx",\n      "args": ["-y", "@discourse\/mcp@latest", "--profile", "${HOME}\/.config\/discourse\/7edge-profile.json"]\n    }\n  }/' "$config_file"
    echo "✓ Added 7edge-community-local server to existing mcpServers"
  else
    # Create the entire mcpServers block
    sed -i '/{/a\  "mcpServers": {\n    "7edge-community-local": {\n      "command": "npx",\n      "args": ["-y", "@discourse\/mcp@latest", "--profile", "${HOME}\/.config\/discourse\/7edge-profile.json"]\n    }\n  },' "$config_file"
    echo "✓ Created mcpServers block with 7edge-community-local"
  fi
}

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
else
  echo "Claude Desktop config exists: $CONFIG_FILE"
  echo ""
  echo "⚠  Manually add this to your mcpServers section (if not already present):"
  echo ""
  echo "    \"7edge-community-local\": {"
  echo "      \"command\": \"npx\","
  echo "      \"args\": [\"-y\", \"@discourse/mcp@latest\", \"--profile\", \"$PROFILE_PATH\"]"
  echo "    }"
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
echo "────────────────────────────────────────────────────────────────"
echo "Next step: Load the skill into Claude Desktop"
echo ""
echo "1. Open Claude Desktop"
echo "2. Create or open a Project"
echo "3. Go to Project Settings → Instructions (or Custom Instructions)"
echo "4. Paste the contents of:"
echo "   $SCRIPT_DIR/SKILL.md"
echo ""
echo "5. Save, then restart Claude Desktop"
echo "────────────────────────────────────────────────────────────────"
