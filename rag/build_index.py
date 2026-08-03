"""
Run this once (and re-run whenever you add/update documents) to build
the RAG vector index from source documents in rag/documents/.
Uses sentence-transformers locally — no API calls needed.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import chromadb
from chromadb.utils import embedding_functions
from config import VECTOR_DB_PATH

EMBED_MODEL = "all-MiniLM-L6-v2"

def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def build_index():
    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL
    )
    collection = client.get_or_create_collection(
        name="sika_knowledge", embedding_function=embed_fn
    )

    doc_folder = os.path.join(os.path.dirname(__file__), "documents")
    doc_id = 0
    for filename in os.listdir(doc_folder):
        if not filename.endswith(".txt"):
            continue
        path = os.path.join(doc_folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                metadatas=[{"source": filename, "chunk": i}],
                ids=[f"{filename}-{i}-{doc_id}"]
            )
            doc_id += 1
    print(f"Indexed {doc_id} chunks from {doc_folder}")

if __name__ == "__main__":
    build_index()
