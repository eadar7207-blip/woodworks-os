import logging
import os
from pathlib import Path

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

DOWNLOAD_DIR = Path(__file__).resolve().parent / "telegram_downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello! I can save images, documents, and text for you. "
        "Send me a photo, document, or message and I will save it in telegram_downloads."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/start - welcome message\n"
        "/help - this help text\n"
        "Send an image or document and I will save it locally."
    )

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    saved_files = []

    if message.photo:
        photo = message.photo[-1]
        file = await photo.get_file()
        filename = DOWNLOAD_DIR / f"photo_{photo.file_unique_id}.jpg"
        await file.download_to_drive(custom_path=str(filename))
        saved_files.append(filename.name)

    if message.document:
        document = message.document
        file = await document.get_file()
        filename = DOWNLOAD_DIR / document.file_name
        await file.download_to_drive(custom_path=str(filename))
        saved_files.append(filename.name)

    if message.text and not (message.photo or message.document):
        filename = DOWNLOAD_DIR / f"message_{message.message_id}.txt"
        filename.write_text(message.text, encoding="utf-8")
        saved_files.append(filename.name)

    if saved_files:
        await update.message.reply_text(
            "Saved files: " + ", ".join(saved_files)
        )
    else:
        await update.message.reply_text("I did not recognize this content type.")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Sorry, I didn\'t understand that command.")

def main() -> None:
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise RuntimeError(
            "Set TELEGRAM_BOT_TOKEN environment variable or replace YOUR_BOT_TOKEN_HERE in telegram_bot.py"
        )

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL | filters.TEXT, handle_media))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("Starting Telegram bot...")
    application.run_polling()


if __name__ == "__main__":
    main()
