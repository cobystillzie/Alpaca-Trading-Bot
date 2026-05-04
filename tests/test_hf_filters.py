from pathlib import Path

from bot.config import Settings
from bot.hf_filters import apply_hf_filters, run_hf_evaluation
from bot.models import TradeCandidate
from bot.strategy import score_candidate


def settings(tmp_path: Path) -> Settings:
    return Settings(
        root=tmp_path,
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


def candidate(symbol: str = "MSFT", urls: list[str] | None = None, text: str = "") -> TradeCandidate:
    return TradeCandidate(
        symbol=symbol,
        thesis=f"{symbol} has durable demand, cash flow, and a defined owner-quality thesis. {text}",
        catalyst="Earnings, sector rotation, and product demand provide a defined paper-trade catalyst.",
        quality_case="The business has recurring demand, balance-sheet support, and margin of safety.",
        momentum_case="Shares show relative strength versus peers with volume confirmation.",
        bear_case="Valuation can compress if growth expectations weaken or macro risk rises.",
        confidence=0.76,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=8,
        source_urls=urls or ["https://investor.microsoft.com", "https://www.sec.gov"],
    )


def test_hf_source_hype_filter_vetoes_listicle_or_social_only_candidates(tmp_path):
    weak = candidate(
        "HYPE",
        urls=["https://reddit.com/r/stocks/comments/hype", "https://example.com/top-stocks"],
        text="This setup is moon rocket viral social hype with no official filing support.",
    )

    enriched, report = apply_hf_filters(settings(tmp_path), [weak], memory_bundle="", research_context={})
    result = score_candidate(enriched[0])

    assert report.veto_count == 1
    assert enriched[0].hf_filter_vetoes
    assert not result.approved
    assert any("HF veto" in reason for reason in result.rejects)


def test_hf_sentiment_adjusts_confidence_but_cannot_approve_alone(tmp_path):
    thin = TradeCandidate(
        symbol="BULL",
        thesis="Strong demand upside beats raised guidance.",
        catalyst="Strong demand upside beats raised guidance.",
        quality_case="Too thin.",
        momentum_case="Too thin.",
        bear_case="Too thin.",
        confidence=0.50,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=8,
        source_urls=["https://investor.example.com"],
    )

    enriched, _ = apply_hf_filters(settings(tmp_path), [thin], memory_bundle="", research_context={})
    result = score_candidate(enriched[0])

    assert enriched[0].hf_sentiment_label == "positive"
    assert not result.approved
    assert any("thin" in reason for reason in result.rejects)


def test_hf_rerank_prefers_official_and_reputable_sources(tmp_path):
    official = candidate("MSFT", urls=["https://investor.microsoft.com", "https://www.sec.gov"])
    weak = candidate("WEAK", urls=["https://reddit.com/r/stocks", "https://example.com/best-stocks"])

    enriched, _ = apply_hf_filters(settings(tmp_path), [official, weak], memory_bundle="", research_context={})

    assert enriched[0].hf_evidence_rank > enriched[1].hf_evidence_rank
    assert enriched[0].hf_source_quality_score > enriched[1].hf_source_quality_score


def test_hf_memory_similarity_flags_prior_rejected_trade_patterns(tmp_path):
    rejected = candidate("REJT")
    memory = (
        "Rejected REJT because "
        + rejected.thesis
        + " "
        + rejected.catalyst
        + " "
        + rejected.quality_case
        + " "
        + rejected.momentum_case
    )

    enriched, _ = apply_hf_filters(settings(tmp_path), [rejected], memory_bundle=memory, research_context={})
    result = score_candidate(enriched[0])

    assert enriched[0].hf_memory_similarity >= 0.85
    assert not result.approved
    assert any("memory" in reason.lower() for reason in result.rejects)


def test_hf_eval_mentions_all_dataset_calibration_tasks(tmp_path):
    report = run_hf_evaluation(settings(tmp_path))

    for dataset in [
        "takala/financial_phrasebank",
        "zeroshot/twitter-financial-news-sentiment",
        "PatronusAI/financebench",
        "embedding-benchmark/FinanceBench",
        "mteb/FinanceBenchRetrieval",
        "FinGPT/fingpt-sentiment-train",
        "AdaptLLM/finance-tasks",
    ]:
        assert dataset in report
    assert "No trades are placed" in report
