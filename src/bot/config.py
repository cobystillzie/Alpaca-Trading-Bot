from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _env(name: str, file_values: dict[str, str], default: str = "") -> str:
    return os.environ.get(name) or file_values.get(name, default)


def _bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _float(value: str, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _bounded_float(value: str, default: float, low: float, high: float) -> float:
    parsed = _float(value, default)
    if parsed < low:
        return low
    if parsed > high:
        return high
    return parsed


def _is_placeholder(value: str) -> bool:
    return not value or value.startswith("PASTE_")


@dataclass(frozen=True)
class Settings:
    root: Path
    alpaca_env: str
    alpaca_base_url: str
    alpaca_api_key: str
    alpaca_secret_key: str
    perplexity_api_key: str
    telegram_bot_token: str
    telegram_chat_id: str
    auto_git_push: bool
    live_trading_enabled: bool
    managed_capital_usd: float
    perplexity_model: str
    perplexity_search_context: str
    perplexity_recency: str
    telegram_detail_level: str
    social_buzz_weight: float
    congressional_signal_weight: float

    @property
    def is_paper(self) -> bool:
        return (
            self.alpaca_env.lower() == "paper"
            and "paper-api.alpaca.markets" in self.alpaca_base_url
            and not self.live_trading_enabled
        )

    @property
    def alpaca_configured(self) -> bool:
        return not _is_placeholder(self.alpaca_api_key) and not _is_placeholder(
            self.alpaca_secret_key
        )

    @property
    def perplexity_configured(self) -> bool:
        return not _is_placeholder(self.perplexity_api_key)

    @property
    def telegram_configured(self) -> bool:
        return not _is_placeholder(self.telegram_bot_token) and not _is_placeholder(
            self.telegram_chat_id
        )

    def setup_issues(self) -> list[str]:
        issues: list[str] = []
        if not self.is_paper:
            issues.append(
                "Alpaca must be paper-only: use ALPACA_ENV=paper, paper base URL, and LIVE_TRADING_ENABLED=false."
            )
        if not self.alpaca_configured:
            issues.append("Missing Alpaca paper API key or secret.")
        if not self.perplexity_configured:
            issues.append("Missing Perplexity API key.")
        if not self.telegram_configured:
            issues.append("Missing Telegram bot token or chat id.")
        if self.managed_capital_usd <= 0:
            issues.append("MANAGED_CAPITAL_USD must be greater than 0.")
        if self.perplexity_search_context not in {"low", "medium", "high"}:
            issues.append("PERPLEXITY_SEARCH_CONTEXT must be low, medium, or high.")
        if self.social_buzz_weight > 0.10:
            issues.append("SOCIAL_BUZZ_WEIGHT must be 0.10 or lower.")
        if self.congressional_signal_weight > 0.05:
            issues.append("CONGRESSIONAL_SIGNAL_WEIGHT must be 0.05 or lower.")
        return issues


def load_settings(root: Path | None = None) -> Settings:
    resolved_root = root or repo_root()
    file_values = _read_env_file(resolved_root / ".env.local")
    return Settings(
        root=resolved_root,
        alpaca_env=_env("ALPACA_ENV", file_values, "paper"),
        alpaca_base_url=_env(
            "ALPACA_BASE_URL", file_values, "https://paper-api.alpaca.markets"
        ).rstrip("/"),
        alpaca_api_key=_env("ALPACA_API_KEY", file_values),
        alpaca_secret_key=_env("ALPACA_SECRET_KEY", file_values),
        perplexity_api_key=_env("PERPLEXITY_API_KEY", file_values),
        telegram_bot_token=_env("TELEGRAM_BOT_TOKEN", file_values),
        telegram_chat_id=_env("TELEGRAM_CHAT_ID", file_values),
        auto_git_push=_bool(_env("AUTO_GIT_PUSH", file_values, "false")),
        live_trading_enabled=_bool(_env("LIVE_TRADING_ENABLED", file_values, "false")),
        managed_capital_usd=_float(_env("MANAGED_CAPITAL_USD", file_values, "10000"), 10000),
        perplexity_model=_env("PERPLEXITY_MODEL", file_values, "sonar-pro"),
        perplexity_search_context=_env(
            "PERPLEXITY_SEARCH_CONTEXT", file_values, "high"
        ).lower(),
        perplexity_recency=_env("PERPLEXITY_RECENCY", file_values, "day").lower(),
        telegram_detail_level=_env(
            "TELEGRAM_DETAIL_LEVEL", file_values, "checkpoint_full"
        ).lower(),
        social_buzz_weight=_bounded_float(
            _env("SOCIAL_BUZZ_WEIGHT", file_values, "0.10"), 0.10, 0.0, 0.10
        ),
        congressional_signal_weight=_bounded_float(
            _env("CONGRESSIONAL_SIGNAL_WEIGHT", file_values, "0.05"), 0.05, 0.0, 0.05
        ),
    )
