from core.lector_correos import leer_correos
from utils.telegram_alerts import alerta_telegram
from datetime import datetime

try:
    # Guardar la fecha de última ejecución exitosa
    with open("/home/andres9jaen/nutriasistente/ultima_ejecucion.txt", "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    leer_correos()

except Exception as e:
    error_msg = f"⚠️ ERROR CRÍTICO al ejecutar main.py:\n\n{str(e)}"
    print(error_msg)
    alerta_telegram(error_msg)

