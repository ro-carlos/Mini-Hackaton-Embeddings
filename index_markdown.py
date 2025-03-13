import os
import time
import chromadb
from sentence_transformers import SentenceTransformer
from joblib import Parallel, delayed

# Configurar modelo de embeddings
modelo = SentenceTransformer("all-MiniLM-L6-v2")

# Conectar a ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documentos_markdown")

# Procesamos solo markdown_pages/es/
ROOT_DIR = "markdown_pages/es"

def generar_embeddings(textos):
    """Genera embeddings para una lista de textos."""
    return modelo.encode(textos).tolist()

def obtener_ids_existentes():
    """Obtiene los IDs existentes en la base de datos paginando los resultados."""
    ids_existentes = set()
    limit = 1000  # Evitar consumir demasiada RAM
    offset = 0

    while True:
        resultados = collection.get(limit=limit, offset=offset)
        if not resultados["ids"]:
            break  # No hay más IDs para cargar
        ids_existentes.update(resultados["ids"])
        offset += limit  # Avanzar en la paginación

    return ids_existentes

def indexar_markdown():
    start_time = time.time()  # Iniciar tiempo total
    total_archivos = 0
    total_chunks = 0
    ids_existentes = obtener_ids_existentes()  # Obtener IDs en bloques

    batch_size = 10  # Tamaño del lote (puedes ajustarlo si es necesario)

    # Procesar los archivos y dividir en chunks
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".md"):
                total_archivos += 1
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    contenido = f.read()

                chunks = contenido.split("\n\n")
                nuevos_chunks = [
                    (i, chunk) for i, chunk in enumerate(chunks)
                    if f"{file_path}_chunk_{i}" not in ids_existentes
                ]
                
                if nuevos_chunks:
                    # Dividir los chunks en lotes
                    lotes = [nuevos_chunks[i:i+batch_size] for i in range(0, len(nuevos_chunks), batch_size)]
                    
                    # Paralelizar el procesamiento de los lotes de chunks
                    embeddings = Parallel(n_jobs=-1)(delayed(generar_embeddings)([chunk[1] for chunk in lote]) for lote in lotes)

                    # Almacenar los embeddings en la base de datos
                    for lote, embedding_lote in zip(lotes, embeddings):
                        collection.add(
                            documents=[chunk[1] for chunk in lote],  # Solo los textos
                            embeddings=embedding_lote,
                            metadatas=[{
                                "archivo": file,
                                "seccion": root.replace(ROOT_DIR, "").strip("/"),  # Extraer sección de la ruta
                                "posicion": i
                            } for i, _ in lote],
                            ids=[f"{file_path}_chunk_{i}" for i, _ in lote]
                        )

                        total_chunks += len(lote)
                        print(f"✅ {file}: {len(lote)} chunks nuevos procesados y almacenados en DB")

    print(f"\n🔹 Total archivos procesados: {total_archivos}")
    print(f"🔹 Total chunks almacenados: {total_chunks}")
    print(f"⏳ Tiempo total: {time.time() - start_time:.2f}s")