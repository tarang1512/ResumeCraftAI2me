#!/bin/bash
# setup_new_device.sh - Full OpenClaw setup on a new device
# Usage: ./setup_new_device.sh [path/to/backup.tar.gz]

set -e

BACKUP_FILE="${1:-openclaw_backup_latest.tar.gz}"
WORKSPACE_DIR="$HOME/.openclaw/workspace"

echo "🦞 OpenClaw New Device Setup"
echo "============================"
echo ""

# Check if backup exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Error: Backup file not found: $BACKUP_FILE"
    echo ""
    echo "Usage: $0 [path/to/backup.tar.gz]"
    echo ""
    echo "Place your backup file in this directory and run again."
    exit 1
fi

echo "📦 Using backup: $BACKUP_FILE"
echo ""

# Step 1: Install dependencies
echo "🔧 Step 1: Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    # Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install -y nodejs npm python3 python3-pip ffmpeg git curl
elif command -v brew &> /dev/null; then
    # macOS
    brew install node python ffmpeg git curl
elif command -v yum &> /dev/null; then
    # RHEL/CentOS/Fedora
    sudo yum install -y nodejs npm python3 python3-pip ffmpeg git curl
else
    echo "⚠️  Could not detect package manager. Please install manually:"
    echo "   - Node.js + npm"
    echo "   - Python 3 + pip"
    echo "   - ffmpeg"
    echo "   - git"
    echo "   - curl"
    read -p "Press Enter when ready to continue..."
fi
echo "✓ Dependencies installed"
echo ""

# Step 2: Install OpenClaw
echo "🔧 Step 2: Installing OpenClaw..."
if command -v openclaw &> /dev/null; then
    echo "✓ OpenClaw already installed: $(openclaw --version)"
else
    npm install -g openclaw
    echo "✓ OpenClaw installed"
fi
echo ""

# Step 3: Create workspace directory
echo "🔧 Step 3: Setting up workspace..."
mkdir -p "$WORKSPACE_DIR"
cd "$WORKSPACE_DIR"
echo "✓ Workspace directory created: $WORKSPACE_DIR"
echo ""

# Step 4: Extract backup
echo "🔧 Step 4: Restoring backup..."
tar -xzf "$BACKUP_FILE" -C "$WORKSPACE_DIR"
echo "✓ Backup restored to: $WORKSPACE_DIR"
echo ""

# Step 5: Install npm dependencies
echo "🔧 Step 5: Installing Node.js dependencies..."
if [ -f "$WORKSPACE_DIR/package.json" ]; then
    cd "$WORKSPACE_DIR"
    npm install
    echo "✓ Node modules installed"
else
    echo "⚠️  No package.json found, skipping npm install"
fi
echo ""

# Step 6: Make scripts executable
echo "🔧 Step 6: Setting permissions..."
chmod +x "$WORKSPACE_DIR/"*.sh 2>/dev/null || true
chmod +x "$WORKSPACE_DIR/"*.py 2>/dev/null || true
chmod +x "$WORKSPACE_DIR/skills/"*/*.py 2>/dev/null || true
echo "✓ Scripts made executable"
echo ""

# Step 7: Check for large dependencies
echo "🔧 Step 7: Checking for large dependencies..."
MISSING_DEPS=()

if [ ! -d "$WORKSPACE_DIR/Indic-TTS" ]; then
    MISSING_DEPS+=("Indic-TTS")
fi

if [ ! -d "$WORKSPACE_DIR/vosk_models" ]; then
    MISSING_DEPS+=("Vosk models")
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "⚠️  Missing large dependencies (must install manually):"
    for dep in "${MISSING_DEPS[@]}"; do
        echo "   - $dep"
    done
    echo ""
    echo "Install commands:"
    echo ""
    if [[ " ${MISSING_DEPS[@]} " =~ "Indic-TTS" ]]; then
        echo "  # Indic-TTS (~4GB)"
        echo "  cd $WORKSPACE_DIR"
        echo "  git clone https://github.com/AI4Bharat/Indic-TTS"
        echo "  cd Indic-TTS"
        echo "  pip install -e ."
        echo "  # Download Gujarati models from AI4Bharat releases"
        echo ""
    fi
    if [[ " ${MISSING_DEPS[@]} " =~ "Vosk" ]]; then
        echo "  # Vosk Gujarati Model (~1.9GB)"
        echo "  mkdir -p $WORKSPACE_DIR/vosk_models"
        echo "  cd $WORKSPACE_DIR/vosk_models"
        echo "  wget https://alphacephei.com/vosk/models/vosk-model-gu-0.42.zip"
        echo "  unzip vosk-model-gu-0.42.zip"
        echo "  mv vosk-model-gu-0.42 gujarati"
        echo ""
    fi
else
    echo "✓ All large dependencies present"
fi
echo ""

# Step 8: Setup Python virtual environment (optional but recommended)
echo "🔧 Step 8: Setting up Python environment..."
if command -v python3 &> /dev/null; then
    pip3 install --user requests numpy soundfile scipy pyyaml 2>/dev/null || true
    echo "✓ Python packages installed"
else
    echo "⚠️  Python3 not found"
fi
echo ""

# Step 9: Summary
echo "🎉 SETUP COMPLETE!"
echo "=================="
echo ""
echo "📂 Workspace location: $WORKSPACE_DIR"
echo ""
echo "⚠️  MANUAL STEPS REQUIRED:"
echo ""
echo "1. Add API keys:"
echo "   openclaw agents add nvidia-nim"
echo "   openclaw agents add openrouter"
echo "   openclaw agents add moonshot"
echo "   # (and any others you use)"
echo ""
echo "2. Install large dependencies (if not done above):"
echo "   - Indic-TTS (~4GB)"
echo "   - Vosk Gujarati model (~1.9GB)"
echo ""
echo "3. Configure WhatsApp (if needed):"
echo "   openclaw channels add whatsapp"
echo ""
echo "4. Start the gateway:"
echo "   openclaw gateway start"
echo ""
echo "5. Open the dashboard:"
echo "   openclaw tui"
echo "   # or"
echo "   openclaw web"
echo ""
echo "🦞 You're ready to go!"
echo ""

# Create a quick reference file
cat > "$WORKSPACE_DIR/QUICKSTART.md" << 'EOF'
# OpenClaw Quickstart (New Device)

## Start Everything
```bash
openclaw gateway start  # Start the gateway
openclaw tui            # Open TUI dashboard
```

## Common Commands
```bash
openclaw status                    # Check status
openclaw cron list                 # List cron jobs
openclaw agents list               # List configured agents
openclaw channels list             # List connected channels
```

## File Locations
- Workspace: ~/.openclaw/workspace/
- Config: ~/.openclaw/
- Logs: ~/.openclaw/logs/

## Backup/Restore
```bash
# Create backup
./backup_openclaw.sh

# Restore backup
./restore_openclaw.sh backup_file.tar.gz
```
EOF

echo "📖 Quick reference saved to: $WORKSPACE_DIR/QUICKSTART.md"
