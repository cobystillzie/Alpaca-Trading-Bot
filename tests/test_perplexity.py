from bot.config import Settings
from bot.perplexity import build_sonar_payload


def settings() -> Settings:
    return Settings(
        root=None,  # type: ignore[arg-type]
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


def test_build_sonar_payload_uses_research_controls():
    payload = build_sonar_payload(
        settings(),
        "research",
        search_mode="sec",
        search_domain_filter=["sec.gov", "investor.apple.com"],
    )

    assert payload["model"] == "sonar-pro"
    assert payload["web_search_options"]["search_context_size"] == "high"
    assert payload["search_recency_filter"] == "day"
    assert payload["search_mode"] == "sec"
    assert payload["search_domain_filter"] == ["sec.gov", "investor.apple.com"]
