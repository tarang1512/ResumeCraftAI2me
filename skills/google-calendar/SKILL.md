---
name: google-calendar
description: Full Google Calendar integration — read events, create reminders, manage schedules. Use when user needs calendar access, event reminders, schedule queries, or calendar automation. Supports OAuth authentication, event listing, filtering, and smart reminder creation via cron.
---

# Google Calendar Skill

Full access to Google Calendar API for reading events, creating reminders, and schedule management.

## Authentication

Uses OAuth 2.0 flow. Credentials stored at:
- Token: `/home/ubuntu/.openclaw/credentials/google-calendar-token.json`
- Client secrets: `/home/ubuntu/.openclaw/credentials/google-calendar-client.json`

### First-time setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Google Calendar API
3. Create OAuth 2.0 credentials (Desktop app type)
4. Download `client_secret.json` and save to credentials path above
5. Run auth flow: `python3 /home/ubuntu/.openclaw/workspace/skills/google-calendar/scripts/auth.py`
6. Follow link, authorize, paste code back

## Scripts

### List events
```bash
python3 scripts/list_events.py [--days N] [--calendar ID] [--query TEXT]
```

### Get next event
```bash
python3 scripts/next_event.py [--calendar ID]
```

### Create reminder cron
```bash
python3 scripts/create_reminder.py --event-id ID --minutes-before N
```

### List calendars
```bash
python3 scripts/list_calendars.py
```

## Common Workflows

**"What's on my calendar today?"**
→ Run `list_events.py --days 1`, summarize for user.

**"Remind me 15 min before my meetings"**
→ Use `create_reminder.py` for each meeting, or set up recurring cron that checks calendar every 15 min.

**"When's my next meeting?"**
→ Run `next_event.py`, report start time and details.

**"Add a reminder for [event]"**
→ Find event via list_events.py with query, then create_reminder.py.

## Calendar IDs

- Primary: `primary`
- Find others: `list_calendars.py`

## Error Handling

- Token expired → Re-run auth flow
- Rate limit → Back off 60 seconds
- No events found → Report clearly, don't error
