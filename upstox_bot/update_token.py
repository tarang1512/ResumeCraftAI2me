#!/usr/bin/env python3
"""
Quick Upstox Token Updater
Just paste your new access token and this updates the .env file
"""

import os
import re
from datetime import datetime, timedelta

def update_token():
    print("=" * 60)
    print("UPSTOX TOKEN UPDATER")
    print("=" * 60)
    print()
    print("Paste your new Upstox access token below:")
    print("(Token looks like: eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4w...)")
    print()
    
    new_token = input("Token: ").strip()
    
    if not new_token:
        print("❌ No token provided. Exiting.")
        return
    
    if not new_token.startswith("eyJ"):
        print("⚠️ Warning: Token doesn't look like a JWT. Continue anyway? (y/n)")
        if input().lower() != 'y':
            return
    
    # Update .env file
    env_path = '/home/ubuntu/.openclaw/workspace/config/.env'
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Replace the access token
        new_content = re.sub(
            r'UPSTOX_ACCESS_TOKEN=.*',
            f'UPSTOX_ACCESS_TOKEN={new_token}',
            content
        )
        
        with open(env_path, 'w') as f:
            f.write(new_content)
        
        print()
        print("=" * 60)
        print("✅ TOKEN UPDATED SUCCESSFULLY")
        print("=" * 60)
        print(f"File: {env_path}")
        
        # Extract expiry if possible
        if '.' in new_token:
            try:
                import base64
                payload = new_token.split('.')[1]
                payload += '=' * (4 - len(payload) % 4)
                decoded = base64.b64decode(payload)
                import json
                data = json.loads(decoded)
                exp = data.get('exp')
                if exp:
                    from datetime import datetime
                    expiry = datetime.fromtimestamp(exp)
                    print(f"Token expires: {expiry.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                    print(f"Time remaining: {expiry - datetime.now()}")
            except:
                pass
        
        print()
        print("Next steps:")
        print("1. Test connection: openclaw gateway status")
        print("2. Check bot: openclaw trading-bot status")
        
    except Exception as e:
        print(f"❌ Error updating token: {e}")

if __name__ == "__main__":
    update_token()
