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
        }


@dataclass(frozen=True)
class ScoreResult:
    score: int
    reasons: list[str]
    rejects: list[str]

    @property
    def approved(self) -> bool:
        return not self.rejects and self.score >= 70


@dataclass(frozen=True)
class GuardrailResult:
    approved: bool
    reasons: list[str]
    warnings: list[str]
    order_notional: float = 0.0
