import openai
import sqlite3

# Configura tu clave de API
openai.api_key = "pon la tuya jeta"

# ID del modelo personalizado (reemplázalo con el tuyo)
modelo_personalizado_id = "Behavioral Pattern Detector"

# Nombre de la base de datos con los comentarios descargados
DOWNLOAD_DB_NAME = "downloaded_comments.db"

def enviar_a_gpt(comment, user_name, user_id):
    try:
        respuesta = openai.ChatCompletion.create(
            model=modelo_personalizado_id,
            messages=[
                {"role": "system", "content": "Eres un asistente útil propiedad de gustavolobatoclara@gmail.com y realizarás el mejor de los trabajos como analista. Todos los comentarios que sean incluidos los analizarás en busca de patrones de comportamientos violentos o peligrosos."},
                {"role": "user", "content": f"Comentario: {comment}\nUsuario: {user_name}\nID de Usuario: {user_id}. Realiza una evaluación psicológica del individuo."}
            ]
        )
        return respuesta['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        print(f"Error al conectar con el modelo: {e}")
        return None

def procesar_comentarios():
    # Conexión a la base de datos de comentarios descargados
    conn = sqlite3.connect(DOWNLOAD_DB_NAME)
    cursor = conn.cursor()

    # Consulta todos los comentarios
    cursor.execute("SELECT user_name, user_id, post_id, comment FROM comentarios_descargados")
    comentarios = cursor.fetchall()

    for comentario in comentarios:
        user_name, user_id, post_id, comment = comentario
        print(f"Procesando comentario del usuario {user_name} ({user_id})...")
        
        # Enviar comentario al modelo GPT personalizado
        evaluacion = enviar_a_gpt(comment, user_name, user_id)
        if evaluacion:
            print("Evaluación realizada por GPT:")
            print(evaluacion)

    conn.close()

if __name__ == "__main__":
    procesar_comentarios()

