# Telegram Bot Setup

This repository includes a minimal Telegram bot in `telegram_bot.py`.

## Create the bot

1. Open Telegram and chat with `@BotFather`.
2. Send `/newbot`.
3. Give your bot a name.
4. Give your bot a username ending in `bot`.
5. Copy the token that BotFather returns.

## Configure the bot

Set the environment variable with your token:

```bash
export TELEGRAM_BOT_TOKEN="123456789:ABCdefGhIJKlmNoPQRsTuvWXyZ"
```

## Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

## Run the bot

```bash
python3 telegram_bot.py
```

## What it does

- `/start` sends a welcome message.
- `/help` shows usage instructions.
- Sending a photo or document saves the file under `telegram_downloads/`.
- Sending plain text saves the text to a `.txt` file.

## Notes

- The bot runs with polling, so keep the script running while you use Telegram.
- If you want to use a Telegram bot for file transfer, send files to it from your phone, and then retrieve them from the `telegram_downloads/` folder on this computer.
