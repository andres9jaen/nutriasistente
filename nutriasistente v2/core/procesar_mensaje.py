from gpt.gpt_nutri import analizar_mensaje
import json

def limpiar_json(texto):
    # Elimina las comillas ```json ... ``` si vienen del GPT
    if texto.startswith("```json"):
        texto = texto.replace("```json", "").replace("```", "").strip()
    elif texto.startswith("```"):
        texto = texto.replace("```", "").strip()
    return texto

def procesar_mensaje(texto):
    salida = analizar_mensaje(texto)

    if salida is None:
        print("❌ No se pudo obtener respuesta del GPT.")
        return None

    try:
        limpio = limpiar_json(salida)
        datos = json.loads(limpio)
        return datos
    except json.JSONDecodeError as e:
        print("❌ Error al convertir JSON:", e)
        print("Contenido recibido:")
        print(salida)
        return None

