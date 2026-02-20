#!/bin/bash
# Gateway Restart Notification Script
# Sends a message to the last active chat when gateway restarts

RESTART_FLAG="/tmp/openclaw-restart-notify"
LAST_CHAT_FLAG="/tmp/openclaw-last-chat"

# Check if this is a fresh restart (flag file doesn't exist)
if [ ! -f "$RESTART_FLAG" ]; then
    # Create the flag to prevent duplicate notifications
    touch "$RESTART_FLAG"
    
    # Wait for gateway to be ready
    sleep 3
    
    # Send restart notification via Telegram
    # The message will be picked up by the next heartbeat
    echo "Gateway restarted at $(date)" > /tmp/openclaw-restart-message
    
    # Optional: Could send directly via Telegram API if needed
    # For now, rely on heartbeat to pick up the restart status
fi

exit 0
