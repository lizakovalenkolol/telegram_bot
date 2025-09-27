import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Загружаем токен
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не задан!")

# Список чатов для уведомлений
subscribed_chats = set()

# Команда поддержки
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribed_chats.add(chat_id)
    
    if update.message:
        await update.message.reply_text("Сейчас с вами свяжутся для поддержки!")
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text("Сейчас с вами свяжутся для поддержки!")

# Ежечасная функция
async def hourly_support(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in subscribed_chats:
        await context.bot.send_message(chat_id=chat_id, text="Время для поддержки! ⏰")

# Стартовая команда с кнопкой
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribed_chats.add(chat_id)

    keyboard = [
        [InlineKeyboardButton("Получить поддержку прямо сейчас", callback_data='support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нажмите кнопку ниже для получения поддержки:", reply_markup=reply_markup)

def main():
    # Создаём приложение
    app = Application.builder().token(TOKEN).build()

    # Хэндлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(support, pattern="support"))

    # JobQueue: ежечасные уведомления
    app.job_queue.run_repeating(hourly_support, interval=3600, first=3600)

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()
