#!/bin/bash
# UGC Studio — one-command launch

cd "$(dirname "$0")"

# Check ffmpeg
if ! command -v ffmpeg &>/dev/null; then
  echo "Installing ffmpeg..."
  brew install ffmpeg
fi

# Install Python deps
pip3 install -r requirements.txt -q

# Start server
echo ""
echo "UGC Studio launching at http://localhost:8765"
echo "Open your browser to http://localhost:8765"
echo ""

# Open browser after 1s
(sleep 1 && open http://localhost:8765) &

python3 server.py
