import os
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

# Получаем токен из переменной окружения
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

# Хранилище chat_id для авто-уведомлений
active_chats = set()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    active_chats.add(chat_id)
    keyboard = [[InlineKeyboardButton("Получить поддержку прямо сейчас", callback_data="SUPPORT_NOW")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я буду присылать поддержку каждый час.\nНажми кнопку, чтобы получить поддержку прямо сейчас.",
        reply_markup=reply_markup
    )

# Кнопка "Получить поддержку прямо сейчас"
async def support_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    message = random.choice(SUPPORT_MESSAGES)
    await query.message.reply_text(message)

# Ответ на ключевые слова
async def keyword_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    keywords = ["помощь", "поддержка", "не могу", "плохо", "тяжело", "один", "устала"]
    if any(word in text for word in keywords):
        message = random.choice(SUPPORT_MESSAGES)
        await update.message.reply_text(message)

# Авто-уведомления каждый час
async def hourly_notifications(application: Application):
    while True:
        for chat_id in active_chats:
            await application.bot.send_message(chat_id=chat_id, text=random.choice(SUPPORT_MESSAGES))
        await asyncio.sleep(3600)  # 1 час

# Основной запуск
def main():
    app = Application.builder().token(TOKEN).build()

    # Хендлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(support_now, pattern="SUPPORT_NOW"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, keyword_handler))

    # Запуск цикла авто-уведомлений
    app.create_task(hourly_notifications(app))

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()
