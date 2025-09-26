import os
import random
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Загружаем переменные окружения
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

# Отправка поддержки конкретному пользователю
async def send_support(chat_id, context: ContextTypes.DEFAULT_TYPE):
    message = random.choice(SUPPORT_MESSAGES)
    await context.bot.send_message(chat_id, message)

# Ежечасная рассылка всем пользователям
async def hourly_support(context: ContextTypes.DEFAULT_TYPE):
    chat_ids = context.bot_data.get("chat_ids", set())
    for chat_id in chat_ids:
        await send_support(chat_id, context)

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

# Кнопка поддержки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query.data == "support_now":
        await update.callback_query.answer()
        chat_id = update.effective_chat.id
        await send_support(chat_id, context)

# Основная функция
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button, pattern="support_now"))

    # Ежечасная рассылка
    app.job_queue.run_repeating(hourly_support, interval=3600, first=10)

    app.run_polling()

if __name__ == "__main__":
    main()
