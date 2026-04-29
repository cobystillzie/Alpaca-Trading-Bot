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
    )

