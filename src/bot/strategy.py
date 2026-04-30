from __future__ import annotations

import json
import re

from .config import Settings
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


WEAK_SOURCE_HINTS = [
    "best-swing",
    "best swing",
    "best-stocks",
    "top-stocks",
    "top stocks",
    "listicle",
]


def _source_looks_weak(url: str) -> bool:
    clean = url.lower()
    return any(hint in clean for hint in WEAK_SOURCE_HINTS)


def _signal_weight(candidate: TradeCandidate, key: str) -> float:
    return float(candidate.signal_weights.get(key, 0) or 0)


def _has_signal_text(text: str) -> bool:
    clean = " ".join(str(text or "").lower().split())
    if not clean:
        return False
    return clean not in {
        "none",
        "n/a",
        "na",
        "no",
        "no signal",
        "no decisive signal",
        "no decisive disclosure signal",
    }


def research_prompt(
    memory_bundle: str,
    *,
    settings: Settings | None = None,
    research_context: dict[str, str] | None = None,
) -> str:
    social_weight = settings.social_buzz_weight if settings else 0.10
    congressional_weight = (
        settings.congressional_signal_weight if settings else 0.05
    )
    context_block = ""
    if research_context:
        context_block = "\n\nResearch context from earlier passes:\n"
        for name, value in research_context.items():
            context_block += f"\n--- {name} ---\n{value[-4000:]}\n"
    return f"""
You are the research agent for a paper-trading bot.

Strategy:
- Stocks/ETFs only.
- No options, crypto, margin, or short selling.
- Blend quality businesses, clear catalysts, and momentum.
- Prefer 1-10 day swing trades only when there is a strong catalyst and defined risk.
- Apply Buffett/Munger quality discipline and YC-style evidence-based iteration.
- Use social buzz only as attention/volume anomaly context. Maximum influence: {social_weight:.2f}.
- Use congressional disclosures only as weak secondary catalyst context. Maximum influence: {congressional_weight:.2f}.
- Social buzz and congressional disclosures must never be the main reason for a trade.
- Reject or set confidence below 0.60 for hype-only, source-thin, or listicle-only candidates.
- Prefer official/company, SEC, exchange/ETF sponsor, earnings, reputable financial news, and market data sources.

Return strict JSON only:
{{
  "summary": "short market summary",
  "market_regime": "risk-on/risk-off/neutral and why",
  "candidates": [
    {{
      "symbol": "MSFT",
      "thesis": "why this is a good business/trade",
      "catalyst": "specific catalyst",
      "quality_case": "business quality and margin of safety notes",
      "momentum_case": "relative strength/trend/volume notes",
      "bear_case": "why this can fail",
      "market_regime": "how the broad market affects this trade",
      "sector": "sector or ETF category",
      "entry_plan": "specific paper-trade entry plan",
      "exit_plan": "profit-taking and invalidation plan",
      "risk_reward": "risk/reward in plain English",
      "source_quality": "why the evidence is strong or weak",
      "recommendation": "hold, avoid, watch, or execute-if-guards-pass",
      "adversary_case": "strongest objection before execution",
      "social_buzz": "low-weight social attention signal, or none",
      "congressional_signal": "low-weight congressional disclosure signal, or none",
      "signal_weights": {{"social_buzz": 0.00, "congressional_signal": 0.00}},
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
{context_block}
""".strip()


def market_regime_prompt(memory_bundle: str) -> str:
    return f"""
Return strict JSON only with keys summary, market_regime, sector_rotation, risk_flags, source_urls.
Analyze the current US equity market tone for a paper-trading bot using high-quality sources.
Focus on index trend, rates/Fed, volatility, earnings tone, sector rotation, and risk-on/risk-off conditions.
No trade recommendations.

Existing memory:
{memory_bundle[-8000:]}
""".strip()


def social_buzz_prompt(memory_bundle: str) -> str:
    return f"""
Return strict JSON only with keys summary, social_buzz, attention_anomalies, source_urls.
Scan public web/social-attention coverage for unusual discussion around liquid US stocks/ETFs.
Treat this as weak context only. Do not recommend trades. Do not let hype override fundamentals.
Flag suspected hype, pump language, or unsupported claims as risk.

Existing memory:
{memory_bundle[-8000:]}
""".strip()


def congressional_prompt(memory_bundle: str) -> str:
    return f"""
Return strict JSON only with keys summary, congressional_signal, tickers, source_urls.
Scan public congressional disclosure sources for recently reported trades relevant to liquid US stocks/ETFs.
Treat disclosures as low-weight, delayed, secondary catalyst context only. Do not recommend trades.

Existing memory:
{memory_bundle[-8000:]}
""".strip()


def sec_quality_prompt(memory_bundle: str) -> str:
    return f"""
Return strict JSON only with keys summary, filing_risks, quality_notes, source_urls.
Use SEC/company filing evidence to identify business-quality risks and durable-demand evidence for current watchlist names.
Do not recommend trades. Highlight balance-sheet, concentration, litigation, revenue quality, and valuation risks.

Existing memory:
{memory_bundle[-8000:]}
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
    if _signal_weight(candidate, "social_buzz") > 0.10:
        rejects.append("Social buzz weight exceeds the 10% maximum.")
    if _signal_weight(candidate, "congressional_signal") > 0.05:
        rejects.append("Congressional signal weight exceeds the 5% maximum.")
    has_low_weight_signal = (
        _signal_weight(candidate, "social_buzz") > 0
        or _signal_weight(candidate, "congressional_signal") > 0
        or _has_signal_text(candidate.social_buzz)
        or _has_signal_text(candidate.congressional_signal)
    )
    if has_low_weight_signal and len(candidate.source_urls) < 2:
        rejects.append("Low-weight social/congress signal needs at least two stronger sources.")
    if candidate.source_urls and all(_source_looks_weak(url) for url in candidate.source_urls):
        rejects.append("Candidate relies only on weak/listicle-style sources.")
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
