#!/usr/bin/env python3
"""List available calendars."""
import sys
from auth import get_service

def list_calendars():
    service = get_service()
    if not service:
        print("ERROR: Not authenticated", file=sys.stderr)
        return []
    
    calendars_result = service.calendarList().list().execute()
    return calendars_result.get('items', [])

if __name__ == '__main__':
    calendars = list_calendars()
    for cal in calendars:
        primary = " [PRIMARY]" if cal.get('primary') else ""
        print(f"{cal['id']} | {cal.get('summary', 'Unnamed')}{primary}")
