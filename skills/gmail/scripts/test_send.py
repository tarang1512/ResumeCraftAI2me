#!/usr/bin/env python3
"""Quick test of Gmail send functionality."""
import pickle
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build

with open('/home/ubuntu/.openclaw/credentials/gmail-token.json', 'rb') as f:
    creds = pickle.load(f)

service = build('gmail', 'v1', credentials=creds, static_discovery=False)

# Create test email
msg = MIMEText('This is a test email from your OpenClaw assistant.')
msg['to'] = 'tarang1512@yahoo.com'  # Send to yourself
msg['subject'] = 'Test Email from OpenClaw'

raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

try:
    result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
    print(f"✅ Test email sent! Message ID: {result['id']}")
except Exception as e:
    print(f"❌ Error: {e}")
