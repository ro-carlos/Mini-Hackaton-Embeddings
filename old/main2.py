import os
import chromadb
from sentence_transformers import SentenceTransformer

import markdown
import chromadb
import uuid


# Modelo para generar embeddings (puedes cambiarlo por otro)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Crear el cliente de ChromaDB (opcional: cambiar path para persistencia)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Crear la colección donde almacenaremos los documentos
collection = chroma_client.get_or_create_collection(name="markdown_docs")

# Directorio donde están los archivos Markdown
markdown_dir = "./markdown_pages"

# Leer los archivos y guardarlos en ChromaDB
for filename in os.listdir(markdown_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(markdown_dir, filename)

        # Leer el contenido del archivo
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # Convertir el texto en un embedding
        embedding = model.encode(content).tolist()

        # Agregar a la base de datos con metadata (nombre del archivo)
        collection.add(
            ids=[filename],
            embeddings=[embedding],
            metadatas=[{"filename": filename, "content": content}]
        )

print("✅ Archivos indexados en ChromaDB")




# Inicializa el modelo de embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')  # Puedes cambiar el modelo según prefieras

# Inicializa la base de datos Chroma
client = chromadb.Client()
# Crear o seleccionar una colección en la base de datos
collection = client.create_collection(name="markdown_embeddings")

def read_markdown_file(file_path):
    """Lee el contenido de un archivo Markdown y lo convierte a texto plano"""
    with open(file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    # Convierte Markdown a HTML y luego extrae solo el texto
    html = markdown.markdown(md_content)
    return html

def generate_embeddings(text):
    """Genera embeddings para un texto utilizando un modelo preentrenado"""
    embeddings = model.encode(text)
    return embeddings

def store_embeddings_in_chroma(file_name, text, embeddings):
    """Almacena los embeddings en la base de datos Chroma"""
    # Crear un ID único para cada documento utilizando uuid
    unique_id = str(uuid.uuid4())
    
    collection.add(
        documents=[text],
        metadatas=[{"file_name": file_name}],
        embeddings=[embeddings],
        ids=[unique_id]  # Agregar un identificador único para el documento
    )

def process_markdown_files(directory):
    """Procesa todos los archivos .md en el directorio dado y guarda los embeddings"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                print(f"Procesando {file_path}...")
                
                # Lee el contenido del archivo markdown
                text = read_markdown_file(file_path)
                
                # Genera los embeddings
                embeddings = generate_embeddings(text)
                
                # Almacena los embeddings en la base de datos Chroma
                store_embeddings_in_chroma(file, text, embeddings)

# Carpeta donde están los archivos Markdown
markdown_directory = "/Users/ochand/Dev/Mini-Hackaton-Embedding/markdown_pages/"

# Procesar los archivos y almacenarlos en la base de datos Chroma
process_markdown_files(markdown_directory)

print("Embeddings procesados y almacenados en Chroma.")




# Inicializa ChromaDB y crea/selecciona la colección
client = chromadb.Client()
collection = client.create_collection(name="markdown_embeddings")

def search_in_chroma(query, model, collection, top_n=5):
    """Busca los documentos más similares a una consulta"""
    query_embedding = model.encode(query)  # Genera el embedding de la consulta
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_n
    )
    return results

# Inicializa el modelo de embeddings
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# Ejemplo de búsqueda
query = "grado"
results = search_in_chroma(query, model, collection)

# Mostrar los resultados
for i, result in enumerate(results['documents']):
    print(f"Resultado {i + 1}:")
    print(f"Documento: {result}")
    print(f"Metadatos: {results['metadatas'][i]}")
    print()
