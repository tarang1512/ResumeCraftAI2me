#!/bin/bash
# Stop voice note watcher

if [ -f voice_watcher.pid ]; then
    PID=$(cat voice_watcher.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        echo "Stopped voice watcher (PID: $PID)"
    else
        echo "Process not running"
    fi
    rm -f voice_watcher.pid
else
    echo "No PID file found, trying to find process..."
    pkill -f "voice_watcher.py" && echo "Stopped" || echo "Not running"
fi
