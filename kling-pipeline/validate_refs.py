#!/usr/bin/env python3
"""
Validates all images in face-refs/ before sending anything to Kling.
Checks: file exists, correct format, reasonable size, not corrupted.
"""

import os
import sys
from pathlib import Path

FACE_REFS_DIR = Path(__file__).parent.parent / "face-refs"

PRIMARY_IMAGE = "01-straight-on.jpeg"
OPTIONAL_IMAGES = [
    "02-smiling.jpeg",
    "03-straight-on-alt.jpeg",
    "04-profile.jpeg",
    "05-three-quarter-left.jpeg",
    "06-three-quarter-right.jpeg",
]
EXPECTED_IMAGES = [PRIMARY_IMAGE] + OPTIONAL_IMAGES

ALLOWED_EXTENSIONS = {".jpeg", ".jpg", ".png", ".webp"}
MIN_SIZE_BYTES = 10_000       # 10 KB — anything smaller is likely corrupt
MAX_SIZE_BYTES = 10_000_000   # 10 MB — Kling's stated limit


def check_pillow():
    try:
        from PIL import Image
        return True
    except ImportError:
        print("  [warn] Pillow not installed — skipping pixel-level validation")
        print("         Run: pip install Pillow")
        return False


def validate_image(path: Path, use_pillow: bool) -> list[str]:
    errors = []

    if not path.exists():
        errors.append(f"file not found: {path.name}")
        return errors

    ext = path.suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        errors.append(f"unsupported format '{ext}' — must be jpeg/jpg/png/webp")

    size = path.stat().st_size
    if size < MIN_SIZE_BYTES:
        errors.append(f"file too small ({size} bytes) — likely corrupt or placeholder")
    if size > MAX_SIZE_BYTES:
        errors.append(f"file too large ({size / 1_000_000:.1f} MB) — Kling limit is 10 MB")

    if use_pillow and not errors:
        try:
            from PIL import Image
            with Image.open(path) as img:
                img.verify()
            with Image.open(path) as img:
                w, h = img.size
                if w < 256 or h < 256:
                    errors.append(f"resolution too low ({w}x{h}) — minimum 256x256 recommended")
                if img.mode not in ("RGB", "RGBA", "L"):
                    errors.append(f"unexpected color mode '{img.mode}'")
        except Exception as e:
            errors.append(f"image corrupt or unreadable: {e}")

    return errors


def main():
    print(f"\nValidating face-refs at: {FACE_REFS_DIR}\n")

    if not FACE_REFS_DIR.exists():
        print(f"ERROR: Directory not found: {FACE_REFS_DIR}")
        print("Create it and add your 6 reference images.")
        sys.exit(1)

    use_pillow = check_pillow()
    print()

    all_passed = True
    for filename in EXPECTED_IMAGES:
        path = FACE_REFS_DIR / filename
        optional = filename != PRIMARY_IMAGE

        if not path.exists() and optional:
            print(f"  --    {filename}  (optional, not present)")
            continue

        errors = validate_image(path, use_pillow)
        if errors:
            if optional:
                print(f"  WARN  {filename}  (optional)")
            else:
                all_passed = False
                print(f"  FAIL  {filename}")
            for e in errors:
                print(f"        - {e}")
        else:
            size_kb = path.stat().st_size / 1000
            print(f"  OK    {filename}  ({size_kb:.0f} KB)")

    # Also warn about unexpected files in the folder
    actual = {f.name for f in FACE_REFS_DIR.iterdir() if f.is_file()}
    expected_set = set(EXPECTED_IMAGES)
    extras = actual - expected_set
    if extras:
        print(f"\n  [warn] Unexpected files in face-refs/ (ignored by pipeline):")
        for f in sorted(extras):
            print(f"         {f}")

    print()
    if all_passed:
        print("All images passed. Safe to run generate_video.py.\n")
        sys.exit(0)
    else:
        print("Fix the errors above before generating video.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
