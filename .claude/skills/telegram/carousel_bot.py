#!/usr/bin/env python3
"""Telegram bot for Instagram carousel posting via Instagrapi."""

import logging
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from instagrapi import Client
import json

BOT_TOKEN = "8779220832:AAEQKWGGntYISslIelMLUy6UH_IjFP0eZbc"
CAROUSEL_BASE_PATH = Path.home() / "Desktop" / "Woodworks-OS" / "projects" / "instagram-carousels"

# Instagram credentials - UPDATE THESE
INSTAGRAM_USERNAME = "eitanadar.ai"
INSTAGRAM_PASSWORD = "T14082002d"  # Replace with actual password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instagram client
ig_client = None

def init_instagram():
    """Initialize Instagram client."""
    global ig_client
    try:
        ig_client = Client()
        ig_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        logger.info("✅ Instagram authenticated")
        return True
    except Exception as e:
        logger.error(f"❌ Instagram auth failed: {str(e)}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Carousel Bot**\n\n"
        "Post carousels to @eitanadar.ai\n\n"
        "/list - See carousels\n"
        "/post name - Post carousel\n\n"
        "Example: `/post realtor-prompts-10-slides`",
        parse_mode="Markdown"
    )

async def list_carousels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    carousels = [d.name for d in CAROUSEL_BASE_PATH.iterdir() if d.is_dir()] if CAROUSEL_BASE_PATH.exists() else []
    
    if not carousels:
        await update.message.reply_text("❌ No carousels found")
        return
    
    msg = "📁 **Available Carousels:**\n\n"
    for c in sorted(carousels):
        path = CAROUSEL_BASE_PATH / c / "images"
        count = len(list(path.glob("*.jpg")) + list(path.glob("*.png"))) if path.exists() else 0
        msg += f"• `{c}` ({count} slides)\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")

async def post_carousel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ig_client
    
    if not context.args or len(context.args) == 0:
        await update.message.reply_text("❌ Usage: `/post carousel_name`", parse_mode="Markdown")
        return
    
    carousel_name = " ".join(context.args)
    carousel_path = CAROUSEL_BASE_PATH / carousel_name / "images"
    
    if not carousel_path.exists():
        await update.message.reply_text(f"❌ Carousel not found: `{carousel_name}`", parse_mode="Markdown")
        return
    
    images = sorted(list(carousel_path.glob("*.jpg")) + list(carousel_path.glob("*.png")))
    
    if not images:
        await update.message.reply_text("❌ No images in carousel", parse_mode="Markdown")
        return
    
    await update.message.reply_text(f"📤 Posting `{carousel_name}` ({len(images)} slides)...", parse_mode="Markdown")
    
    try:
        if not ig_client:
            await update.message.reply_text("❌ Instagram not connected. Check bot credentials.")
            return
        
        # Convert paths to strings
        image_paths = [str(img) for img in images]
        
        # Post carousel
        caption = "15 powerful prompts every realtor should use for lead automation, CRM, proposals, and client communication. Save 10+ hours/week. 🤖 #RealEstate #Automation #RealEstateMarketing"
        
        media = ig_client.album_upload(image_paths, caption=caption)
        
        await update.message.reply_text(
            f"✅ **Posted to Instagram!**\n\n"
            f"Carousel: `{carousel_name}`\n"
            f"Slides: {len(images)}\n"
            f"Status: Published 🎉",
            parse_mode="Markdown"
        )
        logger.info(f"✅ Posted: {carousel_name} ({len(images)} images)")
        
    except Exception as e:
        error_msg = str(e)
        await update.message.reply_text(f"❌ Error: {error_msg[:100]}")
        logger.error(f"Post failed: {error_msg}")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Carousel Bot Commands**\n\n"
        "/start - Welcome\n"
        "/list - List carousels\n"
        "/post name - Post carousel to Instagram",
        parse_mode="Markdown"
    )

def main():
    print("🤖 Starting Carousel Bot...")
    
    # Initialize Instagram
    if not init_instagram():
        print("❌ Failed to authenticate with Instagram")
        print("Update bot with correct Instagram credentials!")
        return
    
    print("✅ Bot ready!")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_carousels))
    app.add_handler(CommandHandler("post", post_carousel))
    app.add_handler(CommandHandler("help", help_cmd))
    
    print("📱 Bot running! Message @eitanadar_carousel_bot in Telegram")
    app.run_polling()

if __name__ == '__main__':
    main()
