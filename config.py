import os
from dotenv import load_dotenv

# Resolve project root from this file so paths work locally AND on Vercel
# (where the working directory is not guaranteed to be the repo root).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load local secrets from logs/.env (dev only). Env vars set in the Vercel
# dashboard take precedence because load_dotenv doesn't override by default.
load_dotenv(os.path.join(BASE_DIR, "logs", ".env"))

# LLM provider — defaults to Groq (free tier, OpenAI-compatible API)
# Get a free key at https://console.groq.com/keys
LLM_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

# Embeddings — Google Gemini API (free tier) is used at query time (see
# rag/retriever.py). The document index is precomputed offline into
# EMBEDDINGS_PATH. Get a free key at https://aistudio.google.com/apikey
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")

SKILLS_DIR = os.path.join(BASE_DIR, "skills")
LOG_DIR = os.path.join(BASE_DIR, "logs")
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "rag", "embeddings.json")
