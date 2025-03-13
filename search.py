import chromadb

# Conectar a ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="documentos_markdown")

def buscar_texto(query, n_resultados=5, filtros=None):
    """ Busca texto en ChromaDB con filtros opcionales. """
    query_params = {
        "query_texts": [query],
        "n_results": n_resultados,
    }

    # Solo incluir filtros si existen
    if filtros:
        query_params["where"] = filtros

    resultados = collection.query(**query_params)
    return resultados