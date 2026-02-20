#!/usr/bin/env python3
"""Direct test without module imports"""
import os
import sys
import json
import requests

# Load .env manually
env_path = '/home/ubuntu/.openclaw/workspace/config/.env'
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ[key] = value

ACCESS_TOKEN = os.environ.get('UPSTOX_ACCESS_TOKEN')
ENVIRONMENT = os.environ.get('UPSTOX_ENVIRONMENT', 'production')

BASE_URL = "https://api.upstox.com/v2" if ENVIRONMENT == "production" else "https://api.sandbox.upstox.com/v2"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json",
    "Api-Version": "2.0"
}

print(f"Base URL: {BASE_URL}")
print(f"Testing Upstox API v2...")

endpoints = [
    "/user/profile",
    "/user/get-funds-and-margin",
    "/portfolio/long-term-holdings",
    "/portfolio/short-term-holdings",
    "/portfolio/positions",
]

for endpoint in endpoints:
    print(f"\n--- Test: {endpoint} ---")
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success: {json.dumps(data, indent=2)[:500]}")
        elif response.status_code == 401:
            print(f"✗ Unauthorized: Token might be expired or invalid")
            print(f"Response: {response.text[:200]}")
        else:
            print(f"✗ Failed: {response.text[:300]}")
    except Exception as e:
        print(f"✗ Error: {e}")
