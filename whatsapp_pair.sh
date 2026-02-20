#!/bin/bash
cd /home/ubuntu/.openclaw/workspace
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 18

# Run pairing for 60 seconds
node whatsapp_bridge.js &
pid=$!

sleep 60
kill $pid 2>/dev/null

echo "Pairing window closed. Check if authenticated."
