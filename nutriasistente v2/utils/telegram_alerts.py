import os
import telebot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))

if BOT_TOKEN and CHAT_ID:
    bot = telebot.TeleBot(BOT_TOKEN)

    def alerta_telegram(mensaje):
        try:
            bot.send_message(CHAT_ID, mensaje)
        except Exception as e:
            print("❌ Error al enviar alerta Telegram:", e)
else:
    def alerta_telegram(mensaje):
        print("⚠️ No se pudo enviar por Telegram (faltan datos)")
