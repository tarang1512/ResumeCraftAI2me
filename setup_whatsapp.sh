#!/bin/bash
set -e

echo "Installing WhatsApp (zca-cli) plugin..."

# Install required dependencies
sudo apt-get update -qq
sudo apt-get install -y -qq curl git

# Install nvm and Node.js
export NVM_DIR="$HOME/.nvm"
if [ ! -d "$NVM_DIR" ]; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
fi
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install Node 18 (LTS stable for whatsapp-web.js)
nvm install 18
nvm use 18

# Install zca-cli globally
npm install -g @openclaw/zca-cli

echo "WhatsApp plugin installed! Next step: run 'zca login' and scan QR code"
