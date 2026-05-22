import json
from datetime import datetime

from bot.config import Settings
from bot.perplexity import PerplexityQuotaError
from bot.runner import _weekly_provider_blocked_review


def settings(root) -> Settings:
    return Settings(
        root=root,
        alpaca_env="paper",
        alpaca_base_url="https://paper-api.alpaca.markets",
        alpaca_api_key="a",
        alpaca_secret_key="b",
        perplexity_api_key="pplx",
        telegram_bot_token="token",
        telegram_chat_id="123",
        auto_git_push=False,
        live_trading_enabled=False,
        managed_capital_usd=10000,
        perplexity_model="sonar-pro",
        perplexity_search_context="high",
        perplexity_recency="day",
        telegram_detail_level="checkpoint_full",
        social_buzz_weight=0.10,
        congressional_signal_weight=0.05,
        hf_research_enabled=True,
        hf_mode="hybrid",
        hf_cache_dir=".hf_cache",
        hf_allow_api_fallback=False,
        hf_token="",
    )


def test_weekly_provider_blocked_review_uses_local_memory(tmp_path):
    memory = tmp_path / "memory"
    memory.mkdir()
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    (memory / "WATCHLIST.md").write_text(
        "\n".join(
            [
                f"## Latest Candidates - {stamp} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| INTU | software fintech |",
                f"## Latest Candidates - {stamp} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| INTU | software fintech |",
                f"## Latest Candidates - {stamp} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| INTU | software fintech |",
            ]
        ),
        encoding="utf-8",
    )
    (memory / "REJECTED-TRADES.md").write_text(
        "\n".join(
            [
                "# Rejected Trades",
                f"## Rejected INTU - {stamp} Eastern Daylight Time",
                "",
                "Candidate references banned v1 instruments or leverage.",
            ]
        ),
        encoding="utf-8",
    )

    review = _weekly_provider_blocked_review(
        settings(tmp_path),
        PerplexityQuotaError("401 insufficient_quota"),
    )
    payload = json.loads(review)

    assert payload["status"] == "provider-blocked"
    assert any("INTU x3" in lesson for lesson in payload["concise_lessons"])
    assert payload["rejected_patterns"] == ["INTU: hard_banned"]
    assert payload["signal_component_assessment"]["social_buzz"].endswith("10%.")
