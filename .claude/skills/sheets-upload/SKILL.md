# sheets-upload

Upload any local .xlsx, .csv, or .ods file directly to Google Sheets — no browser interaction needed. Uses the Google Drive API with your existing OAuth credentials. The file is converted to a native Google Sheet and the URL is returned and opened automatically.

## When to use

Use this skill any time the user wants to:
- Open an Excel or CSV file in Google Sheets
- Upload a spreadsheet to Google Drive
- Share a spreadsheet via a Google Sheets link

## How to invoke

`/sheets-upload <file_path> [sheet_name]`

Examples:
- `/sheets-upload ~/Desktop/social_media_jobs.xlsx`
- `/sheets-upload projects/dailyremote-scraper/social_media_jobs.xlsx "Social Media Jobs"`
- `/sheets-upload data.csv "Q3 Report"`

## What it does

1. Authenticates with Google Drive API (one-time browser auth on first run, then uses saved token at `~/.config/woodworks-os/sheets_token.json`)
2. Uploads the file and converts it to a native Google Sheet
3. Returns the Google Sheets URL
4. Opens the sheet in your browser automatically

## Supported formats

- `.xlsx` — Excel (recommended)
- `.xls` — Legacy Excel
- `.csv` — Comma-separated values
- `.tsv` — Tab-separated values
- `.ods` — OpenDocument Spreadsheet

## Implementation

Run the upload script:

```bash
python3 .claude/skills/sheets-upload/scripts/upload_to_sheets.py <file_path> [sheet_name]
```

Credentials: `.claude/gmail_credentials.json`
Token cache: `~/.config/woodworks-os/sheets_token.json`

## First run note

The first time this runs, a browser window will open asking you to authorize Google Drive access. After that it's fully automatic — the token is saved and reused.
