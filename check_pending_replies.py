#!/usr/bin/env python3
"""
Check and send pending voice note replies
Run this manually or via cron to send queued replies
"""

import json
import os
from pathlib import Path

PENDING_FILE = Path("/home/ubuntu/.openclaw/workspace/.pending_reply.json")

def check_and_clear():
    """Check for pending reply, return it and clear"""
    if not PENDING_FILE.exists():
        return None
    
    try:
        with open(PENDING_FILE) as f:
            data = json.load(f)
        # Clear after reading
        os.remove(PENDING_FILE)
        return data
    except Exception as e:
        print(f"Error reading pending reply: {e}")
        return None

def main():
    """CLI entry point"""
    reply = check_and_clear()
    if reply:
        print(f"TO: {reply.get('to')}")
        print(f"MESSAGE: {reply.get('message')}")
        print(f"FROM_GUJARATI: {reply.get('gujarati')}")
        print(f"TRANSLATION: {reply.get('english')}")
        return reply
    else:
        print("NO_REPLY")
        return None

if __name__ == '__main__':
    main()
