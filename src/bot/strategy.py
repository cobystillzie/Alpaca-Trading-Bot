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

BASE_STRATEGY_WEIGHT = 0.70
CHITTICK_CASH_WEIGHT = 0.30
CHITTICK_SEED_WATCHLIST = {"GOOGL", "GOOG", "INTC", "USAR", "GT"}

VALUE_TERMS = (
    "margin of safety",
    "undervalued",
    "valuation",
    "free cash flow",
    "cash flow",
    "discount",
    "earnings yield",
    "downside",
    "asymmetric",
)
GROWTH_TERMS = (
    "growth",
    "runway",
    "tailwind",
    "demand",
    "operating leverage",
    "revenue",
    "catalyst",
    "durable",
)
QUALITY_TERMS = (
    "moat",
    "recurring",
    "balance sheet",
    "high margins",
    "cash flow quality",
    "capital allocation",
    "owner",
    "durable",
)
RISK_TERMS = (
    "debt",
    "dilution",
    "cyclical",
    "commodity",
    "execution risk",
    "valuation risk",
    "bear case",
    "downside",
)


def _source_looks_weak(url: str) -> bool:
    clean = url.lower()
    return any(hint in clean for hint in WEAK_SOURCE_HINTS)


def _signal_weight(candidate: TradeCandidate, key: str) -> float:
    return float(candidate.signal_weights.get(key, 0) or 0)


def normalize_alphabet_exposure(symbol: str) -> str:
    clean = str(symbol or "").upper().strip()
    return "GOOGL" if clean in {"GOOG", "GOOGL"} else clean


def _clamp_score(value: float) -> int:
    return max(0, min(100, int(round(value))))


def _has_any(text: str, terms: tuple[str, ...]) -> bool:
    clean = text.lower()
    return any(term in clean for term in terms)


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


def _has_chittick_reject_reason(text: str) -> bool:
    clean = " ".join(str(text or "").lower().split())
    if not clean:
        return False
    if clean in {"none", "n/a", "na", "no", "no reject", "not rejected"}:
        return False
    if clean.startswith(("pass", "passes", "passed")):
        return False
    return True


def chittick_reject_reason_text(candidate: TradeCandidate) -> str:
    return (
        candidate.chittick_reject_reason
        if _has_chittick_reject_reason(candidate.chittick_reject_reason)
        else ""
    )


def _chittick_text(candidate: TradeCandidate) -> str:
    return " ".join(
        [
            candidate.thesis,
            candidate.catalyst,
            candidate.quality_case,
            candidate.momentum_case,
            candidate.bear_case,
            candidate.margin_of_safety_case,
            candidate.valuation_case,
            candidate.growth_runway,
            candidate.balance_sheet_risk,
            candidate.capital_allocation_case,
            candidate.concentration_case,
            candidate.owner_hold_case,
            candidate.chittick_reject_reason,
        ]
    )


