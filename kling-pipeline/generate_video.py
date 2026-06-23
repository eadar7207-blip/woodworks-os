#!/usr/bin/env python3
"""
Kling talking-head video generator.

Usage:
  1. Drop your script text into script.txt (in this folder)
  2. Run: python3 generate_video.py
  3. Audio is saved as generated_voice.mp3 — Claude then uploads it to Kling
"""

import os
import sys
import requests
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
PIPELINE_DIR = Path(__file__).parent
SCRIPT_FILE = PIPELINE_DIR / "script.txt"

load_dotenv(PIPELINE_DIR / ".env")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")


def load_script() -> str:
    if not SCRIPT_FILE.exists():
        print(f"ERROR: {SCRIPT_FILE} not found.")
        sys.exit(1)
    text = SCRIPT_FILE.read_text(encoding="utf-8").strip()
    if not text:
        print("ERROR: script.txt is empty.")
        sys.exit(1)
    return text


def generate_voice(script_text: str) -> Path:
    if not ELEVENLABS_API_KEY:
        print("ERROR: ELEVENLABS_API_KEY not set in .env")
        sys.exit(1)
    if not ELEVENLABS_VOICE_ID:
        print("ERROR: ELEVENLABS_VOICE_ID not set. Run setup_voice.py first.")
        sys.exit(1)

    print(f"Generating audio ({len(script_text)} chars) via ElevenLabs...")
    resp = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
        headers={
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "text": script_text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        },
        timeout=60,
    )

    if resp.status_code != 200:
        print(f"ERROR: ElevenLabs TTS failed ({resp.status_code}): {resp.text}")
        sys.exit(1)

    audio_path = PIPELINE_DIR / "generated_voice.mp3"
    audio_path.write_bytes(resp.content)
    size_kb = len(resp.content) / 1000
    print(f"Audio saved: {audio_path}  ({size_kb:.0f} KB)")
    return audio_path


def main():
    print("\n=== Step 1: Generate Voice Audio ===\n")
    script_text = load_script()
    print(f'Script: "{script_text[:80]}{"..." if len(script_text) > 80 else ""}"\n')
    audio_path = generate_voice(script_text)
    print(f"\nDone. Audio at: kling-pipeline/generated_voice.mp3")
    print("Now tell Claude to upload to Kling.")


if __name__ == "__main__":
    main()
