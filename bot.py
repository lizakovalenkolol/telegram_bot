# bot.py
import asyncio
import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не задан!")

support_messages = [
    "Ты делаешь достаточно",
    "Всё будет хорошо",
    "Скоро всё получится",
    "У тебя уже получается",
    "Ты не одна",
    "Ты справляешься",
    "Помни: ты делаешь достаточно",
    "Маленькие победы тоже важны"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Получить поддержку прямо сейчас", callback_data="support_now")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Нажми кнопку ниже, чтобы получить поддержку:", reply_markup=reply_markup)

async def support_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    message = random.choice(support_messages)
    await query.message.reply_text(message)

async def hourly_support(context: ContextTypes.DEFAULT_TYPE):
    # Отправляем сообщение всем, кто стартовал бота
    for chat_id in context.bot_data.get("chat_ids", []):
        await context.bot.send_message(chat_id=chat_id, text=random.choice(support_messages))

async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if "chat_ids" not in context.bot_data:
        context.bot_data["chat_ids"] = set()
    context.bot_data["chat_ids"].add(chat_id)

def main():
    app = Application.builder().token(TOKEN).build()

    # Хэндлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(support_callback, pattern="support_now"))
    app.add_handler(CommandHandler("track", track_users))  # можно вызвать командой /track чтобы добавлять в рассылку

    # JobQueue для уведомлений каждый час
    app.job_queue.run_repeating(hourly_support, interval=3600, first=3600)

    app.run_polling()

if __name__ == "__main__":
    main()
