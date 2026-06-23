#!/usr/bin/env python3
"""
Send emails via Gmail API.
First run: authenticates and saves credentials
Subsequent runs: uses saved credentials
"""

import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CREDENTIALS_FILE = '.claude/gmail_credentials.json'
TOKEN_FILE = '.claude/gmail_token.json'

def authenticate_gmail():
    """Authenticate with Gmail API (one-time setup required)"""
    creds = None

    # Load saved token if it exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # First time: start OAuth flow in browser
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for next time
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds

def send_email(to, subject, body, from_email='eadar7207@gmail.com'):
    """Send email via Gmail API"""
    creds = authenticate_gmail()
    if not creds:
        print("Not authenticated. Set up OAuth credentials first.")
        return False

    try:
        service = build('gmail', 'v1', credentials=creds)

        # Create message
        message = MIMEText(body)
        message['to'] = to
        message['from'] = from_email
        message['subject'] = subject

        # Encode and send
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {'raw': raw_message}

        result = service.users().messages().send(userId='me', body=send_message).execute()
        print(f"✓ Email sent to {to}")
        print(f"Message ID: {result['id']}")
        return True

    except Exception as e:
        print(f"✗ Failed to send: {str(e)}")
        return False

if __name__ == '__main__':
    # Example: send the outreach email
    to = 'eadar7207@icloud.com'
    subject = '15-min call: Automating your lead follow-up'
    body = """Hi Eden,

I came across Adar Systems Tech and thought this might be relevant — we help tech companies automate their lead follow-up so teams spend less time on manual follow-up and more time closing deals.

Most teams we talk to are manually managing follow-up sequences, calendars, and CRM logging. It adds up to 10+ hours a week of tedious work. We've built automations that cut that down to minutes.

I'd love to show you how this works in a quick 15-minute call. No pitch — just a walkthrough of what's possible for your workflow.

Are you free for a brief call this week? I'm flexible on timing.

Best,
Eitan Adar"""

    send_email(to, subject, body)
