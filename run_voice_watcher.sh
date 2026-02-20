#!/bin/bash
# Run voice note watcher in background

cd /home/ubuntu/.openclaw/workspace
echo "Starting voice note watcher..."
source Indic-TTS/venv311/bin/activate

# Run with nohup to survive terminal close
nohup python3 voice_watcher.py > voice_watcher.log 2>&1 &

PID=$!
echo "Voice watcher started (PID: $PID)"
echo $PID > voice_watcher.pid
echo "Log: voice_watcher.log"
echo "Output will appear here when voice notes arrive"
