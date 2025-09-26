import os
import asyncio
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# ==========================
# Переменная окружения
# ==========================
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не задан!")

# ==========================
# Сообщения поддержки
# ==========================
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

# ==========================
# Функция отправки поддержки
# ==========================
async def send_support(context: CallbackContext):
    """Отправляет случайное поддерживающее сообщение всем чатам"""
    for chat_id in context.chat_data.keys():
        message = random.choice(SUPPORT_MESSAGES)
        await context.bot.send_message(chat_id=chat_id, text=message)

# ==========================
# Команды бота
# ==========================
async def start(update: Update, context: CallbackContext):
    """Команда /start"""
    chat_id = update.effective_chat.id
    context.chat_data[chat_id] = True  # сохраняем чат для авто-уведомлений
    keyboard = [[InlineKeyboardButton("Получить поддержку прямо сейчас", callback_data="SUPPORT_NOW")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я буду присылать поддержку каждый час.\nНажми кнопку, чтобы получить поддержку прямо сейчас.",
        reply_markup=reply_markup
    )

async def support_now(update: Update, context: CallbackContext):
    """Обработчик кнопки поддержки"""
    query = update.callback_query
    await query.answer()
    message = random.choice(SUPPORT_MESSAGES)
    await query.message.reply_text(message)

async def keyword_handler(update: Update, context: CallbackContext):
    """Отправка поддержки при ключевых словах"""
    text = update.message.text.lower()
    keywords = ["помощь", "поддержка", "не могу", "плохо", "тяжело", "один", "устала"]
    if any(word in text for word in keywords):
        message = random.choice(SUPPORT_MESSAGES)
        await update.message.reply_text(message)

# ==========================
# Планировщик уведомлений каждый час
# ==========================
async def hourly_support(context: CallbackContext):
    for chat_id in context.chat_data.keys():
        message = random.choice(SUPPORT_MESSAGES)
        await context.bot.send_message(chat_id=chat_id, text=message)

# ==========================
# Основная функция
# ==========================
async def main():
    app = Application.builder().token(TOKEN).build()

    # Хендлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(support_now, pattern="SUPPORT_NOW"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, keyword_handler))

    # Добавляем задачу каждый час (3600 секунд)
    job_queue = app.job_queue
    job_queue.run_repeating(hourly_support, interval=3600, first=3600)

    # Запуск бота
    await app.run_polling()

# ==========================
# Старт
# ==========================
if __name__ == "__main__":
    asyncio.run(main())
