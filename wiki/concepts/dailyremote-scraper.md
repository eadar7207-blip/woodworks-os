---
title: DailyRemote Job Scraper
type: concept
tags: [tools, scraping, lead-gen, sales]
created: 2026-06-24
updated: 2026-06-24
sources: 0
---

# DailyRemote Job Scraper

A Python scraper that pulls remote job listings from dailyremote.com and exports them to a formatted Excel file.

## What it does

- Scrapes job listings by category and country using country-specific URLs (`/remote-sales-jobs-in-{country}`)
- Deduplicates by job URL across runs
- Outputs a formatted `.xlsx` with brand colors, frozen header row, auto-filter, and clickable apply links

## Output columns

Job Title, Country, Employment Type, Date Posted, Location, Salary, Experience Level, Categories, Description Snippet, Apply URL

## Files

- Script: `projects/dailyremote-scraper/scrape_jobs.py`
- Output: `projects/dailyremote-scraper/europe_sales_jobs.xlsx`
- Google Sheet (100-row preview): https://docs.google.com/spreadsheets/d/1vrNFYCySiwTntUHVMezWwLNihxG-8gthfE6poCsmQjg/edit

## How to run

```bash
python3 projects/dailyremote-scraper/scrape_jobs.py
```

To change target: edit `EUROPEAN_COUNTRIES`, `MAX_JOBS`, and `OUTPUT_FILE` at the top of the script.

## Current config

- Category: Sales (UK)
- Countries: 25 European countries defined, UK fills 500 jobs alone
- Max jobs: 500
- URL pattern: `https://dailyremote.com/remote-sales-jobs-in-{country-slug}?page={n}`

## Notes

- Location filter via URL param (`?location=Europe`) is JS-rendered and doesn't work with static scraping — use country-specific URLs instead
- To upload full 500 rows to Google Sheets, run: `python3 .claude/skills/sheets-upload/scripts/upload_to_sheets.py projects/dailyremote-scraper/europe_sales_jobs.xlsx "UK Remote Sales Jobs"` (requires one-time browser OAuth)
