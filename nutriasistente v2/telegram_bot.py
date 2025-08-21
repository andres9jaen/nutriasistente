import os
import telebot
import subprocess
import json
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables del entorno
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))

bot = telebot.TeleBot(BOT_TOKEN)

# Rutas importantes
MAIN_SCRIPT = "/home/andres9jaen/nutriasistente/main.py"
PYTHON_BIN = "/home/andres9jaen/nutriasistente/.venv/bin/python"
LOG_FILE = "/home/andres9jaen/nutriasistente/logs.txt"
CONFIG_FILE = "/home/andres9jaen/nutriasistente/config.json"

# Variable de estado del sistema
toggle_estado = {"activo": True}

# Leer y guardar configuración
estilos = {
    "calido": "✍️ Cálido y motivador",
    "directo": "🎯 Directo y profesional",
    "tecnico": "💡 Técnico y explicativo",
    "empatico": "🧘‍♂️ Tranquilo y empático"
}

def guardar_estilo(estilo):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"estilo": estilo}, f)

def cargar_estilo():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f).get("estilo", "calido")
    return "calido"

# Menú persistente tipo teclado
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def teclado_principal():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("▶️ Ejecutar ahora", "📝 Ver logs", "🧹 Limpiar logs", "📊 Estado", "🛑 Parar sistema", "🟢 Reanudar sistema", "🎨 Elegir estilo GPT")
    return markup

def inline_estilos():
    markup = InlineKeyboardMarkup()
    for key, label in estilos.items():
        markup.add(InlineKeyboardButton(label, callback_data=f"estilo_{key}"))
    return markup

# --------- MENSAJES ---------

@bot.message_handler(commands=['start', 'menu'])
def start(msg):
    if msg.chat.id == CHAT_ID:
        bot.send_message(CHAT_ID, "🤖 Panel de control de Nutriasistente. Elige una opción:", reply_markup=teclado_principal())

@bot.message_handler(func=lambda message: True)
def manejar_mensajes(message):
    if message.chat.id != CHAT_ID:
        return

    texto = message.text.strip().lower()

    if texto.startswith("estado") or "📊" in texto:
        estado = "🟢 EN FUNCIONAMIENTO" if toggle_estado["activo"] else "🔴 DETENIDO"
        bot.send_message(CHAT_ID, f"🔎 Estado actual del sistema: {estado}", reply_markup=teclado_principal())

    elif "ejecutar" in texto:
        bot.send_message(CHAT_ID, "▶️ Ejecutando el script manualmente...", reply_markup=teclado_principal())
        subprocess.Popen([PYTHON_BIN, MAIN_SCRIPT])

    elif "ver logs" in texto:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                contenido = f.read()[-4000:] or "(Log vacío)"
            bot.send_message(CHAT_ID, f"📝 Últimos logs:\n\n{contenido}", reply_markup=teclado_principal())
        else:
            bot.send_message(CHAT_ID, "❌ No se encontró el archivo de logs.", reply_markup=teclado_principal())

    elif "limpiar logs" in texto:
        open(LOG_FILE, 'w').close()
        bot.send_message(CHAT_ID, "🧹 Logs limpiados correctamente.", reply_markup=teclado_principal())

    elif "parar" in texto:
        toggle_estado["activo"] = False
        bot.send_message(CHAT_ID, "🛑 Sistema pausado manualmente. No se ejecutará automáticamente.", reply_markup=teclado_principal())

    elif "reanudar" in texto:
        toggle_estado["activo"] = True
        bot.send_message(CHAT_ID, "🟢 Sistema reanudado. Vuelve a funcionar con normalidad.", reply_markup=teclado_principal())

    elif "estilo" in texto:
        bot.send_message(CHAT_ID, "🎨 Elige el estilo de respuesta GPT que deseas usar:", reply_markup=inline_estilos())

    else:
        bot.send_message(CHAT_ID, "❓ Comando no reconocido. Usa los botones para interactuar.", reply_markup=teclado_principal())

@bot.callback_query_handler(func=lambda call: call.data.startswith("estilo_"))
def cambiar_estilo(call):
    clave = call.data.split("_")[1]
    guardar_estilo(clave)
    nombre = estilos[clave]
    bot.answer_callback_query(call.id, f"Estilo cambiado a: {nombre}")
    bot.send_message(CHAT_ID, f"✅ Nuevo estilo GPT guardado: {nombre}", reply_markup=teclado_principal())

# --------- INICIO ---------

if __name__ == '__main__':
    estilo_actual = cargar_estilo()
    hora_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🤖 Bot iniciado {hora_inicio} | Estilo GPT: {estilo_actual}")

    mensaje_inicio = (
        f"🔁 *Raspberry Pi iniciada / Bot arrancado*\n\n"
        f"📅 Fecha: *{hora_inicio}*\n"
        f"🎨 Estilo actual de GPT: *{estilo_actual}*\n\n"
        f"Todo preparado para recibir nuevos clientes. ✅"
    )

    bot.send_message(CHAT_ID, mensaje_inicio, parse_mode="Markdown", reply_markup=teclado_principal())
    bot.infinity_polling()

