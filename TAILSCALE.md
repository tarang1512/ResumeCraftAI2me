# Tailscale Setup for OpenClaw

## Status
- Tailscale version: 1.94.2
- Node: AWS Ubuntu instance (ip-172-31-94-103)

## Login Required
**Auth URL:** https://login.tailscale.com/a/5aa45c039b946

## How to Connect

### Step 1: Authenticate AWS Node
1. Open the auth URL above in your browser
2. Login with your Tailscale account
3. Approve the node

### Step 2: Connect Your Mac
1. Install Tailscale: `brew install tailscale`
2. Run: `tailscale up`
3. Login with same account

### Step 3: Done!
- Your Mac will have direct access to AWS
- No need for public IPs or firewall rules
- Use `tailscale ip` to find the internal IP

## Notes
- Generated: 2026-02-18
- For OpenClaw cross-device sync

