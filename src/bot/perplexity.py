from __future__ import annotations

from typing import Any

from .config import Settings
from .http_client import HttpClientError
from .http_client import request_json


PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"


class PerplexityQuotaError(RuntimeError):
    pass


def _is_quota_error(exc: HttpClientError) -> bool:
    text = str(exc).lower()
    return "401" in text and ("insufficient_quota" in text or "exceeded your current quota" in text)


def build_sonar_payload(
    settings: Settings,
    prompt: str,
    *,
    system_content: str | None = None,
    search_mode: str | None = None,
    search_domain_filter: list[str] | None = None,
    search_context_size: str | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model or settings.perplexity_model,
        "messages": [
            {
                "role": "system",
                "content": system_content
                or "You are a cautious paper-trading research analyst. Return only valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "web_search_options": {
            "search_context_size": search_context_size
            or settings.perplexity_search_context
        },
    }
    if settings.perplexity_recency:
        payload["search_recency_filter"] = settings.perplexity_recency
    if search_mode:
        payload["search_mode"] = search_mode
    if search_domain_filter:
        payload["search_domain_filter"] = search_domain_filter[:20]
    return payload


def run_sonar_research(
    settings: Settings,
    prompt: str,
    *,
    system_content: str | None = None,
    search_mode: str | None = None,
    search_domain_filter: list[str] | None = None,
    search_context_size: str | None = None,
    model: str | None = None,
) -> str:
    if not settings.perplexity_configured:
        return (
            '{"summary":"Perplexity API key is missing. No live research was run.",'
            '"candidates":[]}'
        )
    payload = build_sonar_payload(
        settings,
        prompt,
        system_content=system_content,
        search_mode=search_mode,
        search_domain_filter=search_domain_filter,
        search_context_size=search_context_size,
        model=model,
    )
    try:
        data = request_json(
            "POST",
            PERPLEXITY_URL,
            headers={"Authorization": f"Bearer {settings.perplexity_api_key}"},
            payload=payload,
            timeout=60,
        )
    except HttpClientError as exc:
        if _is_quota_error(exc):
            raise PerplexityQuotaError(str(exc)) from exc
        raise
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return '{"summary":"Perplexity returned an unexpected response shape.","candidates":[]}'
