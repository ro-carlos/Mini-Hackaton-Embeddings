# Mini-Hackaton-Embedding

## 🏁 Setup Instructions

### 1️⃣ Create a Virtual Environment

```bash
python3 -m venv virtual_environment
```

### 2️⃣ Activate the Virtual Environment

On Linux / Mac:

```bash
source virtual_environment/bin/activate
```

On Windows:

```bash
virtual_environment\Scriptsctivate
```

---

### 3️⃣ Install Dependencies

```bash
python3 -m pip install -r requirements.txt html2text
```

---

## 🚀 Execution

### 4️⃣ Run the Main Script

```bash
python3 scrapper.py
```

### Software Embeding

https://ollama.com/search?q=embeding
https://www.nomic.ai/gpt4all
https://platform.openai.com/docs/guides/embeddings

🔹 Lista de pasos recomendada

Vamos a hacerlo por partes:

📌 FASE 1: Indexar los archivos en ChromaDB (ya casi lo tenemos)

1️⃣ Recorrer los archivos Markdown en markdown_pages/.
2️⃣ Extraer la metadata (idioma, sección, subsección).
3️⃣ Generar embeddings y guardarlos en ChromaDB.

📌 FASE 2: Crear una API con FastAPI

4️⃣ Hacer un endpoint /search para consultar ChromaDB con texto.
5️⃣ (Opcional) Hacer un endpoint /upload para subir nuevos .md dinámicamente.

📌 FASE 3: (Opcional) Integrar Ollama como generador de respuestas

6️⃣ Llamar a un modelo (mistral, llama2) con los resultados de ChromaDB.
7️⃣ Crear un endpoint /ask para recibir preguntas y responder con contexto.s
