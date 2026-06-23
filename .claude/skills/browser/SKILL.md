---
name: browser
description: Use when you need to control a real browser — navigate sites, click buttons, fill forms, upload files, scrape content, automate multi-step web workflows, or interact with any web app as a human would. Requires the Playwright MCP server to be configured in ~/.claude.json.
version: 1.0.0
user-invocable: true
argument-hint: "[url or task description]"
---

You are controlling a real browser via Playwright. The user wants zero manual effort — you do everything.

## Setup check

Before starting any task, verify Playwright MCP is available by calling `mcp__playwright__browser_snapshot`. If it errors, tell the user to restart Claude Code so the MCP server loads.

## Core workflow

1. **Navigate** — go to the URL or starting page
2. **Screenshot** — take a screenshot to see the current state
3. **Snapshot** — use `browser_snapshot` to get the accessibility tree for clicking/typing (not the screenshot)
4. **Act** — click, type, upload, select as needed
5. **Verify** — screenshot again to confirm the action worked
6. **Repeat** until the task is done

Always take a screenshot after each major action. Never assume an action succeeded without visual confirmation.

## Tool usage rules

- Use `browser_snapshot` to find element refs before clicking — never guess selectors blind
- Use `browser_take_screenshot` to see what's on screen (visual confirmation)
- Use `browser_navigate` to go to URLs
- Use `browser_click` with the `target` ref from snapshot, not fragile CSS selectors
- Use `browser_type` to fill text fields
- Use `browser_evaluate` to run JavaScript when no direct tool works
- Use `browser_file_upload` immediately after a file chooser opens — it only works in that window

## Common patterns

### File upload (hidden input)
Most file inputs are invisible. Trigger them with JS, then upload:
```
browser_evaluate: () => { document.querySelector('input[type="file"]').dispatchEvent(new MouseEvent('click', {bubbles: true})) }
```
Then immediately call `browser_file_upload` with the absolute file path.

Files must be inside the project directory — Playwright blocks uploads from outside the workspace. Copy files to the project dir first if needed.

### Clicking when strict mode fails (multiple matches)
Use `browser_snapshot` to get the specific `ref=eXXX` for the exact element, then pass that ref as the `target`.

### Waiting for something to load
Use `browser_wait_for` with a reasonable time, then screenshot to check state. Don't sleep more than needed.

### Settings panels / dropdowns
If a settings panel opens, use `browser_snapshot` scoped to the panel's ref to get clean refs for the options inside it.

### Login state
Playwright MCP persists browser sessions across uses. If the user is already logged into a site in their Playwright browser, Claude inherits that session automatically.

## File paths

When uploading files, always use absolute paths:
- Project root: `/Users/main10servicesgmail.com/Desktop/Woodworks-OS/`
- Copy files here before uploading if they're elsewhere on disk

## What this skill handles

- Automating web tools (Kling, HeyGen, Canva, any SaaS)
- Form filling and submission
- File uploads (images, docs, videos)
- Scraping content from pages
- Multi-step checkout or signup flows
- Any task where the user says "can you do it for me" on a website

## What this skill does NOT handle

- Native desktop apps (not browser-based)
- Tasks requiring real payment without user confirmation — always pause and confirm before clicking "Pay"
- CAPTCHA solving
