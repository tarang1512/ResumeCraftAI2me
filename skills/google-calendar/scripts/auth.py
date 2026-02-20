#!/usr/bin/env python3
"""Google Calendar OAuth authentication flow."""
import os
import json
import pickle
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_PATH = '/home/ubuntu/.openclaw/credentials/google-calendar-token.json'
CLIENT_PATH = '/home/ubuntu/.openclaw/credentials/google-calendar-client.json'

def authenticate():
    creds = None
    
    # Load existing token
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh or create new
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_PATH):
                print(f"ERROR: Client secrets not found at {CLIENT_PATH}")
                print("Download from Google Cloud Console and save there.")
                return None
            
            # Headless flow - print URL for user to open
            flow = Flow.from_client_secrets_file(CLIENT_PATH, SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
            auth_url, _ = flow.authorization_url(prompt='consent')
            
            print("\n" + "="*60)
            print("GOOGLE CALENDAR AUTHENTICATION REQUIRED")
            print("="*60)
            print("\n1. Open this URL in your browser:")
            print(f"\n   {auth_url}\n")
            print("2. Sign in and authorize access")
            print("3. Copy the authorization code")
            print("4. Run: python3 auth_complete.py '<paste-code-here>'")
            print("="*60 + "\n")
            return None
        
        # Save token
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_service():
    creds = authenticate()
    if not creds:
        return None
    return build('calendar', 'v3', credentials=creds, static_discovery=False)

if __name__ == '__main__':
    service = get_service()
    if service:
        print("✅ Authentication successful!")
        # Test by listing calendars
        calendars = service.calendarList().list().execute()
        print(f"Found {len(calendars.get('items', []))} calendars")
    else:
        print("❌ Authentication failed")
        exit(1)
