#!/usr/bin/env python3
"""Generate a logo PNG for Adar Realty Studios."""

import argparse
from PIL import Image, ImageDraw, ImageFont
import os


def generate_logo(output_path: str, width: int = 600, height: int = 160):
    primary = (27, 58, 107)    # #1B3A6B
    accent = (74, 158, 219)    # #4A9EDB
    white = (255, 255, 255)

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background pill
    draw.rounded_rectangle([0, 0, width, height], radius=18, fill=primary)

    # Accent stripe
    stripe_w = 8
    draw.rounded_rectangle([0, 0, stripe_w, height], radius=4, fill=accent)

    # House icon (simple polygon)
    cx, cy = 60, 80
    house_pts = [
        (cx, cy - 30),          # roof peak
        (cx - 28, cy),          # left eave
        (cx - 28, cy + 28),     # bottom left
        (cx + 28, cy + 28),     # bottom right
        (cx + 28, cy),          # right eave
    ]
    draw.polygon(house_pts, fill=accent)
    # Door
    draw.rectangle([cx - 8, cy + 10, cx + 8, cy + 28], fill=primary)

    # Text
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except OSError:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((110, 38), "ADAR REALTY STUDIOS", font=font_large, fill=white)
    draw.text((112, 88), "AI Automation for Real Estate Agents", font=font_small, fill=accent)

    img.save(output_path, "PNG")
    print(f"Logo saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--width", type=int, default=600)
    parser.add_argument("--height", type=int, default=160)
    args = parser.parse_args()
    generate_logo(args.output, args.width, args.height)
