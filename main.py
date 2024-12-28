import os
from modules.connection import connect_to_groups
from modules.keyword_search import search_keywords
from modules.download_posts import download_posts
from modules.analysis import analyze_posts
from modules.report import generate_report

def main():
    print("Conectando con grupos peligrosos...")
    groups = connect_to_groups()

    print("Buscando palabras clave...")
    posts = search_keywords(groups)

    print("Descargando publicaciones...")
    user_data = download_posts(posts)

    print("Analizando publicaciones...")
    analysis_results = analyze_posts(user_data)

    print("Generando reporte final...")
    generate_report(analysis_results)

    print("Proceso completo. Reporte generado con éxito.")

if __name__ == "__main__":
    main()
