#!/bin/bash
# backup_openclaw.sh - Full backup of OpenClaw workspace
# Usage: ./backup_openclaw.sh [optional_backup_name]

set -e

WORKSPACE="/home/ubuntu/.openclaw/workspace"
BACKUP_DIR="$HOME/openclaw_backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="${1:-openclaw_backup_$DATE}"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME.tar.gz"

echo "🦞 OpenClaw Backup Script"
echo "=========================="
echo ""

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "📦 Creating backup: $BACKUP_NAME"
echo "   Location: $BACKUP_PATH"
echo ""

# Create temp directory for organized backup
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo "📁 Collecting files..."

# Core identity files
cp "$WORKSPACE/AGENTS.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$WORKSPACE/SOUL.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$WORKSPACE/USER.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$WORKSPACE/USER_AVANI.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$WORKSPACE/IDENTITY.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$WORKSPACE/BOOTSTRAP.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$WORKSPACE/HEARTBEAT.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$WORKSPACE/TOOLS.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$WORKSPACE/MEMORY.md" "$TEMP_DIR/" 2>/dev/null || true

# Setup docs
cp "$WORKSPACE/VOICE_SETUP.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$WORKSPACE/VOICE_SETUP_FINAL.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$WORKSPACE/WEBHOOK_SETUP.md" "$TEMP_DIR/" 2>/dev/null || true

# Data files
cp "$WORKSPACE/gujarati_vocab.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$WORKSPACE/voice_conversations_demo.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$WORKSPACE/.voice_processed.json" "$TEMP_DIR/" 2>/dev/null || true

# Skills (full)
cp -r "$WORKSPACE/skills" "$TEMP_DIR/" 2>/dev/null || true

# Python scripts (main ones)
mkdir -p "$TEMP_DIR/scripts"
cp "$WORKSPACE/gujarati_stt.py" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/sarvam_stt.py" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/sarvam_tts.py" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/stt_translate_pipeline.py" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/command_processor.py" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/handle_voice_note.py" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/voice_processor.py" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/voice_auto_responder.py" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/voice_watcher.py" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/whatsapp_voice_handler.py" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/whatsapp_voice_processor.py" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/whatsapp_voice_daemon.py" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/whatsapp_voice_auto.py" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/whatsapp_bridge.js" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/whatsapp_qr.js" "$TEMP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE/check_pending_replies.py" "$TEMP_DIR/scripts/" 2>/dev/null || true

# Shell scripts
mkdir -p "$TEMP_DIR/shell"
cp "$WORKSPACE/install_voice_service.sh" "$TEMP_DIR/shell/" 2>/dev/null || true
cp "$WORKSPACE/run_voice_watcher.sh" "$TEMP_DIR/shell/" 2>/dev/null || true
cp "$WORKSPACE/stop_voice_watcher.sh" "$TEMP_DIR/shell/" 2>/dev/null || true
cp "$WORKSPACE/voice_hook.sh" "$TEMP_DIR/shell/" 2>/dev/null || true
cp "$WORKSPACE/setup_gujarati_tts.sh" "$TEMP_DIR/shell/" 2>/dev/null || true
cp "$WORKSPACE/setup_ocr.sh" "$TEMP_DIR/shell/" 2>/dev/null || true
cp "$WORKSPACE/setup_whatsapp.sh" "$TEMP_DIR/shell/" 2>/dev/null || true
cp "$WORKSPACE/tts_final_setup.sh" "$TEMP_DIR/shell/" 2>/dev/null || true
cp "$WORKSPACE/ocr_final_setup.sh" "$TEMP_DIR/shell/" 2>/dev/null || true
cp "$WORKSPACE/whatsapp_pair.sh" "$TEMP_DIR/shell/" 2>/dev/null || true

# Systemd service files
cp "$WORKSPACE/voice-watcher.service" "$TEMP_DIR/" 2>/dev/null || true

# OCR wrapper
cp "$WORKSPACE/ocr_wrapper.py" "$TEMP_DIR/scripts/" 2>/dev/null || true

# Memory directory
cp -r "$WORKSPACE/memory" "$TEMP_DIR/" 2>/dev/null || true

# RainbowBaby app
cp -r "$WORKSPACE/rainbow_baby_app" "$TEMP_DIR/" 2>/dev/null || true

# Package files (for npm dependencies)
cp "$WORKSPACE/package.json" "$TEMP_DIR/" 2>/dev/null || true
cp "$WORKSPACE/package-lock.json" "$TEMP_DIR/" 2>/dev/null || true

# Create backup manifest
cat > "$TEMP_DIR/BACKUP_MANIFEST.txt" << 'EOF'
OpenClaw Workspace Backup
==========================
Created: $(date)
Hostname: $(hostname)
User: $(whoami)

CONTENTS:
- Core identity files (SOUL.md, USER.md, etc.)
- Skills (talk2me/, ocr/)
- Python scripts (STT, TTS, voice handling)
- Shell scripts (setup, runners)
- Memory files (daily logs)
- RainbowBaby Flutter app
- Systemd service files

RESTORE:
Run ./restore_openclaw.sh from the extracted backup directory

IMPORTANT EXTERNAL DEPENDENCIES (not backed up):
- Indic-TTS (large, reinstall separately)
- Vosk models (large, reinstall separately)
- node_modules (restore via npm install)
- Conda environments
- API keys (in ~/.openclaw/agents/main/agent/auth-profiles.json)
EOF

# Create the tar.gz archive
tar -czf "$BACKUP_PATH" -C "$TEMP_DIR" .

# Create latest symlink
ln -sf "$BACKUP_PATH" "$BACKUP_DIR/openclaw_latest.tar.gz"

# Calculate size
SIZE=$(du -h "$BACKUP_PATH" | cut -f1)

echo ""
echo "✅ Backup complete!"
echo "   File: $BACKUP_PATH"
echo "   Size: $SIZE"
echo ""
echo "📂 Latest backup symlink: $BACKUP_DIR/openclaw_latest.tar.gz"
echo ""
echo "💡 To restore later, run:"
echo "   ./restore_openclaw.sh $BACKUP_PATH"
