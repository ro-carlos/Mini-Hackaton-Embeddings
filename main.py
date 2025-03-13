from index_markdown import indexar_markdown
from search import buscar_texto

def main():
    print("\n🔹 1. Indexar archivos Markdown en ChromaDB...")
    indexar_markdown()

    print("\n🔹 2. Realizar una búsqueda de prueba...")
    query = "¿Qué dice sobre inteligencia artificial?"
    resultados = buscar_texto(query, n_resultados=3)

    for i, (doc, meta) in enumerate(zip(resultados['documents'][0], resultados['metadatas'][0])):
        print(f"\n🔹 Resultado {i+1}:")
        print(f"📄 Archivo: {meta['archivo']}")
        print(f"📂 Sección: {meta['seccion']}")
        print(f"📝 Texto: {doc[:200]}...")  # Mostrar solo los primeros 200 caracteres

if __name__ == "__main__":
    main()