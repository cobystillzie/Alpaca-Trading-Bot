from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any


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
            confidence=float(data.get("confidence", 0) or 0),
            horizon_days=int(float(data.get("horizon_days", 0) or 0)),
            target_allocation_percent=float(
                data.get("target_allocation_percent", 0) or 0
            ),
            stop_loss_percent=float(data.get("stop_loss_percent", 0) or 0),
            source_urls=[
                str(url).strip()
                for url in data.get("source_urls", [])
                if str(url).strip()
            ],
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

