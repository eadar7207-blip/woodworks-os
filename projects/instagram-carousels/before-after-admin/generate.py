#!/usr/bin/env python3
"""Before/After admin time carousel — @eitanadar.ai"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BG    = (10, 14, 39)
CYAN  = (0, 255, 255)
PINK  = (255, 0, 110)
GREEN = (57, 255, 20)
WHITE = (255, 255, 255)
GRAY  = (130, 140, 170)
DARK  = (20, 26, 60)
DIM   = (40, 50, 90)

W, H = 1080, 1350
M = 72

CONTENT = [
    {
        "task": "LISTING DESCRIPTIONS",
        "old_time": "45 MIN",
        "old_desc": ["Staring at a blank doc.", "Rewriting it three times."],
        "new_time": "3 MIN",
        "new_desc": ["Paste the property details.", "AI writes it. You review."],
    },
    {
        "task": "LEAD FOLLOW-UP",
        "old_time": "2 HRS",
        "old_desc": ["Manual texts and emails.", "Hoping you missed no one."],
        "new_time": "60 SEC",
        "new_desc": ["AI replies instantly.", "You wake up to booked calls."],
    },
    {
        "task": "CLIENT UPDATES",
        "old_time": "1 HR",
        "old_desc": ["Same 'just checking in'", "email. From scratch. Again."],
        "new_time": "10 MIN",
        "new_desc": ["AI drafts every update.", "You review, tweak, send."],
    },
    {
        "task": "PROSPECT RESEARCH",
        "old_time": "30 MIN",
        "old_desc": ["LinkedIn. Google. Zillow.", "Scrambling to find context."],
        "new_time": "5 MIN",
        "new_desc": ["AI pulls the full picture.", "You go in prepared."],
    },
]


def load_fonts():
    fp = "/System/Library/Fonts/Helvetica.ttc"
    try:
        return {
            "time":  ImageFont.truetype(fp, 118),
            "h2":    ImageFont.truetype(fp, 76),
            "h3":    ImageFont.truetype(fp, 54),
            "body":  ImageFont.truetype(fp, 38),
            "label": ImageFont.truetype(fp, 26),
            "small": ImageFont.truetype(fp, 24),
        }
    except Exception as e:
        print(f"Font warning: {e}")
        d = ImageFont.load_default()
        return {k: d for k in ["time","h2","h3","body","label","small"]}


def base_slide(slide_num, total, f):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 5)], fill=CYAN)
    d.text((M, 38), "@eitanadar.ai", fill=GRAY, font=f["small"])
    d.text((W - M, 38), f"{slide_num}/{total}", fill=GRAY, font=f["small"], anchor="ra")
    return img, d


def glow(d, xy, text, font, color, anchor="la"):
    gc = tuple(min(255, c // 5) for c in color)
    for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
        d.text((xy[0] + dx, xy[1] + dy), text, fill=gc, font=font, anchor=anchor)
    d.text(xy, text, fill=color, font=font, anchor=anchor)


def slide_title(f):
    img, d = base_slide(1, 6, f)

    glow(d, (M, 190), "Agents are", f["h2"], WHITE)
    glow(d, (M, 278), "wasting", f["h2"], WHITE)
    glow(d, (M, 375), "3 HOURS", f["time"], CYAN)
    glow(d, (M, 510), "a day", f["h2"], WHITE)
    glow(d, (M, 598), "on admin.", f["h2"], WHITE)

    d.rectangle([(M, 725), (M + 70, 731)], fill=PINK)

    d.text((M, 760), "Here's what that looks like", fill=GRAY, font=f["body"])
    d.text((M, 810), "with AI vs. without it.", fill=GRAY, font=f["body"])

    # Swipe bar
    d.rectangle([(0, H - 90), (W, H)], fill=DARK)
    d.text((W // 2, H - 45), "Swipe to see the breakdown  →", fill=GRAY, font=f["small"], anchor="mm")

    return img


def slide_before_after(data, slide_num, f):
    img, d = base_slide(slide_num, 6, f)

    # Task header
    d.text((M, 95), data["task"], fill=CYAN, font=f["h3"])
    d.rectangle([(M, 160), (W - M, 163)], fill=DIM)

    # OLD WAY
    d.text((M, 180), "OLD WAY", fill=PINK, font=f["label"])
    glow(d, (M, 215), data["old_time"], f["time"], PINK)

    y = 352
    for line in data["old_desc"]:
        d.text((M, y), line, fill=GRAY, font=f["body"])
        y += 52

    # Center divider
    div_y = 530
    d.rectangle([(M, div_y), (W - M, div_y + 2)], fill=DIM)
    d.ellipse([(M - 7, div_y - 5), (M + 7, div_y + 7)], fill=PINK)
    d.ellipse([(W - M - 7, div_y - 5), (W - M + 7, div_y + 7)], fill=GREEN)

    # NEW WAY
    d.text((M, div_y + 18), "NEW WAY", fill=GREEN, font=f["label"])
    glow(d, (M, div_y + 55), data["new_time"], f["time"], GREEN)

    y = div_y + 192
    for line in data["new_desc"]:
        d.text((M, y), line, fill=WHITE, font=f["body"])
        y += 52

    # Time saved pill
    pill_y = 950
    d.rectangle([(M, pill_y), (M + 420, pill_y + 52)], fill=DARK)
    d.rectangle([(M, pill_y), (M + 420, pill_y + 52)], outline=DIM, width=1)
    d.text((M + 210, pill_y + 26), f"That's {_saved(data['old_time'])} saved on this task alone",
           fill=GRAY, font=f["small"], anchor="mm")

    # Bottom bar
    d.rectangle([(0, H - 90), (W, H)], fill=DARK)
    d.text((W // 2, H - 45), "4 hours back. Every single day.", fill=GRAY, font=f["small"], anchor="mm")

    return img


def _saved(old_time):
    mapping = {"45 MIN": "42 minutes", "2 HRS": "nearly 2 hours",
               "1 HR": "50 minutes", "30 MIN": "25 minutes"}
    return mapping.get(old_time, "significant time")


def slide_cta(f):
    img, d = base_slide(6, 6, f)

    glow(d, (W // 2, 200), "4 HOURS", f["time"], CYAN, anchor="mm")
    glow(d, (W // 2, 330), "BACK.", f["time"], CYAN, anchor="mm")
    d.text((W // 2, 470), "every single day.", fill=GRAY, font=f["h3"], anchor="mm")

    d.rectangle([(M, 560), (W - M, 562)], fill=DIM)

    d.text((W // 2, 615), "Want the full setup guide?", fill=WHITE, font=f["body"], anchor="mm")
    d.text((W // 2, 665), "6 areas. Step by step.", fill=GRAY, font=f["body"], anchor="mm")

    # CTA box
    d.rectangle([(M, 760), (W - M, 940)], fill=DARK)
    d.rectangle([(M, 760), (W - M, 940)], outline=CYAN, width=2)
    d.text((W // 2, 820), "Comment", fill=WHITE, font=f["h3"], anchor="mm")
    glow(d, (W // 2, 885), "PLAYBOOK", f["h3"], CYAN, anchor="mm")

    d.text((W // 2, 990), "and I'll DM it to you.", fill=GRAY, font=f["body"], anchor="mm")

    d.text((W // 2, 1090), "Save this post.", fill=GRAY, font=f["body"], anchor="mm")
    d.text((W // 2, 1140), "You'll want it later.", fill=GRAY, font=f["body"], anchor="mm")

    # Bottom bar
    d.rectangle([(0, H - 110), (W, H)], fill=DARK)
    glow(d, (W // 2, H - 70), "@eitanadar.ai", f["h3"], CYAN, anchor="mm")
    d.text((W // 2, H - 25), "AI automation for real estate", fill=GRAY, font=f["small"], anchor="mm")

    return img


def main():
    out = Path.home() / "Desktop/Woodworks-OS/projects/instagram-carousels/before-after-admin/images"
    out.mkdir(parents=True, exist_ok=True)

    f = load_fonts()
    print("Generating carousel...")

    slides = [slide_title(f)]
    for i, data in enumerate(CONTENT, 2):
        slides.append(slide_before_after(data, i, f))
    slides.append(slide_cta(f))

    for i, img in enumerate(slides, 1):
        p = out / f"slide-{i:02d}.jpg"
        img.save(p, "JPEG", quality=95)
        print(f"  slide-{i:02d}.jpg")

    print(f"\nDone. {len(slides)} slides saved to:\n{out}")
    print("\nTo post:")
    print('  /instagram post ~/Desktop/Woodworks-OS/projects/instagram-carousels/before-after-admin/images/ "<caption>" <api_key>')


if __name__ == "__main__":
    main()
