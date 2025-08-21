import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
sheet_name = os.getenv("GOOGLE_SHEET_NAME")

# Autenticación con Google
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Ruta absoluta al archivo de credenciales
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
client = gspread.authorize(creds)

# Abrir hoja
sheet = client.open(sheet_name).sheet1

def guardar_en_sheet(datos_cliente):
    try:
        fila = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),             # Fecha
            datos_cliente.get("nombre_cliente", ""),
            datos_cliente.get("email", ""),
            datos_cliente.get("telefono", ""),
            datos_cliente.get("pack_interesado", ""),
            datos_cliente.get("nivel_interes", ""),
            datos_cliente.get("preguntas_detectadas", ""),
            datos_cliente.get("resumen_sheet", ""),
            datos_cliente.get("respuesta_email", ""),
            "Pendiente",   # Estado seguimiento (editable luego)
            "",            # ID del hilo
            ""             # Observaciones
        ]

        sheet.append_row(fila)
        print("✅ Fila añadida correctamente a Google Sheets.")
    except Exception as e:
        print("❌ Error al escribir en Google Sheet:", e)
