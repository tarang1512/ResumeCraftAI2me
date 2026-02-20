#!/usr/bin/env python3
"""Get the next upcoming event."""
import sys
from auth import get_service

def get_next_event(calendar_id='primary'):
    service = get_service()
    if not service:
        print("ERROR: Not authenticated", file=sys.stderr)
        return None
    
    from datetime import datetime
    now = datetime.utcnow().isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=1,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    return events[0] if events else None

if __name__ == '__main__':
    event = get_next_event()
    if event:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'No title')
        location = event.get('location', '')
        event_id = event['id']
        
        print(f"Next: {summary}")
        print(f"Start: {start}")
        if location:
            print(f"Location: {location}")
        print(f"ID: {event_id}")
    else:
        print("No upcoming events")
