#!/usr/bin/env python3
"""
One-time setup: clones your voice in ElevenLabs from eitan_voice_sample.mp3
and saves the voice ID to .env so the pipeline can use it every time.

Run this once:
  python3 setup_voice.py
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

PIPELINE_DIR = Path(__file__).parent
ROOT = PIPELINE_DIR.parent
VOICE_SAMPLE = ROOT / "eitan_voice_sample.mp3"

load_dotenv(PIPELINE_DIR / ".env")
API_KEY = os.getenv("ELEVENLABS_API_KEY")

def main():
    if not API_KEY or API_KEY == "your_elevenlabs_key_here":
        print("ERROR: Add your ELEVENLABS_API_KEY to kling-pipeline/.env first.")
        sys.exit(1)

    if not VOICE_SAMPLE.exists():
        print(f"ERROR: Voice sample not found at {VOICE_SAMPLE}")
        sys.exit(1)

    print(f"Creating voice clone from: {VOICE_SAMPLE.name}")

    with open(VOICE_SAMPLE, "rb") as f:
        resp = requests.post(
            "https://api.elevenlabs.io/v1/voices/add",
            headers={"xi-api-key": API_KEY},
            data={
                "name": "Eitan Adar",
                "description": "Eitan Adar personal voice for Instagram content",
            },
            files={"files": (VOICE_SAMPLE.name, f, "audio/mpeg")},
            timeout=60,
        )

    if resp.status_code != 200:
        print(f"ERROR: Voice clone failed ({resp.status_code}): {resp.text}")
        sys.exit(1)

    voice_id = resp.json().get("voice_id")
    print(f"Voice created. ID: {voice_id}")

    # Save voice ID to .env
    env_path = PIPELINE_DIR / ".env"
    env_text = env_path.read_text()
    if "ELEVENLABS_VOICE_ID=" in env_text:
        lines = []
        for line in env_text.splitlines():
            if line.startswith("ELEVENLABS_VOICE_ID="):
                lines.append(f"ELEVENLABS_VOICE_ID={voice_id}")
            else:
                lines.append(line)
        env_path.write_text("\n".join(lines) + "\n")
    else:
        env_path.write_text(env_text + f"\nELEVENLABS_VOICE_ID={voice_id}\n")

    print(f"\nDone. Voice ID saved to .env.")
    print("Now run: python3 generate_video.py")

if __name__ == "__main__":
    main()
