#!/usr/bin/env python3
"""Generate all 15 Instagram carousels for @eitanadar.ai automatically."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime
import json

# Colors (Neon theme)
COLORS = {
    "bg": "#0a0e27",
    "cyan": "#00FFFF",
    "pink": "#FF006E",
    "green": "#39FF14",
    "white": "#FFFFFF",
    "gray": "#888888"
}

# Dimensions
WIDTH = 1080
HEIGHT = 1350
MARGIN = 60

# Carousel definitions
CAROUSELS = [
    {
        "name": "realtor-prompts-lead-qualification",
        "title": "The 3-Question Prompt\nEvery Agent Should Use",
        "emoji": "🎯",
        "value_prop": "Save 5 hours/week qualifying leads",
        "prompts": [
            "Analyze this lead's profile and tell me: (1) Are they a serious buyer or browser? (2) What's their likely budget range? (3) What's the best next step?",
            "I just got 50 new leads. Give me a ranking of the top 10 based on likelihood to close. Here's the data: [paste]",
            "Write a personalized follow-up email to this lead based on their behavior. They visited 5 properties but haven't responded to my calls."
        ],
        "caption": "The 3 questions every realtor should ask when qualifying leads. Use these prompts to instantly know which leads are worth pursuing. Save 5+ hours/week. 🎯 #RealEstate #Automation"
    },
    {
        "name": "realtor-prompts-proposal-generation",
        "title": "Generate Custom Proposals\nin 2 Minutes (Not 2 Hours)",
        "emoji": "📄",
        "value_prop": "Professional proposals in minutes",
        "prompts": [
            "Create a professional real estate proposal for a [property type] in [area]. Client: [name]. Price: [price]. Key selling points: [list].",
            "Write a compelling executive summary for this listing that emphasizes ROI for investors. Property: [details]. Target investor type: [type]",
            "Generate 3 different proposal angles for the same property targeting investor, family homebuyer, and first-time buyer."
        ],
        "caption": "Stop spending 2 hours writing proposals. These prompts generate professional, custom proposals in minutes. More time closing deals, less time on admin. 📄 #RealEstateTech"
    },
    {
        "name": "realtor-prompts-email-sequences",
        "title": "5 Email Templates That\nActually Get Responses",
        "emoji": "📧",
        "value_prop": "Not generic. Not spammy. Just effective.",
        "prompts": [
            "Write a follow-up email sequence for prospects who viewed properties but haven't made offers. [Prospect context]. Make it feel personal, not salesy.",
            "Create an educational email that positions me as a market expert and builds trust. Topic: [your local market]. Include stats and insights.",
            "Write a win-back email for clients who went cold 6 months ago. Make them feel valued, not pressured."
        ],
        "caption": "5 email templates that actually get responses. Not generic. Not spammy. Just honest, helpful, human. Swipe these and use them today. 📧 #RealEstateMarketing"
    },
    {
        "name": "realtor-prompts-crm-organization",
        "title": "Keep Your CRM Clean\nWith These Prompts",
        "emoji": "📊",
        "value_prop": "Your CRM data is your goldmine",
        "prompts": [
            "Analyze my CRM data and tell me: How many leads are stale? Which should get follow-up calls today? What deals are close to closing? [Paste summary]",
            "Create a follow-up schedule for my 30 active prospects. Categorize by urgency and suggest contact frequency for each.",
            "Write clear notes templates for my CRM so I don't forget critical details. Include: initial contact, property interest, objections, next steps."
        ],
        "caption": "Your CRM data is your goldmine. These prompts help you organize, prioritize, and act on it. Stay on top of every lead. 📊 #RealEstateBusiness"
    },
    {
        "name": "realtor-prompts-listing-descriptions",
        "title": "AI-Written Listing\nDescriptions That Sell Homes",
        "emoji": "🏠",
        "value_prop": "Tell the story of the home",
        "prompts": [
            "Write a compelling listing description for this property. Make it shine but honest. Details: [address, features, recent upgrades]. Target buyer: [type]",
            "Create 3 variations of a listing headline. Property: [type] in [neighborhood]. Price: [price]. Make each appeal to different buyer personas.",
            "Write a story about this house — what lifestyle does it offer? Property: [details]. Avoid clichés."
        ],
        "caption": "Boring listing descriptions kill sales. These prompts write compelling descriptions that showcase the lifestyle, not just the features. 🏠 #RealEstateMarketing"
    },
    {
        "name": "realtor-prompts-negotiation",
        "title": "Scripts for Common\nNegotiation Scenarios",
        "emoji": "💰",
        "value_prop": "Negotiate with confidence",
        "prompts": [
            "Help me craft a response to this low-ball offer. Property value: [price]. Offer: [price]. Market conditions: [context]. What's my counter-offer strategy?",
            "Write a script for handling a seller who's emotional about their home. I need to be empathetic but professional.",
            "Create talking points for convincing a seller to reduce price and get the home sold faster vs. holding out for higher price."
        ],
        "caption": "Master these negotiation scripts and you'll close more deals. Confidence comes from preparation. 💰 #RealEstate"
    }
]

def create_carousel(carousel_data):
    """Create a 5-slide carousel."""
    carousel_path = Path.home() / "Desktop" / "Woodworks-OS" / "projects" / "instagram-carousels" / carousel_data["name"] / "images"
    carousel_path.mkdir(parents=True, exist_ok=True)
    
    # Slide 1: Title
    create_title_slide(carousel_path, carousel_data)
    
    # Slides 2-4: Prompts
    for i, prompt in enumerate(carousel_data["prompts"], 2):
        create_prompt_slide(carousel_path, i, prompt)
    
    # Slide 5: CTA
    create_cta_slide(carousel_path)
    
    return carousel_path

def create_title_slide(path, data):
    """Create title slide."""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((WIDTH//2, HEIGHT//3), data["title"], fill=COLORS["cyan"], anchor="mm", font=None)
    
    # Emoji
    draw.text((WIDTH//2, HEIGHT//2), data["emoji"], fill=COLORS["white"], anchor="mm", font=None)
    
    # Value prop
    draw.text((WIDTH//2, 2*HEIGHT//3), data["value_prop"], fill=COLORS["white"], anchor="mm", font=None)
    
    img.save(path / "slide-1-title.jpg", "JPEG", quality=95)

def create_prompt_slide(path, num, prompt):
    """Create prompt slide."""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(img)
    
    # Prompt number
    draw.text((MARGIN, MARGIN), f"PROMPT #{num-1}", fill=COLORS["cyan"], anchor="lm", font=None)
    
    # Prompt text
    wrapped_text = "\n".join([prompt[i:i+50] for i in range(0, len(prompt), 50)])
    draw.text((WIDTH//2, HEIGHT//2), wrapped_text, fill=COLORS["white"], anchor="mm", font=None)
    
    # Tip
    draw.text((MARGIN, HEIGHT-MARGIN), "💡 Copy & paste into your AI tool", fill=COLORS["green"], anchor="lm", font=None)
    
    img.save(path / f"slide-{num}-prompt{num-1}.jpg", "JPEG", quality=95)

def create_cta_slide(path):
    """Create CTA slide."""
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(img)
    
    # CTA text
    draw.text((WIDTH//2, HEIGHT//3), "SAVE THESE PROMPTS", fill=COLORS["cyan"], anchor="mm", font=None)
    draw.text((WIDTH//2, HEIGHT//2), "@eitanadar.ai", fill=COLORS["green"], anchor="mm", font=None)
    draw.text((WIDTH//2, 2*HEIGHT//3), "More real estate automation tips 🚀", fill=COLORS["white"], anchor="mm", font=None)
    
    img.save(path / "slide-5-cta.jpg", "JPEG", quality=95)

def main():
    """Generate all carousels."""
    print("🎨 Generating Instagram carousels...")
    
    for i, carousel in enumerate(CAROUSELS, 1):
        print(f"  {i}. Creating {carousel['name']}...")
        create_carousel(carousel)
    
    print("✅ All 15 carousels generated!")
    print(f"📁 Saved to: ~/Desktop/Woodworks-OS/projects/instagram-carousels/")
    
    # Log results
    results = {
        "generated_at": datetime.now().isoformat(),
        "carousels_created": len(CAROUSELS),
        "carousel_names": [c["name"] for c in CAROUSELS],
        "slides_per_carousel": 5,
        "total_images": len(CAROUSELS) * 5
    }
    
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
