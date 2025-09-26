import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

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
    await query.message.reply_text(random.choice(support_messages))

async def hourly_support(context: ContextTypes.DEFAULT_TYPE):
    chat_ids = context.bot_data.get("chat_ids", set())
    for chat_id in chat_ids:
        await context.bot.send_message(chat_id=chat_id, text=random.choice(support_messages))

async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if "chat_ids" not in context.bot_data:
        context.bot_data["chat_ids"] = set()
    context.bot_data["chat_ids"].add(chat_id)
    await update.message.reply_text("Ты добавлен в рассылку поддержки!")

def main():
    app = Application.builder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("track", track_users))
    app.add_handler(CallbackQueryHandler(support_callback, pattern="support_now"))

    # JobQueue
    app.job_queue.run_repeating(hourly_support, interval=3600, first=3600)

    app.run_polling()

if __name__ == "__main__":
    main()
