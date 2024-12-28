import sqlite3

# Conjuntos de palabras clave y frases en diferentes idiomas
keywords = {
    "ar": ["العنف", "التعصب", "التطرف", "الإرهاب", "الكراهية", "الدمار", "الانتقام", "القتل", "الحرب", "الهجوم"],
    "ur": ["تشدد", "جنون", "انتہا پسندی", "دہشت گردی", "نفرت", "تباہی", "انتقام", "قتل", "جنگ", "حملہ"],
    "ps": ["تاوتریخوالی", "تعصب", "بنسټپالنه", "تروریزم", "کرکه", "ویجاړتیا", "انتقام", "وژنه", "جنګ", "برید"],
    "ru": ["насилие", "фанатизм", "радикализм", "терроризм", "ненависть", "разрушение", "месть", "убийство", "война", "атака"],
    "es": ["violencia", "fanatismo", "radicalismo", "terrorismo", "odio", "destrucción", "venganza", "matar", "guerra", "ataque"]
}
phrases = {
    "ar": ["اقتلهم جميعًا", "دمر كل شيء", "الانتقام هو السبيل الوحيد", "يستحقون الموت", "انشر الكراهية", "اقضِ على الكفار", "أبيد الأعداء", "أحرق كل شيء", "استعد للحرب", "النضال أبدي"],
    "ur": ["انہیں سب کو مار دو", "سب کچھ تباہ کر دو", "انتقام ہی واحد راستہ ہے", "وہ مرنے کے لائق ہیں", "نفرت پھیلائیں", "کافروں کا خاتمہ کریں", "دشمنوں کو ختم کریں", "سب کچھ جلا دو", "جنگ کے لئے تیار ہو جاؤ", "جنگ ہمیشہ جاری ہے"],
    "ps": ["ټول ووژنئ", "هرڅه ویجاړ کړئ", "انتقام یوازینۍ لار ده", "هغوی د مرګ وړ دي", "کرکه خپره کړئ", "کافران ختم کړئ", "دښمنان ووژنئ", "هرڅه وسوځوئ", "د جګړې لپاره چمتو شئ", "مبارزه ابدي ده"],
    "ru": ["Убей их всех", "Разрушь всё", "Месть — единственный путь", "Они заслуживают смерти", "Распространяй ненависть", "Уничтожь неверных", "Убей врагов", "Сожги всё", "Готовься к войне", "Борьба вечна"],
    "es": ["Mátenlos a todos", "Destruyan todo", "La venganza es el único camino", "Merecen morir", "Esparce el odio", "Acaben con los infieles", "Eliminen a los enemigos", "Quemen todo", "Prepárense para la guerra", "La lucha es eterna"]
}

# Nombre de las bases de datos
DB_NAME = "facebook_data.db"
ALERT_DB_NAME = "alert_data.db"

def setup_alert_database():
    conn = sqlite3.connect(ALERT_DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            user_id TEXT,
            post_id TEXT,
            group_id TEXT,
            comment TEXT,
            created_time TEXT,
            detected_language TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_alerta(data):
    conn = sqlite3.connect(ALERT_DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alertas (user_name, user_id, post_id, group_id, comment, created_time, detected_language)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

def comprobar_comentarios():
    # Configura la base de datos de alertas
    setup_alert_database()

    # Conexión a la base de datos principal
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Consulta todos los comentarios
    cursor.execute("SELECT user_name, user_id, post_id, group_id, comment, created_time FROM comentarios")
    comentarios = cursor.fetchall()

    for comentario in comentarios:
        user_name, user_id, post_id, group_id, comment, created_time = comentario

        # Comprueba cada palabra clave y frase en todos los idiomas
        for lang, palabras_clave in keywords.items():
            for palabra in palabras_clave:
                if palabra in comment:
                    print(f"ALERTA: Coincidencia detectada en comentario:")
                    print(f"  Usuario: {user_name} ({user_id})")
                    print(f"  Post ID: {post_id}, Grupo ID: {group_id}")
                    print(f"  Comentario: {comment}")
                    print(f"  Hora: {created_time}")
                    print(f"  Idioma detectado: {lang}")
                    print("---")
                    # Guarda en la base de datos de alertas
                    guardar_alerta((user_name, user_id, post_id, group_id, comment, created_time, lang))

        for lang, frases_clave in phrases.items():
            for frase in frases_clave:
                if frase in comment:
                    print(f"ALERTA: Coincidencia detectada en comentario:")
                    print(f"  Usuario: {user_name} ({user_id})")
                    print(f"  Post ID: {post_id}, Grupo ID: {group_id}")
                    print(f"  Comentario: {comment}")
                    print(f"  Hora: {created_time}")
                    print(f"  Idioma detectado: {lang}")
                    print("---")
                    # Guarda en la base de datos de alertas
                    guardar_alerta((user_name, user_id, post_id, group_id, comment, created_time, lang))

    # Cierra la conexión a la base de datos principal
    conn.close()

if __name__ == "__main__":
    comprobar_comentarios()
