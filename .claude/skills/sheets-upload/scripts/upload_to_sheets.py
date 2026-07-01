#!/usr/bin/env python3
"""
Upload a local .xlsx or .csv file to Google Sheets via Drive API.
Converts the file to a native Google Sheet and returns the URL.

Usage:
  python3 upload_to_sheets.py <file_path> [sheet_name]
"""

import sys
import os
import json
import subprocess

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "..", "gmail_credentials.json")
TOKEN_FILE = os.path.expanduser("~/.config/woodworks-os/sheets_token.json")
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
]


def get_creds():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    creds = None

    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return creds


def upload_to_sheets(file_path, sheet_name=None):
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)

    file_path = os.path.abspath(file_path)
    if not sheet_name:
        sheet_name = os.path.splitext(os.path.basename(file_path))[0]

    ext = os.path.splitext(file_path)[1].lower()
    mime_map = {
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xls": "application/vnd.ms-excel",
        ".csv": "text/csv",
        ".tsv": "text/tab-separated-values",
        ".ods": "application/vnd.oasis.opendocument.spreadsheet",
    }
    source_mime = mime_map.get(ext, "application/octet-stream")

    print(f"Authenticating with Google...")
    creds = get_creds()

    service = build("drive", "v3", credentials=creds)

    print(f"Uploading '{os.path.basename(file_path)}' as '{sheet_name}'...")

    file_metadata = {
        "name": sheet_name,
        "mimeType": "application/vnd.google-apps.spreadsheet",  # convert to Sheets
    }

    media = MediaFileUpload(file_path, mimetype=source_mime, resumable=True)

    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id,name,webViewLink",
    ).execute()

    file_id = uploaded["id"]
    name = uploaded["name"]
    url = uploaded["webViewLink"]

    print(f"\nDone!")
    print(f"  Name: {name}")
    print(f"  URL:  {url}")
    print(f"  ID:   {file_id}")

    # Open in browser
    subprocess.run(["open", url])

    return url


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 upload_to_sheets.py <file_path> [sheet_name]")
        sys.exit(1)

    file_path = sys.argv[1]
    sheet_name = sys.argv[2] if len(sys.argv) > 2 else None

    upload_to_sheets(file_path, sheet_name)
