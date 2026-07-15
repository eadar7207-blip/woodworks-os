---
name: claude-app-troubleshooting
description: Diagnose and work through problems with the Claude.ai consumer app (mobile/desktop/web) — chats auto-compacting/summarizing, "new chat" not working, app stuck or unresponsive. Use when Eitan reports issues with the Claude app itself, not with this repo or Claude Code.
---

# Claude App Troubleshooting

Eitan uses the Claude.ai consumer app day to day. This skill is for when *that app* misbehaves — not for bugs in this repo, and not for Claude Code (the CLI/web coding tool this session runs in). Those are different products; don't conflate them.

**Hard limit: this repo has no access to Claude.ai's backend, account state, or client code.** Nothing here can patch the app. The job is to (1) triage what's actually happening, (2) walk through the fixes that are actually in Eitan's control, (3) know when to stop and hand off to support.

---

## Step 1: Pin down which product

Ask if it's not already clear:

- **Claude.ai app** (mobile/desktop/web at claude.ai) — this skill
- **Claude Code** (this coding assistant, CLI or claude.ai/code) — different problem, different fix (e.g. `/compact`, context window settings) — don't use this skill, just help directly
- **Claude Tag / Slack** — different again

Don't guess from the word "Claude" alone — "chat," "compacting," and "new chat" all mean different things depending on which product.

## Step 2: Check for a known outage first

Before troubleshooting client-side, check https://status.anthropic.com for active incidents. Note: WebFetch may return 403 on that domain from this environment — if so, tell Eitan to check it directly rather than guessing at status.

If there's an active incident matching the symptoms, stop here — nothing client-side will fix a server-side outage. Report the incident and move on.

## Step 3: Symptom-specific troubleshooting

### "Chats are compacting" (context getting summarized/condensed)

This is Claude.ai auto-summarizing long conversations to keep them within context limits — expected behavior on long threads, not a bug. Fix:
- Start an actual **new** conversation instead of continuing a long one, if losing earlier context is a problem
- If it's happening on short/new chats, that's abnormal — treat as a bug, go to Step 3b

### "Can't use / start new chats" (new chat button unresponsive, stuck, errors)

Work through in order, stopping as soon as it resolves:
1. Hard refresh (web: Ctrl/Cmd+Shift+R) or fully quit and reopen (mobile/desktop) — not just backgrounding
2. Log out and back in — clears stale session tokens, the most common cause of a stuck "new chat"
3. Check for a pending app update (App Store / Play Store / desktop auto-update)
4. Try a different network or a private/incognito browser window — rules out local network/extension interference
5. Try another device — isolates whether it's account-wide or device-specific

### "Response incomplete" error (Claude stops mid-response)

When Claude's response cuts off with a "Response incomplete" banner:
1. Retry the message (usually works on the second attempt)
2. Hard refresh the page or restart the app
3. Try a shorter prompt or smaller context
4. If it's consistently cutting off responses, check status.anthropic.com for rate-limit or service issues
5. Try on a different device to see if it's app/network-specific

If retries don't work and there's no active incident, this is a backend issue — escalate to support.

### Anything else (errors, crashes, missing features)

Get the exact error message/screenshot before troubleshooting blind. Check status.anthropic.com regardless of symptom.

## Step 4: Escalate

If Step 3 doesn't resolve it, this is out of Eitan's control and mine — report to Anthropic support at support.claude.com with:
- Which product/platform (web/iOS/Android/desktop)
- Exact symptom and when it started
- What was already tried from Step 3

Don't keep looping through client-side fixes past this point — say clearly that it needs support, not more troubleshooting.
