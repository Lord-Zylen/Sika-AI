# AGENTS.md

## What this is

Sika AI — a Python RAG chatbot for Ghanaian financial guidance. LLM via Groq (OpenAI-compatible), Google Gemini free embeddings + numpy cosine retrieval, FastAPI. Deployed on Vercel. No tests, no lint, no CI yet.

## Setup

```bash
source venv/bin/activate        # Python 3.14 venv
pip install -r requirements.txt
```

Secrets live in `logs/.env` (dev) and Vercel env vars (prod):
- `GROQ_API_KEY` — LLM provider (free at https://console.groq.com/keys)
- `GOOGLE_API_KEY` — embeddings (free at https://aistudio.google.com/apikey)

## Running

```bash
# Rebuild the RAG index (run after adding/changing docs in rag/documents/)
python rag/precompute_embeddings.py

# Launch the FastAPI app locally
uvicorn api.index:app --reload
```

`main.py` is the orchestrator (imported by `api/index.py`). Use `from main import chat` to drive the agent programmatically.

## Deploying to Vercel

```bash
npm i -g vercel
vercel             # first time: link project, set up env vars
vercel env add GROQ_API_KEY
vercel env add GOOGLE_API_KEY
vercel --prod
```

Set the same env vars in the Vercel dashboard (Settings → Environment Variables). The RAG index is committed (`rag/embeddings.json`), so no build step is needed on Vercel.

## Project structure

- `config.py` — central config (API keys, model, paths). Loads `logs/.env` explicitly; Vercel env vars take precedence.
- `system_prompt.py` — Sika AI persona and tool-usage instructions.
- `main.py` — orchestrator: builds messages, calls the LLM, dispatches tool calls, integrates RAG.
- `api/index.py` — FastAPI entrypoint (Vercel function): serves `web/index.html`, exposes `/api/chat`.
- `web/index.html` — chat UI (vanilla JS).
- `tools/` — function tools the LLM can call (forex rates, calculator, web search, etc.).
- `rag/` — `precompute_embeddings.py` builds `embeddings.json` (committed); `retriever.py` queries it with numpy cosine similarity.
- `skills/` — `loader.py` reads `SKILL.md` files from subdirs. Add skill content as `skills/<name>/SKILL.md`.
- `logs/.env` — secrets. Never commit.

## Key gotchas

- **`.env` lives at `logs/.env`, not project root.** `config.py` loads it with an absolute path. Don't call bare `load_dotenv()` or it won't find the key.
- **`rag/embeddings.json` must be committed** — Vercel serves it read-only. Rebuild after changing documents: `python rag/precompute_embeddings.py`.
- **Path resolution** uses `BASE_DIR` (from `config.py`) so paths work both locally and on Vercel, where the working directory isn't the repo root.
- **`live_data.py` fallback rates** are hardcoded references. Update them periodically or swap in a live API.
- **Python 3.14 locally, Vercel runs 3.12+** — code uses PEP 604 (`dict | None`) so it works on 3.10+.
- **No quality tooling yet.** If you add lint/typecheck/test, document the commands here.
