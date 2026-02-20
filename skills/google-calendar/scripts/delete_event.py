#!/usr/bin/env python3
"""Delete calendar events."""
import os
import sys
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH = '/home/ubuntu/.openclaw/credentials/google-calendar-token.json'

def get_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
        else:
            return None
    
    return build('calendar', 'v3', credentials=creds, static_discovery=False)

def delete_event(event_id, calendar_id='primary'):
    service = get_service()
    if not service:
        return False
    
    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        print(f"✅ Event deleted")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', required=True, help='Event ID')
    args = parser.parse_args()
    
    delete_event(args.id)
