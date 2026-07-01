# Tools

Python scripts for deterministic execution. Each script does one thing reliably.

## Conventions
- One script per task (e.g. `scrape_site.py`, `send_email.py`)
- All credentials come from `.env` -- never hardcoded
- Scripts should be runnable standalone and importable as modules
- Add a docstring at the top of each file explaining what it does and what it expects

## Usage
Claude reads the relevant workflow first, then calls the appropriate script here.
