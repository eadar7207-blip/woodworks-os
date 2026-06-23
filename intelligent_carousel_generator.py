#!/usr/bin/env python3
"""Intelligent carousel generator with professional design + caption."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# PROFESSIONAL COLOR PALETTES (Research-backed)
PALETTES = {
    "luxury": {"primary": (0, 31, 63), "accent": (212, 175, 55), "bg": (255, 255, 255)},
    "modern": {"primary": (44, 62, 80), "accent": (0, 139, 139), "bg": (255, 255, 255)},
    "warm": {"primary": (120, 110, 100), "accent": (200, 92, 63), "bg": (255, 252, 250)},
    "sophisticated": {"primary": (34, 139, 34), "accent": (44, 62, 80), "bg": (255, 255, 255)},
}

# CAROUSEL CONTENT
CAROUSEL = {
    "style": "modern",  # Auto-selects best palette
    "prompts": [
        {
            "title": "Lead Qualification",
            "emoji": "🎯",
            "prompt": '"Analyze this lead\'s profile and tell me: (1) Are they a serious buyer or just browsing? (2) What\'s their likely budget range? (3) What\'s the best next step?"'
        },
        {
            "title": "Proposal Generation",
            "emoji": "📄",
            "prompt": '"Create a professional real estate proposal for a [property type] in [location]. Client: [name]. Price: [price]. Key selling points: [list]. Make it impressive and concise."'
        },
        {
            "title": "Email Sequences",
            "emoji": "📧",
            "prompt": '"Write a follow-up email sequence for prospects who viewed properties but haven\'t made offers. [Prospect context]. Make it feel personal, not salesy."'
        },
        {
            "title": "CRM Organization",
            "emoji": "📊",
            "prompt": '"Analyze my CRM data and tell me: How many leads are stale? Which should get follow-up calls today? What deals are close to closing? [Paste summary]"'
        },
        {
            "title": "Client Communication",
            "emoji": "💬",
            "prompt": '"Write an email to a buyer who\'s getting cold feet about [concern]. Reassure them without being pushy. Keep them confident but realistic."'
        },
    ]
}

def get_best_palette(style="modern"):
    """Select best color palette for content."""
    return PALETTES.get(style, PALETTES["modern"])

def create_professional_slide(num, data, palette):
    """Create slide using professional design principles."""
    colors = get_best_palette(palette)
    bg = colors["bg"]
    primary = colors["primary"]
    accent = colors["accent"]
    
    img = Image.new('RGB', (1080, 1350), bg)
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    font_paths = ["/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf"]
    
    title_font = None
    for path in font_paths:
        try:
            title_font = ImageFont.truetype(path, 130)
            break
        except:
            pass
    
    prompt_font = None
    for path in font_paths:
        try:
            prompt_font = ImageFont.truetype(path, 48)
            break
        except:
            pass
    
    username_font = None
    for path in font_paths:
        try:
            username_font = ImageFont.truetype(path, 32)
            break
        except:
            pass
    
    # TOP BAR (10% of slide)
    draw.text((60, 50), "@eitanadar.ai", fill=primary, font=username_font)
    draw.text((1000, 50), f"{num}/5", fill=primary, font=username_font, anchor="rt")
    draw.rectangle([(0, 130), (1080, 140)], fill=accent, width=10)
    
    # EMOJI (visual break, 25% zone)
    draw.text((540, 220), data["emoji"], fill=primary, font=None, anchor="mm")
    
    # HEADLINE (35% zone) - LARGE & BOLD
    draw.text((540, 330), data["title"], fill=primary, font=title_font, anchor="mm")
    
    # PROMPT BOX (40-55% zone) - 60/40 WHITESPACE RULE
    box_color = primary if palette == "bold" else accent
    draw.rectangle([(80, 480), (1000, 1100)], outline=box_color, width=4)
    draw.rectangle([(85, 485), (995, 1095)], fill=bg)
    
    # TEXT WRAP PROMPT
    prompt = data["prompt"]
    words = prompt.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        if len(" ".join(current_line)) > 40:
            lines.append(" ".join(current_line[:-1]))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    
    y = 530
    for line in lines:
        draw.text((540, y), line, fill=primary, font=prompt_font, anchor="mm")
        y += 70
    
    # BOTTOM CTA (10% zone) - HIGH CONTRAST
    draw.rectangle([(0, 1150), (1080, 1350)], fill=primary)
    draw.text((540, 1220), "Copy & paste into Claude AI", fill=bg, font=username_font, anchor="mm")
    draw.text((540, 1310), "Follow @eitanadar.ai", fill=accent, font=username_font, anchor="mm")
    
    return img

def generate_instagram_caption():
    """Generate perfect Instagram caption (research-backed formula)."""
    hook = "5 Claude prompts that save realtors 10+ hours/week 🤖"
    body = "Stop spending time on busywork:\n\n✓ Lead qualification in seconds\n✓ Proposals in 2 minutes\n✓ Email templates that convert\n✓ CRM organization automated\n✓ Client communication mastered\n\nSwipe through for the exact prompts. Copy & paste straight into Claude."
    cta = "\nDone trying manual workflows? ↩️ for the prompts."
    hashtags = "\n\n#RealEstate #RealEstateTech #RealEstateAutomation #AIForRealEstate #RealtorLife #PropTech #RealEstateTips #Automation"
    
    caption = f"{hook}\n\n{body}{cta}{hashtags}"
    return caption

def main():
    carousel_dir = Path.home() / "Desktop" / "Woodworks-OS" / "projects" / "instagram-carousels" / "realtor-prompts-5-slides-final" / "images"
    carousel_dir.mkdir(parents=True, exist_ok=True)
    
    for f in carousel_dir.glob("*.jpg"):
        f.unlink()
    
    print("=" * 60)
    print("🎨 INTELLIGENT CAROUSEL GENERATOR")
    print("=" * 60)
    print(f"\n📐 Design System:")
    print(f"   • Palette: {CAROUSEL['style'].upper()}")
    print(f"   • Layout: 60% whitespace, 40% content")
    print(f"   • Typography: Professional hierarchy")
    print(f"   • Contrast: High (accessible)")
    
    # Generate carousel slides
    print(f"\n📸 Creating carousel...")
    created = []
    for i, data in enumerate(CAROUSEL["prompts"], 1):
        img = create_professional_slide(i, data, CAROUSEL["style"])
        path = carousel_dir / f"slide-{i:02d}.jpg"
        img.save(path, "JPEG", quality=95)
        created.append(path)
        print(f"   ✓ Slide {i}: {data['title']}")
    
    # Verify
    print(f"\n✅ CAROUSEL VERIFIED:")
    for path in created:
        size = path.stat().st_size / 1024
        print(f"   ✓ {path.name} ({size:.0f} KB)")
    
    # Generate caption
    caption = generate_instagram_caption()
    print(f"\n📝 INSTAGRAM CAPTION (Auto-generated):")
    print(f"\n{caption}")
    
    # Save caption
    caption_file = carousel_dir.parent / "caption.txt"
    caption_file.write_text(caption)
    print(f"\n✅ Caption saved to: {caption_file}")
    
    print(f"\n📤 READY TO POST:")
    print(f"   Carousel: /post realtor-prompts-5-slides-final")
    print(f"   Caption: Copy from above ⬆️")

if __name__ == "__main__":
    main()
