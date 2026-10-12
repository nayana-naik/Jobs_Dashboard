"""AI client for generating one-line chart summaries via a local Ollama server.

Configure via a `.env` file at the project root (see `.env.example`):

    AI_BASE_URL   Required to enable summaries, e.g. "http://localhost:11434"
                  for a local Ollama server.
    AI_MODEL      Optional. Defaults to "qwen3.6".
"""

import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DEFAULT_MODEL = "qwen3.6"
FALLBACK_MESSAGE = "AI summaries unavailable — set AI_BASE_URL."

SYSTEM_PROMPT = (
    "You write a single short sentence (max 20 words, no markdown) stating the "
    "single most notable takeaway from the given chart data. Be specific and "
    "use numbers from the data when useful."
)


def _ollama_host() -> str | None:
    base_url = os.environ.get("AI_BASE_URL")
    if not base_url:
        return None
    # Accept a bare host or an OpenAI-compatible "/v1" style URL.
    return base_url.rstrip("/").removesuffix("/v1")


@st.cache_data(show_spinner=False, ttl=3600)
def get_chart_summary(chart_name: str, data_context: str) -> str:
    host = _ollama_host()
    if host is None:
        return FALLBACK_MESSAGE

    model = os.environ.get("AI_MODEL", DEFAULT_MODEL)
    try:
        response = requests.post(
            f"{host}/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f'Chart: "{chart_name}"\nData: {data_context}',
                    },
                ],
                "stream": False,
                "think": False,
                "options": {"temperature": 0.2},
            },
            timeout=30,
        )
        response.raise_for_status()
        summary = response.json().get("message", {}).get("content")
        return summary.strip() if summary else FALLBACK_MESSAGE
    except Exception:
        return "AI summary temporarily unavailable."
