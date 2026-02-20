#!/usr/bin/env python3
"""Quick test to verify Upstox API connection"""
import sys
sys.path.insert(0, '/home/ubuntu/.openclaw/workspace')

from upstox_bot.auth import UpstoxAuth
from upstox_bot.api_client import UpstoxClient
from upstox_bot.logger import get_logger

logger = get_logger(__name__)

def test_connection():
    print("Testing Upstox API connection...")
    
    # Initialize auth (will load from .env)
    auth = UpstoxAuth()
    
    print(f"API Key: {auth.api_key[:10]}...")
    print(f"Environment: {auth.environment}")
    print(f"Access Token: {auth.access_token[:50]}..." if auth.access_token else "No token")
    
    # Create client
    client = UpstoxClient(auth, environment=auth.environment)
    
    # Test 1: Get user profile
    print("\n--- Test 1: Get User Profile ---")
    try:
        profile = client.get("/user/profile")
        print(f"✓ Success! User: {profile}")
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    # Test 2: Get holdings
    print("\n--- Test 2: Get Holdings ---")
    try:
        holdings = client.get("/portfolio/holdings")
        print(f"✓ Success! Holdings: {holdings}")
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    # Test 3: Get positions
    print("\n--- Test 3: Get Positions ---")
    try:
        positions = client.get("/portfolio/positions")
        print(f"✓ Success! Positions: {positions}")
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    print("\nDone.")

if __name__ == "__main__":
    test_connection()
