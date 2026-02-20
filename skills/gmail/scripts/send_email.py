#!/usr/bin/env python3
"""Send email with attachments using Gmail API"""

import os
import base64
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

def send_email_with_attachment(to_email, subject, body, attachment_path=None):
    """Send email with optional attachment"""
    
    creds_path = "/home/ubuntu/.openclaw/credentials/gmail-token.json"
    
    if not os.path.exists(creds_path):
        print(f"❌ Gmail credentials not found at {creds_path}")
        return False
    
    try:
        # Load credentials
        creds = Credentials.from_authorized_user_file(creds_path)
        service = build('gmail', 'v1', credentials=creds)
        
        # Create message
        msg = MIMEMultipart()
        msg['to'] = to_email
        msg['subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'plain'))
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                file_data = f.read()
            
            # Determine mime type
            filename = os.path.basename(attachment_path)
            if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
                part = MIMEImage(file_data, name=filename)
            else:
                part = MIMEApplication(file_data, name=filename)
            
            part.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(part)
            print(f"📎 Attached: {filename}")
        
        # Encode and send
        raw_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
        body = {'raw': raw_msg}
        
        message = service.users().messages().send(userId='me', body=body).execute()
        
        print(f"✅ Email sent successfully!")
        print(f"📧 To: {to_email}")
        print(f"📨 Message ID: {message['id']}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 send_email.py <to_email> <subject> <body> [attachment_path]")
        sys.exit(1)
    
    to = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachment = sys.argv[4] if len(sys.argv) > 4 else None
    
    success = send_email_with_attachment(to, subject, body, attachment)
    sys.exit(0 if success else 1)
