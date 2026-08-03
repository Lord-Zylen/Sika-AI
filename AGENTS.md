# AGENTS.md

## What this is

Sika AI — a Python RAG chatbot for Ghanaian financial guidance. OpenAI GPT-4o + ChromaDB + sentence-transformers + Streamlit. No tests, no lint, no CI yet.

## Setup

```bash
source venv/bin/activate        # Python 3.14 venv
pip install -r requirements.txt
```

## Running

```bash
# Build/update the RAG index (do this after adding docs to rag/documents/)
python rag/build_index.py

# Launch the Streamlit chat UI
streamlit run app.py
```

`main.py` is the orchestrator (imported by `app.py`). Use `from main import chat` to drive the agent programmatically.

## Project structure

- `config.py` — central config (API key, model name, paths). Loads `logs/.env` explicitly.
- `system_prompt.py` — Sika AI persona and tool-usage instructions.
- `main.py` — orchestrator: builds messages, calls OpenAI, dispatches tool calls, integrates RAG.
- `app.py` — Streamlit chat UI.
- `tools/` — function tools the LLM can call (forex rates, calculator, etc.).
- `rag/` — ChromaDB vector index: `build_index.py` to index, `retriever.py` to query.
- `skills/` — `loader.py` reads `SKILL.md` files from subdirs. Add skill content as `skills/<name>/SKILL.md`.
- `logs/.env` — secrets (OPENAI_API_KEY). Never commit.

## Key gotchas

- **`.env` lives at `logs/.env`, not project root.** `config.py` loads it with `load_dotenv("logs/.env")`. Don't call bare `load_dotenv()` or it won't find the key.
- **`rag/chroma_store/`** is gitignored. Rebuild after changing documents: `python rag/build_index.py`.
- **`live_data.py` fallback rates** are hardcoded references. Update them periodically or swap in a live API.
- **Python 3.14** — some type hints use `dict | None` style (PEP 604). Fine on 3.14 but will break on <3.10.
- **No quality tooling yet.** If you add lint/typecheck/test, document the commands here.
