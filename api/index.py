"""Sika AI — FastAPI entrypoint for Vercel (api/index.py)."""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from main import chat

app = FastAPI(title="Sika AI")

WEB_DIR = Path(__file__).resolve().parent.parent / "web"


class ChatRequest(BaseModel):
    user_message: str
    history: list[dict] | None = None


@app.get("/", response_class=HTMLResponse)
def index():
    return (WEB_DIR / "index.html").read_text(encoding="utf-8")


@app.get("/api/health")
def health():
    return {"status": "ok", "model": os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")}


@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    try:
        reply, history = chat(req.user_message, req.history or [])
        return {"reply": reply, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
