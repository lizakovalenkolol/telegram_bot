import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Фиктивный порт для Render (не используется самим ботом)
PORT = int(os.environ.get("PORT", 5000))
print(f"Running on dummy port {PORT}")

# Список поддерживающих сообщений
messages = [
    "Ты делаешь достаточно",
    "Всё будет хорошо",
    "Скоро всё получится",
    "У тебя уже получается",
    "Ты не одна",
    "Ты справляешься",
    "Помни: ты делаешь достаточно",
    "Маленькие победы тоже важны"
]

# Множество для хранения пользователей
subscribers = set()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    subscribers.add(chat_id)
    await update.message.reply_text(
        "Привет! Я бот поддержки! 💛 Ты будешь получать поддерживающие сообщения каждый час!"
    )

# Уведомления каждый час
async def hourly_notification(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in subscribers:
        try:
            await context.bot.send_message(chat_id=chat_id, text=random.choice(messages))
        except Exception as e:
            print(f"Не удалось отправить сообщение {chat_id}: {e}")

# Ответ по ключевым словам
async def keyword_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    keywords = ["устала", "плохо", "не могу", "тяжело", "сложно", "одинок", "одинокая"]
    if any(k in text for k in keywords):
        await update.message.reply_text(random.choice(messages))

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN не задан!")

    # Создаём приложение
    app = Application.builder().token(token).build()

    # Команды
    app.add_handler(CommandHandler("start", start))

    # Сообщения по ключевым словам
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), keyword_response))

    # JobQueue для часовых уведомлений
    app.job_queue.run_repeating(hourly_notification, interval=3600, first=10)  # первый раз через 10 сек

    # Запуск бота без asyncio.run() — идеально для Render
    app.run_polling()

if __name__ == "__main__":
    main()
