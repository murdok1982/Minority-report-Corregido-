import openai
import sqlite3
import subprocess
import json
import requests

# Configura tu clave de API
openai.api_key = "pon la tuya jeta"

# ID del modelo personalizado para ciberinvestigaciones
modelo_ciberinvestigacion_id = "Cyber Intelligence Analyst"

# Nombre de la base de datos con los comentarios descargados
DOWNLOAD_DB_NAME = "downloaded_comments.db"

# Sherlock (requiere instalación previa)
def usar_sherlock(username):
    try:
        result = subprocess.run(["sherlock", username, "--json", "sherlock_results.json"], capture_output=True, text=True)
        with open("sherlock_results.json", "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error al usar Sherlock: {e}")
        return {}


# esta es una herramienta de OSINT que busca información sobre un usuario en múltiples redes sociales


# Social-Searcher (requiere registro para obtener la API Key)
SOCIAL_SEARCHER_API_KEY = "pon la tuya listo"


def usar_social_searcher(query):
    url = f"https://api.social-searcher.com/v2/search"
    params = {
        "key": SOCIAL_SEARCHER_API_KEY,
        "q": query,
        "network": "facebook,twitter,instagram"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error en Social-Searcher: {response.text}")
            return {}
    except Exception as e:
        print(f"Error al usar Social-Searcher: {e}")
        return {}

# Combina herramientas OSINT y GPT para ciberinvestigación
def realizar_ciberinvestigacion(user_name, user_id, post_id):
    try:
        # Usar Sherlock
        sherlock_results = usar_sherlock(user_name)

        # Usar Social-Searcher
        social_searcher_results = usar_social_searcher(user_name)

        # Realizar análisis con GPT
        respuesta = openai.ChatCompletion.create(
            model=modelo_ciberinvestigacion_id,
            messages=[
                {"role": "system", "content": "Eres un modelo especializado en ciberinvestigaciones. Utilizas técnicas avanzadas como OSINT (Open Source Intelligence), búsqueda en redes sociales, análisis de huellas digitales y patrones de comportamiento en línea. Evalúa a los individuos con base en la información proporcionada y genera un informe de investigación."},
                {"role": "user", "content": f"Realiza una ciberinvestigación sobre el usuario:\n\nNombre: {user_name}\nID de Usuario: {user_id}\nID del Post: {post_id}.\n\nResultados de Sherlock: {json.dumps(sherlock_results)}\nResultados de theHarvester: {theharvester_results}\nResultados de Social-Searcher: {json.dumps(social_searcher_results)}"}
            ]
        )
        return respuesta['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        print(f"Error al conectar con el modelo: {e}")
        return None

def generar_informe_completo(psicologico, ciberinvestigacion):
    return f"INFORME COMPLETO DE CIBERINTELIGENCIA:\n\n**Informe Psicológico:**\n{psicologico}\n\n**Informe de Ciberinvestigación:**\n{ciberinvestigacion}"

def procesar_usuarios():
    # Conexión a la base de datos de comentarios descargados
    conn = sqlite3.connect(DOWNLOAD_DB_NAME)
    cursor = conn.cursor()

    # Consulta todos los usuarios únicos
    cursor.execute("SELECT DISTINCT user_name, user_id, post_id FROM comentarios_descargados")
    usuarios = cursor.fetchall()

    for usuario in usuarios:
        user_name, user_id, post_id = usuario
        print(f"Realizando ciberinvestigación para el usuario {user_name} ({user_id})...")
        
        # Obtener informe psicológico del GPT personalizado (puedes integrar el anterior aquí)
        informe_psicologico = "Ejemplo de informe psicológico generado anteriormente."

        # Realizar ciberinvestigación usando OSINT y GPT
        informe_ciberinvestigacion = realizar_ciberinvestigacion(user_name, user_id, post_id)

        # Generar informe completo
        informe_completo = generar_informe_completo(informe_psicologico, informe_ciberinvestigacion)
        print(informe_completo)

    conn.close()

if __name__ == "__main__":
    procesar_usuarios()
