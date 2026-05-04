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
        strategy_tags=["chittick_cash"],
        chittick_cash_score=78,
        margin_of_safety_case="Valuation is reasonable versus durable cash flow.",
        valuation_case="Multiple is acceptable relative to balance-sheet quality.",
        growth_runway="Cloud and AI demand support a 30-180 day owner review.",
        balance_sheet_risk="Balance sheet risk is low but expectations can reset.",
        capital_allocation_case="Capital allocation remains disciplined.",
        concentration_case="Quality and liquidity justify focused attention.",
        owner_hold_case="Owner thesis remains intact while cloud demand holds.",
        hf_sentiment_label="positive",
        hf_sentiment_score=0.45,
        hf_sentiment_agreement=0.70,
        hf_source_quality_score=92,
        hf_hype_risk=0.05,
        hf_evidence_rank=95,
        hf_memory_similarity=0.22,
        hf_model_notes="HF staged filter used finance sentiment, source classifier, reranker, and embeddings.",
        catalyst_type="earnings",
        fresh_catalyst=True,
        repeat_count_48h=3,
        diversity_bucket="software-cloud",
        research_tier="execution-ready",
        allocation_learning_note="No current allocation block.",
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
    assert "Chittick Cash Filter" in memo
    assert "Self-Learning Filter" in memo
    assert "Fresh catalyst: yes" in memo
    assert "Repeat count, 48h: 3" in memo
    assert "Research tier: execution-ready" in memo
    assert "Hugging Face Filter" in memo
    assert "Source quality: 92/100" in memo
    assert "Owner thesis, 30-180 days" in memo
    assert "Chittick reject reason: none" in memo
    assert "Social buzz, max 10%" in memo
    assert "Congress signal, max 5%" in memo
    assert "Execute only if guardrails pass" in memo
