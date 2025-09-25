import os
import random
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise SystemExit("TELEGRAM_TOKEN not set in .env!")

SUPPORT_MESSAGES = [
    "Ты справляешься лучше, чем думаешь.",
    "Я рядом — если нужно, напиши.",
    "Позволь себе паузу. Ты делаешь достаточно.",
    "Ошибки — это часть пути. У тебя получится.",
    "Маленькие победы — тоже победы.",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chats = context.application.bot_data.setdefault("chats", set())
    chats.add(chat_id)
    await update.message.reply_text(
        "Привет! Я бот поддержки.\n\n"
        "/support — получить поддержляющее сообщение прямо сейчас\n\n"
        "Теперь я буду присылать поддерживающее сообщение каждый час."
    )

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(SUPPORT_MESSAGES))

async def keyword_listener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    keywords = ["плохо", "тяжело", "не могу", "устал", "один", "одинка", "депресс", "хочется"]
    if any(k in text for k in keywords):
        await update.message.reply_text(random.choice(SUPPORT_MESSAGES))

async def hourly_notification(context: ContextTypes.DEFAULT_TYPE):
    chats = context.application.bot_data.get("chats", set())
    for chat_id in chats:
        await context.bot.send_message(chat_id=chat_id, text=random.choice(SUPPORT_MESSAGES))

async def main():
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("support", support))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, keyword_listener))

    # JobQueue
    app.job_queue.run_repeating(hourly_notification, interval=3600, first=3600)

    print("Bot started. Press Ctrl+C to stop.")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
