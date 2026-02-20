#!/usr/bin/env python3
"""Gmail OAuth authentication flow."""
import os
import pickle
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Full Gmail access
SCOPES = ['https://mail.google.com/']
TOKEN_PATH = '/home/ubuntu/.openclaw/credentials/gmail-token.json'
CLIENT_PATH = '/home/ubuntu/.openclaw/credentials/google-calendar-client.json'

def authenticate():
    creds = None
    
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_PATH):
                print(f"ERROR: Client secrets not found at {CLIENT_PATH}")
                return None
            
            flow = Flow.from_client_secrets_file(
                CLIENT_PATH, 
                SCOPES, 
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'
            )
            auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
            
            print("\n" + "="*60)
            print("GMAIL AUTHORIZATION REQUIRED")
            print("="*60)
            print("\n1. Open this URL in your browser:")
            print(f"\n   {auth_url}\n")
            print("2. Sign in and authorize Gmail access")
            print("3. Copy the authorization code")
            print("4. Paste it here to complete setup")
            print("="*60 + "\n")
            return None
        
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_service():
    creds = authenticate()
    if not creds:
        return None
    return build('gmail', 'v1', credentials=creds, static_discovery=False)

if __name__ == '__main__':
    service = get_service()
    if service:
        print("✅ Gmail authenticated!")
    else:
        print("Waiting for auth code...")
