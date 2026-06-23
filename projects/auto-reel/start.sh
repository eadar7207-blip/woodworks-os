#!/bin/bash
# Auto Reel — start the watch folder pipeline
# Just double-click this or run it in Terminal

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export ANTHROPIC_API_KEY="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"

echo "Starting Auto Reel..."
python3 "$SCRIPT_DIR/auto_post.py"
