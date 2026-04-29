from __future__ import annotations

from typing import Any

from .config import Settings
from .http_client import request_json


def send_message(settings: Settings, text: str) -> bool:
    if not settings.telegram_configured:
        return False
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    request_json(
        "POST",
        url,
        payload={
            "chat_id": settings.telegram_chat_id,
            "text": text[:3900],
            "disable_web_page_preview": True,
        },
    )
    return True


def get_updates(settings: Settings) -> list[dict[str, Any]]:
    if not settings.telegram_bot_token or settings.telegram_bot_token.startswith("PASTE_"):
        return []
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/getUpdates"
    data = request_json("GET", url)
    result = data.get("result", [])
    return result if isinstance(result, list) else []

