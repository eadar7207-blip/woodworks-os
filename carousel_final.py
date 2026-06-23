#!/usr/bin/env python3
"""Professional Instagram carousel inspired by premium real estate design."""

from PIL import Image, ImageDraw
from pathlib import Path

# Premium colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (240, 240, 240)
ACCENT = (100, 200, 255)  # Professional blue (not neon)
ACCENT_DARK = (70, 150, 220)

PROMPTS = [
    {
        "headline": "Lead\nQualification",
        "subtitle": "Ask 3 questions. Instantly know if they're serious.",
        "detail": "Save 5+ hours qualifying leads every week"
    },
    {
        "headline": "Proposal\nGeneration",
        "subtitle": "2 minutes. Not 2 hours.",
        "detail": "Professional proposals that close deals faster"
    },
    {
        "headline": "Email\nSequences",
        "subtitle": "Write follow-ups that actually get responses.",
        "detail": "Higher reply rates. Consistent follow-up."
    },
    {
        "headline": "CRM\nOrganization",
        "subtitle": "Analyze your data. Find hot leads.",
        "detail": "Know who's stale, who's hot, who's closing"
    },
    {
        "headline": "Client\nCommunication",
        "subtitle": "Say the right thing at the right time.",
        "detail": "Handle objections. Keep deals alive."
    }
]

def create_slide(num, data):
    """Create professional carousel slide."""
    img = Image.new('RGB', (1080, 1350), WHITE)
    draw = ImageDraw.Draw(img)
    
    # Username at top
    draw.text((80, 60), "@eitanadar.ai", fill=DARK_GRAY, font=None)
    draw.text((900, 60), f"{num}/5", fill=LIGHT_GRAY, font=None, anchor="rt")
    
    # Thin accent line
    draw.rectangle([(0, 120), (1080, 125)], fill=ACCENT)
    
    # Large headline (split across lines)
    draw.text((80, 250), data["headline"], fill=BLACK, font=None)
    
    # Subtitle
    draw.text((80, 550), data["subtitle"], fill=ACCENT, font=None)
    
    # Detail text
    draw.text((80, 700), data["detail"], fill=DARK_GRAY, font=None)
    
    # Bottom bar with CTA
    draw.rectangle([(0, 1150), (1080, 1350)], fill=LIGHT_GRAY)
    draw.text((540, 1200), "AI Prompts for Real Estate Pros", fill=DARK_GRAY, font=None, anchor="mm")
    draw.text((540, 1280), "Follow @eitanadar.ai for daily automation tips", fill=ACCENT_DARK, font=None, anchor="mm")
    
    return img

def main():
    """Generate carousel."""
    carousel_dir = Path.home() / "Desktop" / "Woodworks-OS" / "projects" / "instagram-carousels" / "realtor-prompts-5-slides-final" / "images"
    carousel_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear old
    for f in carousel_dir.glob("*.jpg"):
        f.unlink()
    
    print("🎨 Creating premium carousel...")
    
    for i, data in enumerate(PROMPTS, 1):
        img = create_slide(i, data)
        path = carousel_dir / f"slide-{i:02d}.jpg"
        img.save(path, "JPEG", quality=95)
        print(f"  ✓ Slide {i}/5: {data['headline'].replace(chr(10), ' ')}")
    
    print("\n✅ Professional carousel ready!")
    print(f"📁 {carousel_dir}")
    print("\nPost to Instagram:")
    print("  /post realtor-prompts-5-slides-final")

if __name__ == "__main__":
    main()
