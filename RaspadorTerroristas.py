import sqlite3
import requests

# Configuración de la API de Facebook
ACCESS_TOKEN = "TU_TOKEN_DE_ACCESO"
BASE_URL = "https://graph.facebook.com/v12.0"
ALERT_DB_NAME = "alert_data.db"

# Configura la base de datos para guardar los comentarios descargados
DOWNLOAD_DB_NAME = "downloaded_comments.db"

def setup_download_database():
    conn = sqlite3.connect(DOWNLOAD_DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios_descargados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            user_id TEXT,
            post_id TEXT,
            comment TEXT,
            created_time TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_comentario(data):
    conn = sqlite3.connect(DOWNLOAD_DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO comentarios_descargados (user_name, user_id, post_id, comment, created_time)
        VALUES (?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

def obtener_comentarios_post(post_id):
    url = f"{BASE_URL}/{post_id}/comments"
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "from{id,name},message,created_time",
        "limit": 100  # Ajusta según sea necesario
    }

    comentarios = []
    while url:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            comentarios.extend(data.get("data", []))
            url = data.get("paging", {}).get("next")  # Página siguiente
        else:
            print(f"Error al obtener comentarios del post {post_id}: {response.text}")
            break

    return comentarios

def procesar_alertas():
    setup_download_database()  # Configura la base de datos

    # Conexión a la base de datos de alertas
    conn = sqlite3.connect(ALERT_DB_NAME)
    cursor = conn.cursor()

    # Consulta todos los posts en la base de datos de alertas
    cursor.execute("SELECT DISTINCT post_id FROM alertas")
    posts = cursor.fetchall()

    for post in posts:
        post_id = post[0]
        print(f"Descargando comentarios del post {post_id}...")
        comentarios = obtener_comentarios_post(post_id)

        for comentario in comentarios:
            guardar_comentario((
                comentario['from']['name'],
                comentario['from']['id'],
                post_id,
                comentario.get('message', ''),
                comentario['created_time']
            ))

    conn.close()

if __name__ == "__main__":
    procesar_alertas()
