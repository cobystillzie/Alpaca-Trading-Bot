from bot.guardrails import evaluate_candidate_for_order
from bot.models import TradeCandidate


def safe_candidate() -> TradeCandidate:
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
        source_urls=["https://example.com"],
    )


def test_guardrails_approve_safe_candidate():
    result = evaluate_candidate_for_order(
        safe_candidate(),
        {"portfolio_value": "100000", "buying_power": "50000", "cash": "50000"},
        [],
        today_order_count=0,
        managed_capital_usd=10000,
    )
    assert result.approved
    assert result.order_notional == 800


def test_guardrails_preserve_cash_reserve():
    result = evaluate_candidate_for_order(
        safe_candidate(),
        {"portfolio_value": "100000", "buying_power": "5000", "cash": "5000"},
        [],
        today_order_count=0,
        managed_capital_usd=10000,
    )
    assert result.approved
    assert result.order_notional == 800


def test_guardrails_preserve_managed_capital_cash_reserve():
    result = evaluate_candidate_for_order(
        safe_candidate(),
        {"portfolio_value": "100000", "buying_power": "50000", "cash": "50000"},
        [{"symbol": "SPY", "market_value": "8950"}],
        today_order_count=0,
        managed_capital_usd=10000,
    )
    assert not result.approved
    assert any("cash reserve" in reason for reason in result.reasons)
