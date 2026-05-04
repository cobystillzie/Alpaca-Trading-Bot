from __future__ import annotations

from typing import Any

from .config import Settings
from .http_client import request_json
from .models import TradeCandidate
from .strategy import chittick_cash_score, chittick_reject_reason_text


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
    chittick_score, _ = chittick_cash_score(candidate)
    parts = [
        f"{index}. {candidate.symbol} ({candidate.sector or 'unclassified'})",
        f"confidence {candidate.confidence:.2f}",
        f"allocation {candidate.target_allocation_percent:.1f}%",
        f"stop {candidate.stop_loss_percent:.1f}%",
        f"Chittick {chittick_score}/100",
    ]
    if candidate.research_tier or candidate.diversity_bucket:
        parts.append(f"tier {candidate.research_tier or 'watch'}")
        parts.append(f"bucket {candidate.diversity_bucket or 'other'}")
    if candidate.hf_model_notes or candidate.hf_source_quality_score or candidate.hf_filter_vetoes:
        parts.append(f"HF source {candidate.hf_source_quality_score:.0f}/100")
        if candidate.hf_filter_vetoes:
            parts.append("HF veto")
    return " | ".join(parts)


def _hf_filter_lines(candidate: TradeCandidate) -> list[str]:
    if not (
        candidate.hf_model_notes
        or candidate.hf_sentiment_label
        or candidate.hf_source_quality_score
        or candidate.hf_hype_risk
        or candidate.hf_evidence_rank
        or candidate.hf_memory_similarity
        or candidate.hf_filter_vetoes
    ):
        return ["Hugging Face Filter", "Not run for this candidate."]
    return [
        "Hugging Face Filter",
        f"Sentiment: {candidate.hf_sentiment_label or 'none'} ({candidate.hf_sentiment_score:.2f}), agreement {candidate.hf_sentiment_agreement:.2f}",
        f"Source quality: {candidate.hf_source_quality_score:.0f}/100",
        f"Hype risk: {candidate.hf_hype_risk:.2f}",
        f"Evidence rank: {candidate.hf_evidence_rank:.0f}/100",
        f"Memory similarity: {candidate.hf_memory_similarity:.2f}",
        f"Vetoes: {_short('; '.join(candidate.hf_filter_vetoes), 260)}",
        f"Model notes: {_short(candidate.hf_model_notes, 300)}",
    ]


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
                f"Chittick Cash: {_short(candidate.margin_of_safety_case or candidate.valuation_case or candidate.owner_hold_case, 220)}",
                f"HF filter: sentiment={candidate.hf_sentiment_label or 'not run'} source={candidate.hf_source_quality_score:.0f}/100 hype={candidate.hf_hype_risk:.2f} vetoes={len(candidate.hf_filter_vetoes)}",
                f"Self-learning: tier={candidate.research_tier or 'watch'} repeat48h={candidate.repeat_count_48h} fresh={'yes' if candidate.fresh_catalyst else 'no'} bucket={candidate.diversity_bucket or 'other'}",
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
        chittick_score, _ = chittick_cash_score(candidate)
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
                "Chittick Cash Filter",
                f"Score: {chittick_score}/100",
                f"Margin of safety: {_short(candidate.margin_of_safety_case, 240)}",
                f"Valuation: {_short(candidate.valuation_case, 240)}",
                f"Growth runway: {_short(candidate.growth_runway, 240)}",
                f"Balance-sheet risk: {_short(candidate.balance_sheet_risk, 220)}",
                f"Capital allocation: {_short(candidate.capital_allocation_case, 220)}",
                f"Concentration case: {_short(candidate.concentration_case, 240)}",
                f"Owner thesis, 30-180 days: {_short(candidate.owner_hold_case, 260)}",
                f"Chittick reject reason: {_short(chittick_reject_reason_text(candidate), 220)}",
                "Self-Learning Filter",
                f"Catalyst type: {_short(candidate.catalyst_type, 120)}",
                f"Fresh catalyst: {'yes' if candidate.fresh_catalyst else 'no'}",
                f"Repeat count, 48h: {candidate.repeat_count_48h}",
                f"Diversity bucket: {_short(candidate.diversity_bucket, 160)}",
                f"Research tier: {_short(candidate.research_tier, 160)}",
                f"Allocation learning: {_short(candidate.allocation_learning_note, 240)}",
                *_hf_filter_lines(candidate),
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
