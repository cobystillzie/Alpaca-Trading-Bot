from __future__ import annotations

import json
import re

from .models import ScoreResult, TradeCandidate


BANNED_PATTERNS = [
    r"\boptions?\b",
    r"\bcall options?\b",
    r"\bput options?\b",
    r"\bcrypto\b",
    r"\bbuy(?:ing)? on margin\b",
    r"\bmargin loan\b",
    r"\bborrowed margin\b",
    r"\bportfolio margin\b",
    r"\bmargin borrowing\b",
    r"\bleverage(?:d)?\b",
    r"\bshort sell(?:ing)?\b",
    r"\bshort-selling\b",
    r"\bshort dated\b",
]


def research_prompt(memory_bundle: str) -> str:
    return f"""
You are the research agent for a paper-trading bot.

Strategy:
- Stocks/ETFs only.
- No options, crypto, margin, or short selling.
- Blend quality businesses, clear catalysts, and momentum.
- Prefer 1-10 day swing trades only when there is a strong catalyst and defined risk.
- Apply Buffett/Munger quality discipline and YC-style evidence-based iteration.

Return strict JSON only:
{{
  "summary": "short market summary",
  "candidates": [
    {{
      "symbol": "MSFT",
      "thesis": "why this is a good business/trade",
      "catalyst": "specific catalyst",
      "quality_case": "business quality and margin of safety notes",
      "momentum_case": "relative strength/trend/volume notes",
      "bear_case": "why this can fail",
      "confidence": 0.72,
      "horizon_days": 5,
      "target_allocation_percent": 8,
      "stop_loss_percent": 8,
      "source_urls": ["https://..."]
    }}
  ]
}}

Existing memory:
{memory_bundle[-12000:]}
""".strip()


def extract_json_object(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = re.sub(r"```$", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.S)
        if not match:
            return {}
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return {}


def extract_candidates(text: str) -> tuple[str, list[TradeCandidate]]:
    data = extract_json_object(text)
    summary = str(data.get("summary", "")).strip()
    raw_candidates = data.get("candidates", [])
    candidates: list[TradeCandidate] = []
    if isinstance(raw_candidates, list):
        for item in raw_candidates:
            if isinstance(item, dict):
                candidate = TradeCandidate.from_dict(item)
                if candidate.symbol:
                    candidates.append(candidate)
    return summary, candidates


def score_candidate(candidate: TradeCandidate) -> ScoreResult:
    score = 0
    reasons: list[str] = []
    rejects: list[str] = []
    joined = " ".join(
        [
            candidate.thesis,
            candidate.catalyst,
            candidate.quality_case,
            candidate.momentum_case,
            candidate.bear_case,
        ]
    ).lower()

    if not candidate.symbol:
        rejects.append("Missing symbol.")
    if any(re.search(pattern, joined) for pattern in BANNED_PATTERNS):
        rejects.append("Candidate references banned v1 instruments or leverage.")
    if candidate.confidence < 0.6:
        rejects.append("Confidence below 0.60.")
    if not (1 <= candidate.horizon_days <= 10):
        rejects.append("Horizon must be 1-10 trading days.")
    if not (1 <= candidate.target_allocation_percent <= 15):
        rejects.append("Target allocation must be between 1% and 15%.")
    if not (3 <= candidate.stop_loss_percent <= 12):
        rejects.append("Stop loss must be between 3% and 12%.")

    required_fields = {
        "thesis": candidate.thesis,
        "catalyst": candidate.catalyst,
        "quality case": candidate.quality_case,
        "momentum case": candidate.momentum_case,
        "bear case": candidate.bear_case,
    }
    for name, value in required_fields.items():
        if len(value) < 24:
            rejects.append(f"Missing or thin {name}.")

    if candidate.thesis:
        score += 15
        reasons.append("Has a concrete thesis.")
    if candidate.catalyst:
        score += 20
        reasons.append("Has a catalyst.")
    if candidate.quality_case:
        score += 20
        reasons.append("Passes quality/business explanation check.")
    if candidate.momentum_case:
        score += 15
        reasons.append("Has momentum evidence.")
    if candidate.bear_case:
        score += 10
        reasons.append("Bear case documented.")
    if candidate.confidence >= 0.75:
        score += 10
        reasons.append("High confidence.")
    elif candidate.confidence >= 0.6:
        score += 5
        reasons.append("Acceptable confidence.")
    if candidate.source_urls:
        score += 10
        reasons.append("Has cited sources.")

    return ScoreResult(score=min(score, 100), reasons=reasons, rejects=rejects)
