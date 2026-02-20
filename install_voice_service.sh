#!/bin/bash
# Install voice watcher as systemd service

SERVICE_NAME="voice-watcher"
SERVICE_FILE="/home/ubuntu/.openclaw/workspace/voice-watcher.service"
USER_SERVICE_DIR="$HOME/.config/systemd/user"

echo "Installing voice watcher service..."

# Create user systemd directory if not exists
mkdir -p "$USER_SERVICE_DIR"

# Copy service file
cp "$SERVICE_FILE" "$USER_SERVICE_DIR/"

# Reload systemd
systemctl --user daemon-reload

# Enable service (auto-start on boot)
systemctl --user enable "$SERVICE_NAME"

# Start service now
systemctl --user start "$SERVICE_NAME"

echo "✅ Voice watcher service installed and started!"
echo ""
echo "Commands:"
echo "  systemctl --user status $SERVICE_NAME  # Check status"
echo "  systemctl --user stop $SERVICE_NAME    # Stop"
echo "  systemctl --user start $SERVICE_NAME   # Start"
echo "  systemctl --user restart $SERVICE_NAME # Restart"
echo ""
echo "Logs: tail -f /home/ubuntu/.openclaw/workspace/voice_watcher.log"
