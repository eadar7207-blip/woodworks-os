#!/usr/bin/env python3
"""
Instagram DM Auto-Responder
Checks recent DMs and replies to unanswered ones using Claude AI.
Run: python3 instagram_dm_bot.py
"""
import sys
import os
# Ensure user packages are on path when running via launchd
sys.path.insert(0, '/Users/main10servicesgmail.com/Library/Python/3.9/lib/python/site-packages')

import json
import urllib.request
from datetime import datetime, timezone

import anthropic

# Load .env
_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env):
    with open(_env) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                if v:
                    os.environ.setdefault(k.strip(), v.strip())

COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
COMPOSIO_USER_ID = os.getenv("COMPOSIO_USER_ID", "pg-test-e1f56a79-b6f4-45b3-884f-707fe3c52d93")
IG_USER_ID = "17841436763290033"  # eitanadar.ai account ID

BASE = "https://backend.composio.dev/api/v3/tools/execute"
claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def composio(tool, arguments=None):
    body = json.dumps({"arguments": arguments or {}, "user_id": COMPOSIO_USER_ID}).encode()
    req = urllib.request.Request(
        f"{BASE}/{tool}", data=body,
        headers={"x-api-key": COMPOSIO_API_KEY, "Content-Type": "application/json"},
        method="POST"
    )
    res = urllib.request.urlopen(req)
    return json.loads(res.read())


def generate_reply(sender_username, message_text):
    prompt = f"""You are Eitan Adar, founder of an AI automation agency focused on real estate businesses.
Someone just DM'd you on Instagram.

Sender: @{sender_username}
Their message: "{message_text}"

Write a short, natural reply (2-3 sentences max). Be conversational, not salesy.
- If they seem interested in AI or automation, ask what their business does
- If they're asking about pricing/services, say you'd love to chat and ask them to book a quick call
- If it's a generic greeting like "hi" or "hello", respond warmly and ask how you can help them
- Sign off as yourself, not as a bot
- No hashtags, no emojis unless they used them first

Just write the reply text, nothing else."""

    msg = claude.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text.strip()


def run():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking Instagram DMs...\n")

    convos = composio("INSTAGRAM_LIST_ALL_CONVERSATIONS", {"limit": 10})
    conversations = convos.get("data", {}).get("data", [])

    if not conversations:
        print("No conversations found.")
        return

    replied = 0
    for convo in conversations:
        convo_id = convo["id"]

        msgs_data = composio("INSTAGRAM_LIST_ALL_MESSAGES", {
            "conversation_id": convo_id, "limit": 5
        })
        messages = msgs_data.get("data", {}).get("data", [])

        if not messages:
            continue

        # Most recent message
        latest = messages[0]
        sender = latest.get("from_", {})
        sender_id = sender.get("id", "")
        sender_name = sender.get("username", "unknown")
        message_text = latest.get("message", "").strip()

        # Skip if we sent the last message (don't reply to ourselves)
        if sender_id == IG_USER_ID:
            continue

        # Skip empty messages
        if not message_text:
            continue

        print(f"Unanswered DM from @{sender_name}: \"{message_text}\"")

        reply = generate_reply(sender_name, message_text)
        print(f"Sending reply: \"{reply}\"")

        result = composio("INSTAGRAM_SEND_TEXT_MESSAGE", {
            "recipient_id": sender_id,
            "text": reply,
            "ig_user_id": IG_USER_ID
        })

        if result.get("successful"):
            print(f"Sent to @{sender_name}\n")
            replied += 1
        else:
            print(f"Failed: {result.get('error')}\n")

    print(f"Done. Replied to {replied} conversation(s).")


if __name__ == "__main__":
    import time
    while True:
        try:
            run()
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
        time.sleep(30)
