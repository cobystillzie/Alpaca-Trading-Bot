from bot.config import load_settings


def test_env_file_loading(tmp_path):
    (tmp_path / ".env.local").write_text(
        "\n".join(
            [
                "ALPACA_ENV=paper",
                "ALPACA_BASE_URL=https://paper-api.alpaca.markets",
                "ALPACA_API_KEY=abc",
                "ALPACA_SECRET_KEY=def",
                "PERPLEXITY_API_KEY=pplx",
                "TELEGRAM_BOT_TOKEN=token",
                "TELEGRAM_CHAT_ID=123",
                "AUTO_GIT_PUSH=true",
                "LIVE_TRADING_ENABLED=false",
                "MANAGED_CAPITAL_USD=10000",
            ]
        ),
        encoding="utf-8",
    )
    settings = load_settings(tmp_path)
    assert settings.is_paper
    assert settings.alpaca_configured
    assert settings.perplexity_configured
    assert settings.telegram_configured
    assert settings.auto_git_push
    assert settings.managed_capital_usd == 10000
