#!/usr/bin/env python3
"""
Test Instagram DM auto-responder via Composio + Claude
Run: python3 test_instagram_dm.py
"""
import os
import anthropic
from composio_anthropic import ComposioToolSet, Action

# Load .env
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _, _v = _line.partition("=")
                if _v:
                    os.environ.setdefault(_k.strip(), _v.strip())

COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Get Instagram tools
tools = toolset.get_tools(actions=[
    Action.INSTAGRAM_GET_CONVERSATIONS,
    Action.INSTAGRAM_SEND_MESSAGE,
])

print("Fetching Instagram DMs and auto-replying...\n")

messages = [
    {
        "role": "user",
        "content": (
            "You are an AI assistant for a real estate business. "
            "1. Fetch the most recent Instagram DM conversations. "
            "2. For each unanswered message, reply with a warm, helpful message "
            "asking how you can help them with their real estate needs. "
            "Keep replies short and conversational."
        ),
    }
]

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

# Agentic loop
while response.stop_reason == "tool_use":
    tool_results = toolset.handle_tool_calls(response)
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

print(response.content[0].text)
