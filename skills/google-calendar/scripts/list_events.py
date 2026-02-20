#!/usr/bin/env python3
"""List upcoming calendar events."""
import argparse
import sys
import os
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from auth import get_service

LOCAL_TZ = ZoneInfo("America/New_York")

def list_events(days=7, calendar_id='primary', query=None, max_results=50):
    service = get_service()
    if not service:
        print("ERROR: Not authenticated. Run auth.py first.", file=sys.stderr)
        return []
    
    now = datetime.now(timezone.utc)
    time_min = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_max = (now + timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime',
        q=query
    ).execute()
    
    events = events_result.get('items', [])
    return events

def format_event(event):
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    summary = event.get('summary', 'No title')
    location = event.get('location', '')
    
    # Parse datetime and convert to local timezone
    if 'T' in start:
        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
        # Convert to local timezone
        start_dt_local = start_dt.astimezone(LOCAL_TZ)
        start_str = start_dt_local.strftime('%Y-%m-%d %H:%M %Z')
    else:
        start_str = start
    
    result = f"{start_str} | {summary}"
    if location:
        result += f" | {location}"
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, default=7)
    parser.add_argument('--calendar', default='primary')
    parser.add_argument('--query', help='Search query')
    args = parser.parse_args()
    
    events = list_events(args.days, args.calendar, args.query)
    
    if not events:
        print("No upcoming events found.")
    else:
        for event in events:
            print(format_event(event))
            # Also print event ID for reminder creation
            print(f"  ID: {event['id']}")