def chittick_cash_score(candidate: TradeCandidate) -> tuple[int, list[str]]:
    reasons: list[str] = []
    score = _clamp_score(candidate.chittick_cash_score)
    if score:
        reasons.append(f"Chittick Cash explicit subscore: {score}.")
    else:
        text = _chittick_text(candidate)
        if len(candidate.quality_case) >= 24:
            score += 20
            reasons.append("Chittick Cash: business quality explained.")
        if len(candidate.thesis) >= 24:
            score += 15
            reasons.append("Chittick Cash: owner-style thesis present.")
        if len(candidate.margin_of_safety_case) >= 24:
            score += 15
            reasons.append("Chittick Cash: margin-of-safety case present.")
        if len(candidate.valuation_case) >= 24:
            score += 15
            reasons.append("Chittick Cash: valuation case present.")
        if len(candidate.growth_runway) >= 24:
            score += 15
            reasons.append("Chittick Cash: growth runway present.")
        if len(candidate.capital_allocation_case) >= 24:
            score += 10
            reasons.append("Chittick Cash: capital allocation reviewed.")
        if len(candidate.concentration_case) >= 24:
            score += 10
            reasons.append("Chittick Cash: concentration case reviewed.")
        if len(candidate.owner_hold_case) >= 24:
            score += 15
            reasons.append("Chittick Cash: 30-180 day owner thesis present.")
        if len(candidate.balance_sheet_risk or candidate.bear_case) >= 24:
            score += 10
            reasons.append("Chittick Cash: downside or balance-sheet risk reviewed.")
        if _has_any(text, VALUE_TERMS):
            score += 15
            reasons.append("Chittick Cash: value or downside language detected.")
        if _has_any(text, GROWTH_TERMS):
            score += 15
            reasons.append("Chittick Cash: growth runway language detected.")
        if _has_any(text, QUALITY_TERMS):
            score += 10
            reasons.append("Chittick Cash: quality language detected.")
        if _has_any(text, RISK_TERMS):
            score += 10
            reasons.append("Chittick Cash: risk terms explicitly addressed.")
        if len(candidate.source_urls) >= 2:
            score += 10
            reasons.append("Chittick Cash: multiple sources cited.")
        elif candidate.source_urls:
            score += 5
            reasons.append("Chittick Cash: at least one source cited.")
        if candidate.confidence >= 0.75:
            score += 10
            reasons.append("Chittick Cash: high confidence.")
        elif candidate.confidence >= 0.60:
            score += 5
            reasons.append("Chittick Cash: acceptable confidence.")
        if normalize_alphabet_exposure(candidate.symbol) in CHITTICK_SEED_WATCHLIST and score >= 30:
            score += 5
            reasons.append("Chittick Cash: seed watchlist name, not an automatic buy.")

    if chittick_reject_reason_text(candidate):
        score = min(score, 35)
        reasons.append("Chittick Cash: reject reason caps the subscore.")
    return _clamp_score(score), reasons


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
- Apply the Chittick Cash filter as a 30% weighted strategy lens, not a hard gate.
- Chittick Cash prioritizes long-only concentrated-quality thinking, high margin of safety, real growth runway, balance-sheet risk review, and an owner-style 30-180 day thesis.
- Keep `horizon_days` between 1 and 10 for paper execution review. Put any 30-180 day owner thesis only in `owner_hold_case`.
- Chittick Cash seed watchlist: GOOGL/GOOG, INTC, USAR, GT. These are research priorities only, never automatic buys.
- Treat GOOG and GOOGL as equivalent Alphabet business exposure; default to GOOGL in candidate JSON unless there is a concrete reason to use GOOG.
- Read and obey SELF-LEARNING-POLICY.md from memory when it exists.
- Penalize stale repeated tickers when there is no fresh catalyst. Do not keep recycling GOOGL, NVDA, SPMO, or any other repeated name unless there is new earnings, filing, guidance, contract, upgrade, or confirmed breakout evidence.
- Build a broader discovery set. Aim for at least three diversity buckets across top candidates and include at least two alternatives from underrepresented sectors when a repeated mega-cap or broad ETF appears again.
- If a candidate was blocked by allocation or concentration constraints, propose a smaller safe tranche or a different-sector alternative instead of repeating the same target allocation.
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
      "strategy_tags": ["chittick_cash"],
      "chittick_cash_score": 72,
      "margin_of_safety_case": "valuation versus quality and downside protection",
      "valuation_case": "why the price is attractive or not versus business quality",
      "growth_runway": "30-180 day and longer-term growth drivers",
      "balance_sheet_risk": "debt, dilution, cyclicality, or balance-sheet risk",
      "capital_allocation_case": "management and reinvestment discipline",
      "concentration_case": "why this deserves attention over a broad ETF or better alternative",
      "owner_hold_case": "what would justify reviewing or holding over 30-180 days",
      "chittick_reject_reason": "",
      "hf_sentiment_score": 0.0,
      "hf_sentiment_label": "",
      "hf_source_quality_score": 0.0,
      "hf_hype_risk": 0.0,
      "hf_evidence_rank": 0.0,
      "hf_memory_similarity": 0.0,
      "hf_filter_vetoes": [],
      "hf_model_notes": "",
      "catalyst_type": "earnings/filing/news/momentum/structural/general",
      "fresh_catalyst": true,
      "repeat_count_48h": 0,
      "diversity_bucket": "mega-cap-internet-cloud",
      "research_tier": "execution-ready/watch/stale-watch/watch-allocation-constrained",
      "allocation_learning_note": "",
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
For Chittick Cash, pay special attention to GOOGL/GOOG, INTC, USAR, and GT when present in memory.
Do not recommend trades. Highlight balance-sheet, concentration, litigation, dilution, revenue quality, capital allocation, and valuation risks.

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
    base_score = 0
    reasons: list[str] = []
    rejects: list[str] = []
    joined = " ".join(
        [
            candidate.thesis,
            candidate.catalyst,
            candidate.quality_case,
            candidate.momentum_case,
            candidate.bear_case,
            candidate.margin_of_safety_case,
            candidate.valuation_case,
            candidate.growth_runway,
            candidate.balance_sheet_risk,
            candidate.capital_allocation_case,
            candidate.concentration_case,
            candidate.owner_hold_case,
            candidate.chittick_reject_reason,
            candidate.hf_model_notes,
            " ".join(candidate.hf_filter_vetoes),
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
    for veto in candidate.hf_filter_vetoes:
        rejects.append(veto)
    hf_active = bool(
        candidate.hf_model_notes
        or candidate.hf_filter_vetoes
        or candidate.hf_sentiment_label
        or candidate.hf_source_quality_score
        or candidate.hf_hype_risk
        or candidate.hf_evidence_rank
        or candidate.hf_memory_similarity
    )
    if hf_active and candidate.hf_source_quality_score < 30 and candidate.hf_hype_risk >= 0.60:
        rejects.append("HF source/hype filter rejects source-thin hype.")
    if hf_active and candidate.hf_memory_similarity >= 0.85:
        rejects.append("HF memory filter flags similarity to prior rejected patterns.")
    if candidate.research_tier == "execution-ready" and candidate.repeat_count_48h >= 3 and not candidate.fresh_catalyst:
        rejects.append("Repeated candidate cannot be execution-ready without a fresh catalyst.")
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
        base_score += 15
        reasons.append("Has a concrete thesis.")
    if candidate.catalyst:
        base_score += 20
        reasons.append("Has a catalyst.")
    if candidate.quality_case:
        base_score += 20
        reasons.append("Passes quality/business explanation check.")
    if candidate.momentum_case:
        base_score += 15
        reasons.append("Has momentum evidence.")
    if candidate.bear_case:
        base_score += 10
        reasons.append("Bear case documented.")
    if candidate.confidence >= 0.75:
        base_score += 10
        reasons.append("High confidence.")
    elif candidate.confidence >= 0.6:
        base_score += 5
        reasons.append("Acceptable confidence.")
    if candidate.source_urls:
        base_score += 10
        reasons.append("Has cited sources.")

    base_score = _clamp_score(base_score)
    chittick_score, chittick_reasons = chittick_cash_score(candidate)
    final_score = _clamp_score(
        (base_score * BASE_STRATEGY_WEIGHT)
        + (chittick_score * CHITTICK_CASH_WEIGHT)
    )
    if hf_active:
        hf_adjustment = 0
        if candidate.hf_source_quality_score >= 75 and candidate.hf_evidence_rank >= 70:
            hf_adjustment += 5
            reasons.append("HF filter: strong source quality and evidence rank.")
        elif 0 < candidate.hf_source_quality_score < 40:
            hf_adjustment -= 5
            reasons.append("HF filter: weak source quality reduces confidence.")
        if candidate.hf_hype_risk >= 0.60:
            hf_adjustment -= 5
            reasons.append("HF filter: high hype risk reduces confidence.")
        if candidate.hf_sentiment_label == "positive" and candidate.hf_sentiment_score >= 0.30:
            hf_adjustment += 2
            reasons.append("HF filter: sentiment is supportive but not sufficient alone.")
        elif candidate.hf_sentiment_label == "negative" and candidate.hf_sentiment_score <= -0.30:
            hf_adjustment -= 3
            reasons.append("HF filter: negative sentiment reduces confidence.")
        final_score = _clamp_score(final_score + hf_adjustment)
    if candidate.repeat_count_48h >= 3:
        if candidate.fresh_catalyst:
            reasons.append(
                f"Self-learning: repeat count {candidate.repeat_count_48h} allowed because a fresh catalyst is documented."
            )
        else:
            stale_penalty = min(15, 6 + candidate.repeat_count_48h)
            final_score = _clamp_score(final_score - stale_penalty)
            reasons.append(
                f"Self-learning: stale repeat penalty -{stale_penalty} for {candidate.repeat_count_48h} appearances without a fresh catalyst."
            )
    if candidate.research_tier == "stale-watch" and not candidate.fresh_catalyst:
        final_score = _clamp_score(final_score - 5)
        reasons.append("Self-learning: stale-watch tier reduces execution priority.")
    if candidate.allocation_learning_note:
        final_score = _clamp_score(final_score - 3)
        reasons.append("Self-learning: allocation constraint history requires smaller tranche or alternative.")
    if candidate.diversity_bucket:
        reasons.append(f"Self-learning diversity bucket: {candidate.diversity_bucket}.")
    reasons.extend(chittick_reasons)
    reasons.append(
        f"Final score blends existing strategy {base_score} at 70% and Chittick Cash {chittick_score} at 30%."
    )

    return ScoreResult(
        score=final_score,
        reasons=reasons,
        rejects=rejects,
        base_score=base_score,
        chittick_cash_score=chittick_score,
    )
