"""Vercel-compatible entrypoint: re-exports the FastAPI app.

The real app lives in api/index.py. This thin shim exists so every Vercel
entrypoint-detection path (which scans root files like app.py/server.py/
main.py for a top-level `app`) can find it. The declared entrypoint in
pyproject.toml ([tool.vercel] entrypoint = "api.index:app") takes priority;
this is just a fallback for older versions of the builder.
"""
from api.index import app

__all__ = ["app"]
