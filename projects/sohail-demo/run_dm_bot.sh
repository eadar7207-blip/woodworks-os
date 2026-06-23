#!/bin/bash
# Instagram DM bot — runs forever, checking every 30 seconds
# Sourced via launchd so it persists across reboots

# Load user environment
source /etc/profile 2>/dev/null
source ~/.bash_profile 2>/dev/null || source ~/.zprofile 2>/dev/null

DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[$(date)] DM bot started" >&2

exec /usr/bin/python3 "$DIR/instagram_dm_bot.py"
