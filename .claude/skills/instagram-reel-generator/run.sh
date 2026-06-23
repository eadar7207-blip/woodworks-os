#!/bin/bash
# Instagram Reel Generator skill runner

ADDRESS="$1"
VIDEO_FILE="$2"
DETAILS="$3"
MOOD="${4:-modern}"

if [ -z "$ADDRESS" ] || [ -z "$VIDEO_FILE" ] || [ -z "$DETAILS" ]; then
    echo "Usage: /instagram-reel-generator \"{address}\" \"{video_file}\" \"{details}\""
    echo "Example: /instagram-reel-generator \"123 Oak St\" \"property.mp4\" \"3BR/2BA • \$450K\""
    exit 1
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: FFmpeg is required. Install with: brew install ffmpeg"
    exit 1
fi

# Run the reel generator
python3 "$(dirname "$0")/reel_generator.py" "$ADDRESS" "$VIDEO_FILE" "$DETAILS" "$MOOD"
