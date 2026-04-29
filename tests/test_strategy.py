from bot.models import TradeCandidate
from bot.strategy import extract_candidates, score_candidate


def test_extract_candidates_from_json():
    text = """
    {
      "summary": "Market constructive.",
      "candidates": [
        {
          "symbol": "MSFT",
          "thesis": "Microsoft has durable enterprise demand and resilient cloud economics.",
          "catalyst": "Cloud demand and AI infrastructure spending remain visible this week.",
          "quality_case": "The business has high recurring revenue, strong balance sheet, and durable margins.",
          "momentum_case": "Shares are above trend with relative strength versus broad software peers.",
          "bear_case": "Valuation can compress if AI spending expectations weaken.",
          "confidence": 0.74,
          "horizon_days": 5,
          "target_allocation_percent": 8,
          "stop_loss_percent": 8,
          "source_urls": ["https://example.com"]
        }
      ]
    }
    """
    summary, candidates = extract_candidates(text)
    assert "constructive" in summary
    assert len(candidates) == 1
    assert candidates[0].symbol == "MSFT"


def test_score_rejects_options_language():
    candidate = TradeCandidate(
        symbol="NVDA",
        thesis="Buy call options because the chart looks exciting and fast.",
        catalyst="Short dated options can move quickly after news.",
        quality_case="Nvidia has a strong business and data center demand.",
        momentum_case="Trend has been strong with relative strength.",
        bear_case="It can fail if valuation compresses quickly.",
        confidence=0.8,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=8,
        source_urls=["https://example.com"],
    )
    result = score_candidate(candidate)
    assert not result.approved
    assert any("banned" in reason for reason in result.rejects)


def test_score_allows_margin_of_safety_language():
    candidate = TradeCandidate(
        symbol="SPY",
        thesis="SPY gives broad diversified exposure for a short paper swing trade.",
        catalyst="Market breadth and index liquidity support a defined paper setup this week.",
        quality_case="Broad diversification and margin of safety reduce single-company blowup risk.",
        momentum_case="Trend and liquidity remain constructive versus other index ETFs.",
        bear_case="Broad market weakness can quickly invalidate the thesis.",
        confidence=0.78,
        horizon_days=5,
        target_allocation_percent=10,
        stop_loss_percent=5,
        source_urls=["https://example.com"],
    )
    result = score_candidate(candidate)
    assert result.approved


def test_score_rejects_buying_on_margin_language():
    candidate = TradeCandidate(
        symbol="SPY",
        thesis="SPY gives broad diversified exposure for a short paper swing trade.",
        catalyst="Market breadth and index liquidity support a defined paper setup this week.",
        quality_case="The setup only works by buying on margin with leverage.",
        momentum_case="Trend and liquidity remain constructive versus other index ETFs.",
        bear_case="Broad market weakness can quickly invalidate the thesis.",
        confidence=0.78,
        horizon_days=5,
        target_allocation_percent=10,
        stop_loss_percent=5,
        source_urls=["https://example.com"],
    )
    result = score_candidate(candidate)
    assert not result.approved
    assert any("banned" in reason for reason in result.rejects)
