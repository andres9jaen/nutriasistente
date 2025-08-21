from utils.telegram_alerts import alerta_telegram
import imaplib
import email
from email.header import decode_header
import re
from dotenv import load_dotenv
import os
from core.procesar_mensaje import procesar_mensaje
from sheets.sheet_writer import guardar_en_sheet
from core.email_sender import enviar_respuesta

load_dotenv()

EMAIL_USER = "top5hoyia@gmail.com"
EMAIL_PASS = "mhni ldiu txdq plwc"  # contraseña de aplicación

def extraer_bloque_cliente(texto):
    """
    Intenta extraer automáticamente el bloque que contiene los datos del cliente.
    Busca desde 'Nombre:' hasta el final de 'Mensaje:'.
    """
    patron = r"(?i)Nombre:.*?Mensaje:.*"
    resultado = re.search(patron, texto, re.DOTALL)
    return resultado.group().strip() if resultado else None

def limpiar_texto(texto):
    return texto.replace("\r", "").strip()

def leer_correos():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    result, data = mail.search(None, 'UNSEEN')  # solo no leídos
    ids = data[0].split()

    print(f"📥 Correos no leídos: {len(ids)}")

    for num in ids:
        res, msg_data = mail.fetch(num, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        cuerpo = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    cuerpo = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            cuerpo = msg.get_payload(decode=True).decode(errors="ignore")

        texto = limpiar_texto(cuerpo)
        bloque = extraer_bloque_cliente(texto)

        if bloque:
            print("✅ Correo válido. Procesando...")
            datos = procesar_mensaje(bloque)
            if datos:
                guardar_en_sheet(datos)
                alerta_telegram(f"📬 Nuevo cliente: {datos['nombre_cliente']}\n📧 {datos['email']}\n📦 {datos['pack_interesado']}")

                # Solo enviar si hay respuesta válida
                respuesta = datos.get("respuesta_email", "")
                if respuesta:
                    enviar_respuesta(
                        destinatario=datos["email"],
                        asunto="Gracias por tu interés en nuestro plan nutricional",
                        cuerpo_usuario=respuesta
                    )
                else:
                    print("⚠️ Advertencia: respuesta_email vacía. No se envió el correo.")

                mail.store(num, '+FLAGS', '\\Seen')  # marcar como leído
        else:
            print("⛔ Correo no válido. Ignorado.")

    mail.logout()
