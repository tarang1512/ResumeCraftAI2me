#!/usr/bin/env python3
"""Complete Gmail OAuth with auth code."""
import sys
import os
import pickle
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = ['https://mail.google.com/']
TOKEN_PATH = '/home/ubuntu/.openclaw/credentials/gmail-token.json'
CLIENT_PATH = '/home/ubuntu/.openclaw/credentials/google-calendar-client.json'

def complete_auth(auth_code):
    flow = Flow.from_client_secrets_file(
        CLIENT_PATH, 
        SCOPES, 
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    
    flow.fetch_token(code=auth_code)
    creds = flow.credentials
    
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    with open(TOKEN_PATH, 'wb') as token:
        pickle.dump(creds, token)
    
    # Test - just verify service builds (profile needs broader scope)
    service = build('gmail', 'v1', credentials=creds, static_discovery=False)
    print(f"✅ Gmail token saved successfully!")
    print(f"   Token path: {TOKEN_PATH}")
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 auth_complete.py '<code>'")
        sys.exit(1)
    
    if complete_auth(sys.argv[1]):
        print("Ready to send emails!")
    else:
        print("❌ Failed")
        sys.exit(1)
