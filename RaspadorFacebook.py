import requests
import sqlite3
import time

# Configura tu token de acceso y la lista de grupos
ACCESS_TOKEN = ""
group_id = ["", "", ""]  # Lista de IDs de grupos
BASE_URL = "https://graph.facebook.com/v12.0"

# Configuración de la base de datos
DB_NAME = "facebook_data.db"

# Crea la base de datos y tabla si no existen
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            user_id TEXT,
            post_id TEXT,
            group_id TEXT,
            comment TEXT,
            created_time TEXT
        )
    """)
    conn.commit()
    conn.close()

# Guarda datos en la base de datos
def guardar_datos(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO comentarios (user_name, user_id, post_id, group_id, comment, created_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

# Recupera publicaciones de un grupo
def obtener_publicaciones(group_id):
    url = f"{BASE_URL}/{group_id}/feed"
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "id,message,created_time,from",
        "limit": 10  # límite 
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error al obtener publicaciones del grupo {group_id}: {response.text}")
        return []

# Recupera comentarios de una publicación
def obtener_comentarios(post_id):
    url = f"{BASE_URL}/{post_id}/comments"
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "from{id,name},message,created_time",
        "limit": 10  # Ajusta el límite según tus necesidades
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error al obtener comentarios del post {post_id}: {response.text}")
        return []

# Procesa todos los grupos y guarda los datos
def procesar_grupos():
    setup_database()  # Configura la base de datos
    for group_id in GROUP_IDS:
        print(f"Procesando grupo: {group_id}")
        publicaciones = obtener_publicaciones(group_id)
        for post in publicaciones:
            post_id = post['id']
            print(f"  Procesando post: {post_id}")
            comentarios = obtener_comentarios(post_id)
            datos_guardar = []
            for comentario in comentarios:
                datos_guardar.append((
                    comentario['from']['name'],
                    comentario['from']['id'],
                    post_id,
                    group_id,
                    comentario.get('message', ''),
                    comentario['created_time']
                ))
            guardar_datos(datos_guardar)  # Guarda en la base de datos
        time.sleep(1)  # Evita exceder el límite de la API

# Ejecuta el procesamiento
if __name__ == "__main__":
    procesar_grupos()
