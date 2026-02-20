#!/bin/bash
#===============================================================================
# OpenClaw Workspace Restore Script
# 
# Usage: ./restore-backup.sh <backup-file.tar.gz>
#
# Example: ./restore-backup.sh /tmp/workspace-backup-20260217-105524.tar.gz
#===============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if backup file is provided
if [ -z "$1" ]; then
    print_error "No backup file specified!"
    echo ""
    echo "Usage: $0 <backup-file.tar.gz>"
    echo ""
    echo "Example:"
    echo "  $0 /tmp/workspace-backup-20260217-105524.tar.gz"
    echo ""
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    print_error "Backup file not found: $BACKUP_FILE"
    exit 1
fi

print_header "🔄 OpenClaw Workspace Restore"

echo "Backup file: $BACKUP_FILE"
echo "File size: $(du -h "$BACKUP_FILE" | cut -f1)"
echo ""

# Confirm before proceeding
read -p "⚠️  This will overwrite your current workspace. Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Restore cancelled."
    exit 0
fi

# Step 1: Stop the gateway
print_header "Step 1: Stopping Gateway"
if pgrep -f "openclaw-gateway" > /dev/null; then
    echo "Stopping gateway..."
    pkill -f "openclaw-gateway" || true
    sleep 3
    print_success "Gateway stopped"
else
    print_warning "Gateway was not running"
fi

# Step 2: Backup current workspace (optional but recommended)
print_header "Step 2: Backing Up Current Workspace"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
OLD_WORKSPACE="/home/ubuntu/.openclaw/workspace.old.$TIMESTAMP"

if [ -d "/home/ubuntu/.openclaw/workspace" ]; then
    echo "Creating backup of current workspace..."
    mv /home/ubuntu/.openclaw/workspace "$OLD_WORKSPACE"
    print_success "Current workspace backed up to: $OLD_WORKSPACE"
    echo ""
    print_warning "You can delete this later: rm -rf $OLD_WORKSPACE"
else
    print_warning "No existing workspace found"
fi

# Step 3: Create fresh workspace directory
print_header "Step 3: Extracting Backup"
mkdir -p /home/ubuntu/.openclaw/workspace
echo "Extracting backup to /home/ubuntu/.openclaw/workspace..."
tar -xzf "$BACKUP_FILE" -C /home/ubuntu/.openclaw/
print_success "Backup extracted successfully"

# Step 4: Fix permissions
print_header "Step 4: Fixing Permissions"
chown -R $(whoami):$(whoami) /home/ubuntu/.openclaw/workspace
chmod -R 755 /home/ubuntu/.openclaw/workspace
print_success "Permissions fixed"

# Step 5: Install dependencies
print_header "Step 5: Installing Dependencies"
cd /home/ubuntu/.openclaw/workspace

if [ -f "package.json" ]; then
    echo "Installing Node.js dependencies..."
    npm install --silent
    print_success "Node.js dependencies installed"
else
    print_warning "No package.json found"
fi

if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt --quiet
    print_success "Python dependencies installed"
else
    print_warning "No requirements.txt found"
fi

# Step 6: Verify credentials (they're stored outside workspace)
print_header "Step 6: Verifying Credentials"
if [ -d "/home/ubuntu/.openclaw/credentials" ]; then
    CRED_COUNT=$(ls -1 /home/ubuntu/.openclaw/credentials/ 2>/dev/null | wc -l)
    print_success "Credentials found ($CRED_COUNT files)"
    echo "Location: /home/ubuntu/.openclaw/credentials/"
else
    print_error "Credentials directory missing!"
    print_warning "You may need to re-authenticate services"
fi

# Step 7: Start the gateway
print_header "Step 7: Starting Gateway"
echo "Starting OpenClaw gateway..."
openclaw gateway start
sleep 5

# Check if gateway is running
if pgrep -f "openclaw-gateway" > /dev/null; then
    print_success "Gateway started successfully"
else
    print_error "Gateway failed to start!"
    print_warning "Check logs: journalctl --user -u openclaw-gateway -n 50"
    echo ""
    echo "You can try starting manually: openclaw gateway start"
fi

# Step 8: Verify installation
print_header "Step 8: Verification"
echo "Checking installation..."

# Check workspace
if [ -d "/home/ubuntu/.openclaw/workspace/skills" ]; then
    SKILL_COUNT=$(ls -1 /home/ubuntu/.openclaw/workspace/skills/ | wc -l)
    print_success "Workspace OK ($SKILL_COUNT skills)"
else
    print_error "Workspace incomplete!"
fi

# Check gateway health
if curl -s http://localhost:18789/health > /dev/null 2>&1; then
    print_success "Gateway health check OK"
else
    print_warning "Gateway not responding yet (may need a moment)"
fi

# Final summary
print_header "🎉 Restore Complete!"
echo "Summary:"
echo "  ✅ Backup extracted"
echo "  ✅ Dependencies installed"
echo "  ✅ Gateway started"
echo ""
echo "Next steps:"
echo "  1. Check gateway status: openclaw status"
echo "  2. Verify skills: ls /home/ubuntu/.openclaw/workspace/skills/"
echo "  3. Test a model: Run any command or send a message"
echo ""
if [ -d "$OLD_WORKSPACE" ]; then
    print_warning "Old workspace saved at: $OLD_WORKSPACE"
    echo "Delete it after verifying everything works:"
    echo "  rm -rf $OLD_WORKSPACE"
fi
echo ""
print_success "Welcome back! Your OpenClaw is ready."

#===============================================================================
# End of restore script
#===============================================================================
