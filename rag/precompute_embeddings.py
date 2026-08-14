"""
Precompute document embeddings into rag/embeddings.json using the Google
Gemini embeddings API (free tier). Run once (and re-run whenever you change
documents):

    python rag/precompute_embeddings.py

The output file is committed to the repo so Vercel can serve it read-only.
At query time, rag/retriever.py embeds just the user's query with the same
model and does a cosine search over these vectors with numpy — no torch,
no chromadb.

Requires a free API key: https://aistudio.google.com/apikey
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import EMBEDDING_MODEL, EMBEDDINGS_PATH, GOOGLE_API_KEY

BATCH_SIZE = 100


def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def build_chunks():
    doc_folder = os.path.join(os.path.dirname(__file__), "documents")
    chunks = []
    for filename in sorted(os.listdir(doc_folder)):
        if not filename.endswith(".txt"):
            continue
        path = os.path.join(doc_folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        for i, c in enumerate(chunk_text(text)):
            chunks.append({
                "id": f"{filename}-{i}",
                "text": c,
                "source": filename,
                "chunk": i,
            })
    return chunks


def embed(client, chunks):
    from google import genai
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        texts = [c["text"] for c in batch]
        resp = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=texts,
            config={"task_type": "RETRIEVAL_DOCUMENT"},
        )
        for j, c in enumerate(batch):
            c["embedding"] = resp.embeddings[j].values


def main():
    if not GOOGLE_API_KEY:
        sys.exit("GOOGLE_API_KEY not found. Set it in logs/.env or your environment.")
    from google import genai
    client = genai.Client(api_key=GOOGLE_API_KEY)
    chunks = build_chunks()
    if not chunks:
        sys.exit("No .txt documents found in rag/documents/")
    embed(client, chunks)
    out = {"model": EMBEDDING_MODEL, "chunks": chunks}
    os.makedirs(os.path.dirname(EMBEDDINGS_PATH), exist_ok=True)
    with open(EMBEDDINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f)
    print(f"Saved {len(chunks)} embedded chunks to {EMBEDDINGS_PATH}")


if __name__ == "__main__":
    main()
