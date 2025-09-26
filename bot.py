import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Получаем токен из Railway переменных окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не задан!")

app = Application.builder().token(TOKEN).build()

# Список поддерживающих сообщений
SUPPORT_MESSAGES = [
    "ты делаешь достаточно 💛",
    "всё будет хорошо 🌿",
    "скоро всё получится ✨",
    "у тебя уже получается 🌸",
    "ты не одна 🤝",
    "ты справляешься 💪",
    "помни: ты делаешь достаточно 🌼",
    "маленькие победы тоже важны 🌷"
]

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет 🌿 Напиши мне, и я поддержу тебя 💛")

# Ответы по ключевым словам
async def reply_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    keywords = ["плохо", "устала", "один", "не получится", "выгорание", "тревога"]

    if any(word in text for word in keywords):
        await update.message.reply_text(random.choice(SUPPORT_MESSAGES))
    else:
        await update.message.reply_text("Я с тобой 🌸")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_support))

    app.run_polling()

if __name__ == "__main__":
    main()

    
