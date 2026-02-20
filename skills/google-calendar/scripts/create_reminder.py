#!/usr/bin/env python3
"""Create a cron job to remind before a calendar event."""
import argparse
import sys
import json
from auth import get_service

def get_event(calendar_id, event_id):
    service = get_service()
    if not service:
        return None
    
    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        return event
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return None

def create_reminder_cron(event, minutes_before=15):
    """Output a cron job definition for this event reminder."""
    from datetime import datetime, timedelta
    
    start_str = event['start'].get('dateTime')
    if not start_str:
        print("ERROR: All-day events not supported for minute-based reminders")
        return None
    
    start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
    reminder_time = start_dt - timedelta(minutes=minutes_before)
    
    # Build cron expression
    cron_expr = f"{reminder_time.minute} {reminder_time.hour} {reminder_time.day} {reminder_time.month} *"
    
    job = {
        "name": f"Calendar: {event.get('summary', 'Event')}",
        "schedule": {"kind": "cron", "expr": cron_expr, "tz": "UTC"},
        "sessionTarget": "isolated",
        "payload": {
            "kind": "agentTurn",
            "message": f"📅 Calendar Reminder: {event.get('summary', 'Event')} starts in {minutes_before} minutes!"
        },
        "delivery": {"mode": "announce"}
    }
    
    return job

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--event-id', required=True)
    parser.add_argument('--calendar', default='primary')
    parser.add_argument('--minutes-before', type=int, default=15)
    args = parser.parse_args()
    
    event = get_event(args.calendar, args.event_id)
    if not event:
        print("ERROR: Event not found")
        sys.exit(1)
    
    job = create_reminder_cron(event, args.minutes_before)
    if job:
        print(json.dumps(job, indent=2))
        print("\n# Add this job using: openclaw cron add --job '<json>'")
