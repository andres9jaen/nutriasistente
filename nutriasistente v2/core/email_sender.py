import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

BLOQUE_EXTRA = """
<hr>
<h3>📌 Próximos pasos para comenzar tu programa</h3>

<b>• Cuestionario</b><br>
Rellénalo con todos los detalles posibles (patologías, objetivos, gustos…).<br><br>

<b>• Documentación</b><br>
- Cuestionario completo<br>
- Justificante de pago<br><br>

<b>• Diseño del plan</b><br>
Nos llevará unos días, ya que elaboramos todo desde cero.<br><br>

<b>• Mediciones</b><br>
Te enviaremos instrucciones para que puedas tomarlas correctamente.<br><br>

<b>💳 IBAN:</b> <code>ES13 2100 7408 1102 0009 4648</code><br>
➡️ <i>En el concepto, pon solo tu nombre completo.</i><br><br>

<b>📬 Atención online</b><br>
Una vez arranquemos, todo el seguimiento será desde nuestro correo personal.<br>
<i>(Este correo solo se usa para la primera toma de contacto).</i><br><br>

<b>✅ ¡Y ya está! Muy pronto comienza tu cambio 💪</b>
<hr>
<i>Un saludo,</i><br>
<b><i>Pepe Lara Troyano</i></b><br><br>

<i>– Nutricionista especializado en salud digestiva y rendimiento deportivo<br>
– Postgrado en farmacología deportiva y ayudas ergogénicas<br>
– Experto en microbiota, análisis clínicos y salud hormonal femenina<br>
– Grado Superior en Dietética y Nutrición</i><br><br>

<i>"Enjoy The Changes"</i><br><br>

🌐 <i>www.npvnutrition.com (Código PL10)</i><br>
📍 <i>Avda. Granada 4 Bajo, Jaén</i><br>
📞 <i>953 88 52 70</i>
"""

def enviar_respuesta(destinatario, asunto, cuerpo_usuario):
    try:
        if not destinatario or not isinstance(destinatario, str):
            raise ValueError("❌ Error: destinatario no válido.")
        if not asunto or not isinstance(asunto, str):
            raise ValueError("❌ Error: asunto vacío o incorrecto.")
        if not cuerpo_usuario or not isinstance(cuerpo_usuario, str):
            raise ValueError("❌ Error: cuerpo_usuario está vacío o no es texto válido.")

        # Construcción del mensaje HTML
        cuerpo_html = f"{cuerpo_usuario}<br><br>{BLOQUE_EXTRA}"

        msg = MIMEMultipart("alternative")
        msg["From"] = "Pepe Lara Nutrición <top5hoyia@gmail.com>"
        msg["To"] = destinatario
        msg["Subject"] = asunto

        msg.attach(MIMEText(cuerpo_html, "html"))

        # Envío del correo
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        print(f"📤 Respuesta enviada correctamente a {destinatario}")

    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")
