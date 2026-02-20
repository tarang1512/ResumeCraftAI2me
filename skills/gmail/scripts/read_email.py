#!/usr/bin/env python3
"""Read emails from Gmail."""
import os
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH = '/home/ubuntu/.openclaw/credentials/gmail-token.json'

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
    
    return build('gmail', 'v1', credentials=creds, static_discovery=False)

def list_emails(query=None, max_results=10, unread_only=False):
    service = get_service()
    if not service:
        return []
    
    q = query or ''
    if unread_only:
        q += ' is:unread' if q else 'is:unread'
    
    results = service.users().messages().list(
        userId='me', 
        q=q.strip() if q else None,
        maxResults=max_results
    ).execute()
    
    messages = results.get('messages', [])
    return messages

def get_email(message_id):
    service = get_service()
    if not service:
        return None
    
    msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    return msg

def format_email(msg):
    headers = {h['name']: h['value'] for h in msg['payload']['headers']}
    subject = headers.get('Subject', 'No Subject')
    sender = headers.get('From', 'Unknown')
    date = headers.get('Date', '')
    
    # Get body
    body = ''
    if 'parts' in msg['payload']:
        for part in msg['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                import base64
                data = part['body'].get('data', '')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                break
    else:
        import base64
        data = msg['payload']['body'].get('data', '')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    
    return {
        'id': msg['id'],
        'subject': subject,
        'from': sender,
        'date': date,
        'snippet': msg.get('snippet', ''),
        'body': body[:500] + '...' if len(body) > 500 else body
    }

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', '-q', help='Search query')
    parser.add_argument('--unread', '-u', action='store_true', help='Unread only')
    parser.add_argument('--max', type=int, default=10, help='Max results')
    parser.add_argument('--read', help='Read specific message ID')
    args = parser.parse_args()
    
    if args.read:
        msg = get_email(args.read)
        if msg:
            formatted = format_email(msg)
            print(f"From: {formatted['from']}")
            print(f"Subject: {formatted['subject']}")
            print(f"Date: {formatted['date']}")
            print(f"\n{formatted['body']}")
    else:
        emails = list_emails(args.query, args.max, args.unread)
        print(f"Found {len(emails)} emails")
        for e in emails:
            msg = get_email(e['id'])
            if msg:
                formatted = format_email(msg)
                print(f"\nID: {formatted['id']}")
                print(f"From: {formatted['from']}")
                print(f"Subject: {formatted['subject']}")
                print(f"Snippet: {formatted['snippet'][:100]}...")
