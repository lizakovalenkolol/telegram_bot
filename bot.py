import os
import random
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Загружаем токен
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не задан!")

# Сообщения поддержки
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

# Отправка поддержки
async def send_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = random.choice(SUPPORT_MESSAGES)
    if update.message:
        await update.message.reply_text(message)
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(message)

# Ежечасная рассылка
async def hourly_support(context: ContextTypes.DEFAULT_TYPE):
    chat_ids = context.bot_data.get("chat_ids", set())
    for chat_id in chat_ids:
        await context.bot.send_message(chat_id, random.choice(SUPPORT_MESSAGES))

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_ids = context.bot_data.get("chat_ids", set())
    chat_ids.add(chat_id)
    context.bot_data["chat_ids"] = chat_ids

    keyboard = [[InlineKeyboardButton("Получить поддержку прямо сейчас", callback_data="support_now")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет! Я буду присылать тебе поддержку каждый час.",
        reply_markup=reply_markup
    )

# Обработка кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query.data == "support_now":
        await send_support(update, context)

# Основная функция
def main():
    app = Application.builder().token(TOKEN).build()

    # Хэндлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button, pattern="support_now"))

    # JobQueue для ежечасной рассылки
    app.job_queue.run_repeating(hourly_support, interval=3600, first=3600)

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()


