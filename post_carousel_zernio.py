#!/usr/bin/env python3
"""Post carousel to Instagram via Zernio API."""

import requests
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
ZERNIO_API_KEY = "sk_e408f417d0a321a0e6503486412dc0d5abac8fa6b592d6794825bdd48600bc55"
ZERNIO_API_URL = "https://api.zernio.com/v1"

# Colors
COLORS = {
    "bg": (10, 14, 39),      # Dark navy
    "cyan": (0, 255, 255),    # Neon cyan
    "pink": (255, 0, 110),    # Neon pink
    "green": (57, 255, 20),   # Neon green
    "white": (255, 255, 255), # White
}

# Carousel content - 10 slides
CAROUSEL = {
    "title": "15 Powerful Prompts Realtors Should Use",
    "slides": [
        {
            "num": "1",
            "heading": "Lead Qualification",
            "content": "Ask 3 questions instantly:\n\n1) Serious buyer or browser?\n2) Likely budget range?\n3) Best next step?\n\nSave 5 hours/week",
            "emoji": "🎯"
        },
        {
            "num": "2", 
            "heading": "Proposal Generation",
            "content": "Generate custom proposals\nin 2 minutes instead of 2 hours\n\nProfessional. Impressive.\nPersonalized.",
            "emoji": "📄"
        },
        {
            "num": "3",
            "heading": "Email Sequences",
            "content": "5 templates that actually\nget responses\n\nNot generic. Not spammy.\nJust honest & helpful.",
            "emoji": "📧"
        },
        {
            "num": "4",
            "heading": "CRM Organization",
            "content": "Keep your lead data clean:\n\n• Which leads are stale?\n• Who needs follow-up?\n• What's close to closing?\n\nStay organized.",
            "emoji": "📊"
        },
        {
            "num": "5",
            "heading": "Listing Descriptions",
            "content": "Write compelling descriptions\nthat SELL homes\n\nTell the story. Not just\nthe features.",
            "emoji": "🏠"
        },
        {
            "num": "6",
            "heading": "Negotiation Scripts",
            "content": "Master these scripts:\n\n• Handle low-ball offers\n• Manage emotional sellers\n• Close deals faster\n\nNegotiate with confidence.",
            "emoji": "💰"
        },
        {
            "num": "7",
            "heading": "Market Analysis",
            "content": "Instant market reports\n(no 2-hour research sessions)\n\nPrice trends • Buyer profiles\nEmerging opportunities",
            "emoji": "📈"
        },
        {
            "num": "8",
            "heading": "Social Media Content",
            "content": "5 daily posts that build\nyour authority\n\nInsightful. Not salesy.\nConsistent.",
            "emoji": "📱"
        },
        {
            "num": "9",
            "heading": "Client Communication",
            "content": "Say the right thing\nat the right time:\n\n• Cold feet? Here's the script.\n• Bad news? Here's how.\n• Closing? Celebrate right.",
            "emoji": "💬"
        },
        {
            "num": "10",
            "heading": "Save These Prompts",
            "content": "@eitanadar.ai\n\nMore real estate automation\nstrategy & prompts in bio 🚀\n\nTag someone who needs this",
            "emoji": "⭐"
        }
    ]
}

def create_slide(slide_num, slide_data):
    """Create a single carousel slide."""
    img = Image.new('RGB', (1080, 1350), COLORS["bg"])
    draw = ImageDraw.Draw(img)
    
    # Use default font (monospace for better text)
    title_font_size = 50
    heading_font_size = 60
    body_font_size = 36
    
    # Slide number (top left)
    draw.text((60, 60), f"SLIDE {slide_num}", fill=COLORS["cyan"], font=None)
    
    # Emoji (large, center top)
    draw.text((1080//2, 200), slide_data["emoji"], fill=COLORS["white"], font=None)
    
    # Heading (center)
    heading = slide_data["heading"]
    draw.text((1080//2, 350), heading, fill=COLORS["cyan"], font=None, anchor="mm")
    
    # Content (center, multi-line)
    content = slide_data["content"]
    lines = content.split('\n')
    y_pos = 600
    for line in lines:
        draw.text((1080//2, y_pos), line.strip(), fill=COLORS["white"], font=None, anchor="mm")
        y_pos += 80
    
    # CTA at bottom
    draw.text((1080//2, 1250), "@eitanadar.ai", fill=COLORS["green"], font=None, anchor="mm")
    
    return img

def create_carousel_images():
    """Generate all 10 carousel images."""
    carousel_dir = Path.home() / "Desktop" / "Woodworks-OS" / "projects" / "instagram-carousels" / "realtor-prompts-10-slides" / "images"
    carousel_dir.mkdir(parents=True, exist_ok=True)
    
    image_paths = []
    for i, slide_data in enumerate(CAROUSEL["slides"], 1):
        img = create_slide(i, slide_data)
        path = carousel_dir / f"slide-{i:02d}.jpg"
        img.save(path, "JPEG", quality=95)
        image_paths.append(str(path))
        print(f"✓ Created slide {i}/10")
    
    return image_paths

def post_carousel(image_paths):
    """Post carousel to Instagram via Zernio API."""
    
    headers = {
        "Authorization": f"Bearer {ZERNIO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prepare carousel payload
    payload = {
        "type": "carousel",
        "images": image_paths,
        "caption": "15 powerful prompts every realtor should use for lead automation, CRM, proposals, and client communication. Save 10+ hours/week. 🤖 #RealEstate #Automation #RealEstateMarketing",
        "platform": "instagram"
    }
    
    print(f"\n📤 Posting carousel via Zernio API...")
    print(f"Images: {len(image_paths)} slides")
    print(f"Caption: {payload['caption'][:80]}...")
    
    try:
        # Post to Zernio
        response = requests.post(
            f"{ZERNIO_API_URL}/posts",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"\n✅ SUCCESS! Carousel posted to @eitanadar.ai")
            print(f"Post ID: {result.get('id')}")
            print(f"Status: {result.get('status')}")
            return True
        else:
            print(f"\n❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error posting: {str(e)}")
        return False

def main():
    print("🎨 Creating 10-slide carousel...")
    print("=" * 60)
    
    # Create images
    image_paths = create_carousel_images()
    
    print(f"\n{'=' * 60}")
    print(f"✅ All 10 slides created!")
    print(f"Location: ~/Desktop/Woodworks-OS/projects/instagram-carousels/realtor-prompts-10-slides/images/")
    
    # Post to Instagram
    print(f"\n{'=' * 60}")
    success = post_carousel(image_paths)
    
    if success:
        print(f"\n{'=' * 60}")
        print("🎉 CAROUSEL POSTED TO INSTAGRAM!")
        print("Check @eitanadar.ai to see your carousel live")
    else:
        print("\n⚠️ Carousel images created but posting failed.")
        print("You can post manually via Zernio dashboard if needed.")

if __name__ == "__main__":
    main()
