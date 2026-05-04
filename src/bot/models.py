from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any


def _float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _signal_weights(data: Any) -> dict[str, float]:
    if not isinstance(data, dict):
        return {}
    weights: dict[str, float] = {}
    for key, value in data.items():
        clean_key = str(key).strip()
        if clean_key:
            weights[clean_key] = _float(value)
    return weights


def _string_list(data: Any) -> list[str]:
    if not isinstance(data, list):
        return []
    return [str(item).strip() for item in data if str(item).strip()]


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class TradeCandidate:
    symbol: str
    thesis: str
    catalyst: str
    quality_case: str
    momentum_case: str
    bear_case: str
    confidence: float
    horizon_days: int
    target_allocation_percent: float
    stop_loss_percent: float
    source_urls: list[str] = field(default_factory=list)
    market_regime: str = ""
    sector: str = ""
    entry_plan: str = ""
    exit_plan: str = ""
    risk_reward: str = ""
    source_quality: str = ""
    recommendation: str = ""
    adversary_case: str = ""
    social_buzz: str = ""
    congressional_signal: str = ""
    signal_weights: dict[str, float] = field(default_factory=dict)
    strategy_tags: list[str] = field(default_factory=list)
    chittick_cash_score: float = 0.0
    margin_of_safety_case: str = ""
    valuation_case: str = ""
    growth_runway: str = ""
    balance_sheet_risk: str = ""
    capital_allocation_case: str = ""
    concentration_case: str = ""
    owner_hold_case: str = ""
    chittick_reject_reason: str = ""
    hf_sentiment_score: float = 0.0
    hf_sentiment_label: str = ""
    hf_sentiment_agreement: float = 0.0
    hf_source_quality_score: float = 0.0
    hf_hype_risk: float = 0.0
    hf_evidence_rank: float = 0.0
    hf_memory_similarity: float = 0.0
    hf_filter_vetoes: list[str] = field(default_factory=list)
    hf_model_notes: str = ""
    catalyst_type: str = ""
    fresh_catalyst: bool = False
    repeat_count_48h: int = 0
    diversity_bucket: str = ""
    research_tier: str = ""
    allocation_learning_note: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TradeCandidate":
        symbol = str(data.get("symbol", "")).upper().strip()
        symbol = re.sub(r"[^A-Z0-9.\-]", "", symbol)
        return cls(
            symbol=symbol,
            thesis=str(data.get("thesis", "")).strip(),
            catalyst=str(data.get("catalyst", "")).strip(),
            quality_case=str(data.get("quality_case", "")).strip(),
            momentum_case=str(data.get("momentum_case", "")).strip(),
            bear_case=str(data.get("bear_case", "")).strip(),
            confidence=_float(data.get("confidence")),
            horizon_days=int(_float(data.get("horizon_days"))),
            target_allocation_percent=float(
                data.get("target_allocation_percent", 0) or 0
            ),
            stop_loss_percent=_float(data.get("stop_loss_percent")),
            source_urls=[
                str(url).strip()
                for url in data.get("source_urls", [])
                if str(url).strip()
            ],
            market_regime=str(data.get("market_regime", "")).strip(),
            sector=str(data.get("sector", "")).strip(),
            entry_plan=str(data.get("entry_plan", "")).strip(),
            exit_plan=str(data.get("exit_plan", "")).strip(),
            risk_reward=str(data.get("risk_reward", "")).strip(),
            source_quality=str(data.get("source_quality", "")).strip(),
            recommendation=str(data.get("recommendation", "")).strip(),
            adversary_case=str(data.get("adversary_case", "")).strip(),
            social_buzz=str(data.get("social_buzz", "")).strip(),
            congressional_signal=str(data.get("congressional_signal", "")).strip(),
            signal_weights=_signal_weights(data.get("signal_weights")),
            strategy_tags=_string_list(data.get("strategy_tags")),
            chittick_cash_score=_float(data.get("chittick_cash_score")),
            margin_of_safety_case=str(data.get("margin_of_safety_case", "")).strip(),
            valuation_case=str(data.get("valuation_case", "")).strip(),
            growth_runway=str(data.get("growth_runway", "")).strip(),
            balance_sheet_risk=str(data.get("balance_sheet_risk", "")).strip(),
            capital_allocation_case=str(data.get("capital_allocation_case", "")).strip(),
            concentration_case=str(data.get("concentration_case", "")).strip(),
            owner_hold_case=str(data.get("owner_hold_case", "")).strip(),
            chittick_reject_reason=str(data.get("chittick_reject_reason", "")).strip(),
            hf_sentiment_score=_float(data.get("hf_sentiment_score")),
            hf_sentiment_label=str(data.get("hf_sentiment_label", "")).strip(),
            hf_sentiment_agreement=_float(data.get("hf_sentiment_agreement")),
            hf_source_quality_score=_float(data.get("hf_source_quality_score")),
            hf_hype_risk=_float(data.get("hf_hype_risk")),
            hf_evidence_rank=_float(data.get("hf_evidence_rank")),
            hf_memory_similarity=_float(data.get("hf_memory_similarity")),
            hf_filter_vetoes=_string_list(data.get("hf_filter_vetoes")),
            hf_model_notes=str(data.get("hf_model_notes", "")).strip(),
            catalyst_type=str(data.get("catalyst_type", "")).strip(),
            fresh_catalyst=_bool(data.get("fresh_catalyst")),
            repeat_count_48h=int(_float(data.get("repeat_count_48h"))),
            diversity_bucket=str(data.get("diversity_bucket", "")).strip(),
            research_tier=str(data.get("research_tier", "")).strip(),
            allocation_learning_note=str(data.get("allocation_learning_note", "")).strip(),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "thesis": self.thesis,
            "catalyst": self.catalyst,
            "quality_case": self.quality_case,
            "momentum_case": self.momentum_case,
            "bear_case": self.bear_case,
            "confidence": self.confidence,
            "horizon_days": self.horizon_days,
            "target_allocation_percent": self.target_allocation_percent,
            "stop_loss_percent": self.stop_loss_percent,
            "source_urls": self.source_urls,
            "market_regime": self.market_regime,
            "sector": self.sector,
            "entry_plan": self.entry_plan,
            "exit_plan": self.exit_plan,
            "risk_reward": self.risk_reward,
            "source_quality": self.source_quality,
            "recommendation": self.recommendation,
            "adversary_case": self.adversary_case,
            "social_buzz": self.social_buzz,
            "congressional_signal": self.congressional_signal,
            "signal_weights": self.signal_weights,
            "strategy_tags": self.strategy_tags,
            "chittick_cash_score": self.chittick_cash_score,
            "margin_of_safety_case": self.margin_of_safety_case,
            "valuation_case": self.valuation_case,
            "growth_runway": self.growth_runway,
            "balance_sheet_risk": self.balance_sheet_risk,
            "capital_allocation_case": self.capital_allocation_case,
            "concentration_case": self.concentration_case,
            "owner_hold_case": self.owner_hold_case,
            "chittick_reject_reason": self.chittick_reject_reason,
            "hf_sentiment_score": self.hf_sentiment_score,
            "hf_sentiment_label": self.hf_sentiment_label,
            "hf_sentiment_agreement": self.hf_sentiment_agreement,
            "hf_source_quality_score": self.hf_source_quality_score,
            "hf_hype_risk": self.hf_hype_risk,
            "hf_evidence_rank": self.hf_evidence_rank,
            "hf_memory_similarity": self.hf_memory_similarity,
            "hf_filter_vetoes": self.hf_filter_vetoes,
            "hf_model_notes": self.hf_model_notes,
            "catalyst_type": self.catalyst_type,
            "fresh_catalyst": self.fresh_catalyst,
            "repeat_count_48h": self.repeat_count_48h,
            "diversity_bucket": self.diversity_bucket,
            "research_tier": self.research_tier,
            "allocation_learning_note": self.allocation_learning_note,
        }


@dataclass(frozen=True)
class ScoreResult:
    score: int
    reasons: list[str]
    rejects: list[str]
    base_score: int = 0
    chittick_cash_score: int = 0

    @property
    def approved(self) -> bool:
        return not self.rejects and self.score >= 70


@dataclass(frozen=True)
class GuardrailResult:
    approved: bool
    reasons: list[str]
    warnings: list[str]
    order_notional: float = 0.0
