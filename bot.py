import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Множество для хранения пользователей
subscribers = set()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    subscribers.add(chat_id)  # сохраняем пользователя для уведомлений
    await update.message.reply_text("Привет! Я бот поддержки! 💛 Ты будешь получать поддерживающие сообщения!")

# Функция часового уведомления
async def hourly_notification(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in subscribers:
        try:
            await context.bot.send_message(chat_id=chat_id, text="💛 Твоё поддерживающее сообщение!")
        except Exception as e:
            print(f"Не удалось отправить сообщение {chat_id}: {e}")

async def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN не задан!")

    app = Application.builder().token(token).build()

    # Команды
    app.add_handler(CommandHandler("start", start))

    # JobQueue для часовых уведомлений
    app.job_queue.run_repeating(hourly_notification, interval=3600, first=10)  # первый раз через 10 сек для теста

    # Запуск бота
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
