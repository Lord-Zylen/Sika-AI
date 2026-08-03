import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import chromadb
from chromadb.utils import embedding_functions
from config import VECTOR_DB_PATH

EMBED_MODEL = "all-MiniLM-L6-v2"

_client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
_embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBED_MODEL
)
_collection = _client.get_or_create_collection(
    name="sika_knowledge", embedding_function=_embed_fn
)

def retrieve(query: str, top_k: int = 4):
    """Returns list of (text, source) dicts relevant to the query."""
    if _collection.count() == 0:
        return []
    results = _collection.query(query_texts=[query], n_results=min(top_k, _collection.count()))
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    if not docs:
        return []
    return [
        {"text": d, "source": m.get("source", "unknown")}
        for d, m in zip(docs, metas)
    ]


def build_context(query: str, top_k: int = 4) -> str:
    """Build a context string from retrieved chunks, suitable for injection into a prompt."""
    results = retrieve(query, top_k)
    if not results:
        return ""
    parts = []
    for r in results:
        parts.append(f"[Source: {r['source']}]\n{r['text']}")
    return "\n\n---\n\n".join(parts)
