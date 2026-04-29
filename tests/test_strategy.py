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

