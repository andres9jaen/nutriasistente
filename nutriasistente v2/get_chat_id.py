import telebot
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def send_chat_id(message):
    print("📡 Tu chat_id es:", message.chat.id)

bot.polling()
