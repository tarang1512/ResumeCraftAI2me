#!/bin/bash
# WhatsApp Voice Note Hook
# Usage: ./voice_hook.sh <audio_file> <sender_name>

cd /home/ubuntu/.openclaw/workspace
source Indic-TTS/venv311/bin/activate

AUDIO_FILE="$1"
SENDER="$2"

if [ -z "$AUDIO_FILE" ] || [ -z "$SENDER" ]; then
    echo "Usage: $0 <audio_file> <sender_name>"
    exit 1
fi

echo "🎙️ Processing voice note from $SENDER..."
python3 whatsapp_voice_handler.py "$AUDIO_FILE" "$SENDER"
