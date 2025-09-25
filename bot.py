import os
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ====== Load .env ======
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise SystemExit("TELEGRAM_TOKEN not set in .env!")

# ====== Поддерживающие сообщения ======
SUPPORT_MESSAGES = [
    "Ты справляешься лучше, чем думаешь.",
    "Я рядом — если нужно, напиши.",
    "Позволь себе паузу. Ты делаешь достаточно.",
    "Ошибки — это часть пути. У тебя получится.",
    "Маленькие победы — тоже победы.",
]

# ====== Обработчики ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привет! Я бот поддержки.\n\n"
        "/support — получить поддерживающее сообщение прямо сейчас\n\n"
        "Если тебе очень плохо — обратись к местным службам помощи."
    )
    await update.message.reply_text(text)

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(SUPPORT_MESSAGES))

async def keyword_listener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    keywords = ["плохо", "тяжело", "не могу", "устал", "один", "одинка", "депресс", "хочется"]
    if any(k in text for k in keywords):
        await update.message.reply_text(random.choice(SUPPORT_MESSAGES))

# ====== Main ======
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("support", support))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, keyword_listener))
    print("Bot started. Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()



