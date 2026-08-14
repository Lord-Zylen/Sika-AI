"""Vector retrieval without a vector DB.

Documents are embedded offline by rag/precompute_embeddings.py into
rag/embeddings.json (committed to the repo). At query time we embed only
the user's query via the Google Gemini embeddings API and do a cosine
search over the precomputed vectors with numpy. This keeps the deploy
small enough to run on Vercel serverless functions.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np

from config import EMBEDDING_MODEL, EMBEDDINGS_PATH, GOOGLE_API_KEY

_index = None
_client = None


def _get_client():
    global _client
    if _client is None:
        from google import genai
        _client = genai.Client(api_key=GOOGLE_API_KEY)
    return _client


def _load_index():
    global _index
    if _index is None:
        if not GOOGLE_API_KEY or not os.path.exists(EMBEDDINGS_PATH):
            return None
        with open(EMBEDDINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        vectors = np.array([c["embedding"] for c in data["chunks"]], dtype="float32")
        # Normalize once so cosine similarity is a plain dot product.
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        _index = {"chunks": data["chunks"], "vectors": vectors / norms}
    return _index


def _embed_query(query: str):
    resp = _get_client().models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[query],
        config={"task_type": "RETRIEVAL_QUERY"},
    )
    vec = np.array(resp.embeddings[0].values, dtype="float32")
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec


def retrieve(query: str, top_k: int = 4):
    """Returns list of (text, source) dicts relevant to the query."""
    idx = _load_index()
    if idx is None or idx["vectors"].shape[0] == 0:
        return []
    try:
        q = _embed_query(query)
    except Exception:
        return []
    sims = idx["vectors"] @ q
    top = int(min(top_k, idx["vectors"].shape[0]))
    order = sims.argsort()[::-1][:top]
    return [
        {"text": idx["chunks"][i]["text"], "source": idx["chunks"][i]["source"]}
        for i in order
        if sims[i] > 0
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
