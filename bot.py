import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters, JobQueue
)

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не задан!")

SUPPORT_MESSAGES = [
    "Ты делаешь достаточно",
    "Всё будет хорошо",
    "Скоро всё получится",
    "У тебя уже получается",
    "Ты не одна",
    "Ты справляешься",
    "Помни: ты делаешь достаточно",
    "Маленькие победы тоже важны"
]

active_chats = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    active_chats.add(chat_id)
    keyboard = [[InlineKeyboardButton("Получить поддержку прямо сейчас", callback_data="SUPPORT_NOW")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я буду присылать поддержку каждый час.\nНажми кнопку, чтобы получить поддержку прямо сейчас.",
        reply_markup=reply_markup
    )

async def support_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    message = random.choice(SUPPORT_MESSAGES)
    await query.message.reply_text(message)

async def keyword_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    keywords = ["помощь", "поддержка", "не могу", "плохо", "тяжело", "один", "устала"]
    if any(word in text for word in keywords):
        message = random.choice(SUPPORT_MESSAGES)
        await update.message.reply_text(message)

async def hourly_support(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in active_chats:
        await context.bot.send_message(chat_id=chat_id, text=random.choice(SUPPORT_MESSAGES))

def main():
    app = Application.builder().token(TOKEN).build()

    # Хендлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(support_now, pattern="SUPPORT_NOW"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, keyword_handler))

    # Фоновые задачи: каждый час
    app.job_queue.run_repeating(hourly_support, interval=3600, first=3600)

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()

