#!/bin/bash
# restore_openclaw.sh - Restore OpenClaw workspace from backup
# Usage: ./restore_openclaw.sh [backup_file.tar.gz]

set -e

WORKSPACE="/home/ubuntu/.openclaw/workspace"
BACKUP_FILE="${1:-$HOME/openclaw_backups/openclaw_latest.tar.gz}"

echo "🦞 OpenClaw Restore Script"
echo "=========================="
echo ""

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Error: Backup file not found: $BACKUP_FILE"
    echo ""
    echo "Usage: $0 [path/to/backup.tar.gz]"
    echo ""
    echo "Available backups:"
    ls -lh ~/openclaw_backups/*.tar.gz 2>/dev/null || echo "   (none found in ~/openclaw_backups/)"
    exit 1
fi

echo "📦 Restoring from: $BACKUP_FILE"
echo "   Target: $WORKSPACE"
echo ""

# Confirm
read -p "⚠️  This will OVERWRITE existing files. Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Create temp directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo ""
echo "📁 Extracting backup..."
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

echo "📂 Restoring files..."

# Core identity files
for file in AGENTS.md SOUL.md USER.md USER_AVANI.md IDENTITY.md BOOTSTRAP.md HEARTBEAT.md TOOLS.md MEMORY.md; do
    if [ -f "$TEMP_DIR/$file" ]; then
        cp "$TEMP_DIR/$file" "$WORKSPACE/"
        echo "  ✓ $file"
    fi
done

# Setup docs
for file in VOICE_SETUP.md VOICE_SETUP_FINAL.md WEBHOOK_SETUP.md; do
    if [ -f "$TEMP_DIR/$file" ]; then
        cp "$TEMP_DIR/$file" "$WORKSPACE/"
        echo "  ✓ $file"
    fi
done

# Data files
for file in gujarati_vocab.md voice_conversations_demo.md .voice_processed.json; do
    if [ -f "$TEMP_DIR/$file" ]; then
        cp "$TEMP_DIR/$file" "$WORKSPACE/"
        echo "  ✓ $file"
    fi
done

# Skills
if [ -d "$TEMP_DIR/skills" ]; then
    cp -r "$TEMP_DIR/skills/"* "$WORKSPACE/skills/" 2>/dev/null || true
    echo "  ✓ Skills restored"
fi

# Scripts
if [ -d "$TEMP_DIR/scripts" ]; then
    cp "$TEMP_DIR/scripts/"*.py "$WORKSPACE/" 2>/dev/null || true
    cp "$TEMP_DIR/scripts/"*.js "$WORKSPACE/" 2>/dev/null || true
    echo "  ✓ Python/JS scripts restored"
fi

# Shell scripts
if [ -d "$TEMP_DIR/shell" ]; then
    cp "$TEMP_DIR/shell/"*.sh "$WORKSPACE/" 2>/dev/null || true
    chmod +x "$WORKSPACE/"*.sh 2>/dev/null || true
    echo "  ✓ Shell scripts restored"
fi

# Service files
if [ -f "$TEMP_DIR/voice-watcher.service" ]; then
    cp "$TEMP_DIR/voice-watcher.service" "$WORKSPACE/"
    echo "  ✓ voice-watcher.service"
fi

# Memory directory
if [ -d "$TEMP_DIR/memory" ]; then
    rm -rf "$WORKSPACE/memory"
    cp -r "$TEMP_DIR/memory" "$WORKSPACE/"
    echo "  ✓ Memory directory restored"
fi

# RainbowBaby app
if [ -d "$TEMP_DIR/rainbow_baby_app" ]; then
    rm -rf "$WORKSPACE/rainbow_baby_app"
    cp -r "$TEMP_DIR/rainbow_baby_app" "$WORKSPACE/"
    echo "  ✓ RainbowBaby app restored"
fi

# Package files
for file in package.json package-lock.json; do
    if [ -f "$TEMP_DIR/$file" ]; then
        cp "$TEMP_DIR/$file" "$WORKSPACE/"
        echo "  ✓ $file"
    fi
done

echo ""
echo "✅ Restore complete!"
echo ""
echo "📋 POST-RESTORE CHECKLIST:"
echo "   ☐ Reinstall npm dependencies: cd $WORKSPACE && npm install"
echo "   ☐ Verify Indic-TTS is at: $WORKSPACE/Indic-TTS/"
echo "   ☐ Verify Vosk models at: $WORKSPACE/vosk_models/"
echo "   ☐ Check API keys in: ~/.openclaw/agents/main/agent/auth-profiles.json"
echo "   ☐ Restart OpenClaw gateway: openclaw gateway restart"
echo "   ☐ Make scripts executable: chmod +x $WORKSPACE/*.py $WORKSPACE/*.sh"
echo ""
echo "🦞 You're ready to go!"
