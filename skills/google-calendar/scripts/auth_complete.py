#!/usr/bin/env python3
"""Complete OAuth flow with authorization code from user."""
import sys
import os
import pickle
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_PATH = '/home/ubuntu/.openclaw/credentials/google-calendar-token.json'
CLIENT_PATH = '/home/ubuntu/.openclaw/credentials/google-calendar-client.json'

def complete_auth(auth_code):
    flow = Flow.from_client_secrets_file(
        CLIENT_PATH, 
        SCOPES, 
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    
    flow.fetch_token(code=auth_code)
    creds = flow.credentials
    
    # Save token
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    with open(TOKEN_PATH, 'wb') as token:
        pickle.dump(creds, token)
    
    # Test
    service = build('calendar', 'v3', credentials=creds, static_discovery=False)
    calendars = service.calendarList().list().execute()
    print(f"✅ Authentication successful! Found {len(calendars.get('items', []))} calendars")
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 auth_complete.py '<authorization-code>'")
        sys.exit(1)
    
    auth_code = sys.argv[1]
    if complete_auth(auth_code):
        print("\nYou can now use the Google Calendar skill!")
    else:
        print("❌ Authentication failed")
        sys.exit(1)
