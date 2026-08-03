import os
from dotenv import load_dotenv

load_dotenv("logs/.env")

# LLM provider — defaults to Groq (free tier, OpenAI-compatible API)
# Get a free key at https://console.groq.com/keys
LLM_API_KEY = os.getenv("GROQ_API_KEY", os.getenv("OPENAI_API_KEY"))
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

VECTOR_DB_PATH = "./rag/chroma_store"
SKILLS_DIR = "./skills"
LOG_DIR = "./logs"
