#!/usr/bin/env python3
"""Create calendar events/reminders."""
import argparse
import sys
import os
import pickle
from datetime import datetime, timedelta
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
            print("ERROR: Not authenticated")
            return None
    
    return build('calendar', 'v3', credentials=creds, static_discovery=False)

def create_event(summary, start_time, end_time=None, description='', calendar_id='primary'):
    service = get_service()
    if not service:
        return None
    
    if not end_time:
        end_time = start_time + timedelta(minutes=30)
    
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/New_York'
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/New_York'
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10}
            ]
        }
    }
    
    try:
        result = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"✅ Event created: {result.get('htmlLink')}")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--summary', required=True)
    parser.add_argument('--start', required=True, help='ISO datetime')
    parser.add_argument('--end', help='ISO datetime')
    parser.add_argument('--description', default='')
    args = parser.parse_args()
    
    start = datetime.fromisoformat(args.start)
    end = datetime.fromisoformat(args.end) if args.end else None
    
    create_event(args.summary, start, end, args.description)
