import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Получить поддержку прямо сейчас", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я твой бот поддержки 💛", reply_markup=reply_markup)

async def send_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(SUPPORT_MESSAGES)
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(msg)
    else:
        await update.message.reply_text(msg)

async def hourly_support(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in context.bot_data.get("chats", []):
        await context.bot.send_message(chat_id=chat_id, text=random.choice(SUPPORT_MESSAGES))

async def register_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chats = context.bot_data.setdefault("chats", set())
    chats.add(chat_id)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(send_support, pattern="support"))
    app.add_handler(CommandHandler("support", send_support))
    app.add_handler(CommandHandler("register", register_chat))

    # Запуск часовой рассылки
    app.job_queue.run_repeating(hourly_support, interval=3600, first=3600)

    app.run_polling()

if __name__ == "__main__":
    main()


