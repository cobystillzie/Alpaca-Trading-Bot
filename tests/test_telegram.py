from bot.models import TradeCandidate
from bot.telegram import format_analyst_memo, split_telegram_text


def candidate() -> TradeCandidate:
    return TradeCandidate(
        symbol="MSFT",
        thesis="Microsoft has durable enterprise demand and resilient cloud economics.",
        catalyst="Cloud demand and AI infrastructure spending remain visible this week.",
        quality_case="The business has recurring revenue, high margins, and a strong balance sheet.",
        momentum_case="Shares show relative strength and a clean trend versus software peers.",
        bear_case="Valuation can compress if AI spending expectations weaken.",
        confidence=0.76,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=8,
        source_urls=["https://investor.microsoft.com", "https://www.sec.gov"],
        market_regime="Risk-on but selective.",
        sector="Software",
        entry_plan="Enter only after guardrails pass.",
        exit_plan="Exit on thesis break or stop.",
        risk_reward="Defined downside with catalyst-backed upside.",
        source_quality="Official company and SEC sources.",
        recommendation="Execute if guardrails pass.",
        adversary_case="AI expectations can reset lower.",
        social_buzz="Discussion is elevated but low weight.",
        congressional_signal="No decisive disclosure signal.",
        signal_weights={"social_buzz": 0.05, "congressional_signal": 0.0},
    )


def test_split_telegram_text_keeps_chunks_under_limit():
    chunks = split_telegram_text("word " * 3000, limit=1000)
    assert len(chunks) > 1
    assert all(len(chunk) <= 1000 for chunk in chunks)


def test_analyst_memo_includes_required_sections():
    memo = format_analyst_memo(
        "Premarket Analyst Memo",
        summary="Market is constructive.",
        candidates=[candidate()],
        action="Execute only if guardrails pass.",
    )

    assert "Market Regime" in memo
    assert "Top Candidates" in memo
    assert "Social buzz, max 10%" in memo
    assert "Congress signal, max 5%" in memo
    assert "Execute only if guardrails pass" in memo
