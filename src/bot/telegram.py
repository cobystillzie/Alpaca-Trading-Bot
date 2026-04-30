from __future__ import annotations

from typing import Any

from .config import Settings
from .http_client import request_json
from .models import TradeCandidate


TELEGRAM_LIMIT = 3900


def split_telegram_text(text: str, limit: int = TELEGRAM_LIMIT) -> list[str]:
    clean = text.strip()
    if not clean:
        return []
    chunks: list[str] = []
    while len(clean) > limit:
        split_at = clean.rfind("\n\n", 0, limit)
        if split_at < limit // 2:
            split_at = clean.rfind("\n", 0, limit)
        if split_at < limit // 2:
            split_at = clean.rfind(" ", 0, limit)
        if split_at < limit // 2:
            split_at = limit
        chunks.append(clean[:split_at].strip())
        clean = clean[split_at:].strip()
    if clean:
        chunks.append(clean)
    return chunks


def _short(text: str, limit: int = 360) -> str:
    clean = " ".join(str(text or "").split())
    if len(clean) <= limit:
        return clean or "none"
    return clean[: limit - 3].rstrip() + "..."


def _candidate_line(candidate: TradeCandidate, index: int) -> str:
    parts = [
        f"{index}. {candidate.symbol} ({candidate.sector or 'unclassified'})",
        f"confidence {candidate.confidence:.2f}",
        f"allocation {candidate.target_allocation_percent:.1f}%",
        f"stop {candidate.stop_loss_percent:.1f}%",
    ]
    return " | ".join(parts)


def format_research_update(summary: str, candidates: list[TradeCandidate]) -> str:
    lines = [
        "Research Update",
        "",
        f"Market tone: {_short(summary, 700)}",
        f"Candidates: {len(candidates)}",
    ]
    for index, candidate in enumerate(candidates[:5], start=1):
        lines.extend(
            [
                "",
                _candidate_line(candidate, index),
                f"Recommendation: {_short(candidate.recommendation, 180)}",
                f"Catalyst: {_short(candidate.catalyst, 240)}",
                f"Social buzz, low weight: {_short(candidate.social_buzz, 180)}",
                f"Congress signal, low weight: {_short(candidate.congressional_signal, 180)}",
            ]
        )
    return "\n".join(lines)


def format_analyst_memo(
    title: str,
    *,
    summary: str,
    candidates: list[TradeCandidate] | None = None,
    portfolio: str | None = None,
    action: str | None = None,
    rejected: list[str] | None = None,
) -> str:
    candidates = candidates or []
    lines = [
        title,
        "",
        f"Recommendation: {_short(action or 'Review the memo and follow guardrails.', 500)}",
        "",
        "Market Regime",
        _short(summary, 900),
    ]
    if portfolio:
        lines.extend(["", "Portfolio", _short(portfolio, 900)])
    lines.extend(["", "Top Candidates"])
    if not candidates:
        lines.append("No current candidates.")
    for index, candidate in enumerate(candidates[:6], start=1):
        lines.extend(
            [
                "",
                _candidate_line(candidate, index),
                f"Thesis: {_short(candidate.thesis, 360)}",
                f"Catalyst: {_short(candidate.catalyst, 300)}",
                f"Entry: {_short(candidate.entry_plan, 260)}",
                f"Exit: {_short(candidate.exit_plan, 260)}",
                f"Risk/reward: {_short(candidate.risk_reward, 260)}",
                f"Bear/adversary: {_short(candidate.adversary_case or candidate.bear_case, 300)}",
                f"Source quality: {_short(candidate.source_quality, 260)}",
                f"Social buzz, max 10%: {_short(candidate.social_buzz, 220)}",
                f"Congress signal, max 5%: {_short(candidate.congressional_signal, 220)}",
                f"Sources: {_short(', '.join(candidate.source_urls[:4]), 420)}",
            ]
        )
    if rejected:
        lines.extend(["", "Rejected / Watchouts"])
        lines.extend(f"- {_short(item, 300)}" for item in rejected[:8])
    return "\n".join(lines)


def send_message(settings: Settings, text: str) -> bool:
    if not settings.telegram_configured:
        return False
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    for chunk in split_telegram_text(text):
        request_json(
            "POST",
            url,
            payload={
                "chat_id": settings.telegram_chat_id,
                "text": chunk,
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
