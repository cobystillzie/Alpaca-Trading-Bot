from __future__ import annotations

from .config import Settings
from .http_client import request_json


PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"


def run_sonar_research(settings: Settings, prompt: str) -> str:
    if not settings.perplexity_configured:
        return (
            '{"summary":"Perplexity API key is missing. No live research was run.",'
            '"candidates":[]}'
        )
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": "You are a cautious paper-trading research analyst. Return only valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    data = request_json(
        "POST",
        PERPLEXITY_URL,
        headers={"Authorization": f"Bearer {settings.perplexity_api_key}"},
        payload=payload,
        timeout=60,
    )
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return '{"summary":"Perplexity returned an unexpected response shape.","candidates":[]}'

