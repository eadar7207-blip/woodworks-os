#!/usr/bin/env python3
"""
Generates the Adar Realty Studios logo as a PNG.
Usage: python3 generate_logo.py --output /path/to/logo.png
"""
import argparse
import os

def generate(output_path):
    from PIL import Image, ImageDraw, ImageFont

    W, H = 600, 200
    primary = (27, 58, 107)
    accent = (74, 158, 219)
    white = (255, 255, 255)
    light = (200, 220, 245)

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([0, 0, W-1, H-1], radius=18, fill=primary)
    draw.rounded_rectangle([0, 0, 8, H-1], radius=4, fill=accent)

    cx, cy = 520, 50
    for c, r in [(accent, 22), (primary, 16), (white, 8)]:
        pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
        draw.polygon(pts, fill=c)

    for row in range(3):
        for col in range(4):
            dx = 465 + col * 16
            dy = 100 + row * 16
            draw.ellipse([dx-2, dy-2, dx+2, dy+2], fill=light + (120,))

    try:
        font_big = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        font_tag = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except Exception:
        font_big = ImageFont.load_default()
        font_sub = font_big
        font_tag = font_big

    draw.text((42, 38), "ADAR", font=font_big, fill=white)
    bbox = draw.textbbox((42, 38), "ADAR", font=font_big)
    line_w = bbox[2] - bbox[0]
    draw.rectangle([42, bbox[3] + 4, 42 + line_w, bbox[3] + 7], fill=accent)
    draw.text((44, bbox[3] + 16), "REALTY STUDIOS", font=font_sub, fill=light)
    draw.text((44, H - 34), "AI Automations for Real Estate", font=font_tag, fill=(150, 190, 230))

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Logo saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/tmp/adar_logo.png")
    args = parser.parse_args()
    generate(args.output)
