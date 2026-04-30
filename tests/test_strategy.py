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
          "market_regime": "Risk-on but selective.",
          "sector": "Software",
          "entry_plan": "Buy only after guardrails pass.",
          "exit_plan": "Exit on stop or thesis break.",
          "risk_reward": "Defined downside with catalyst-backed upside.",
          "source_quality": "Official and reputable financial sources.",
          "recommendation": "Execute if guardrails pass.",
          "adversary_case": "AI expectations can reset lower.",
          "social_buzz": "Elevated discussion, low weight.",
          "congressional_signal": "No decisive disclosure signal.",
          "signal_weights": {"social_buzz": 0.05, "congressional_signal": 0.0},
          "confidence": 0.74,
          "horizon_days": 5,
          "target_allocation_percent": 8,
          "stop_loss_percent": 8,
          "source_urls": ["https://investor.microsoft.com", "https://www.sec.gov"]
        }
      ]
    }
    """
    summary, candidates = extract_candidates(text)
    assert "constructive" in summary
    assert len(candidates) == 1
    assert candidates[0].symbol == "MSFT"
    assert candidates[0].market_regime == "Risk-on but selective."
    assert candidates[0].signal_weights["social_buzz"] == 0.05


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


def test_score_rejects_social_buzz_without_stronger_sources():
    candidate = TradeCandidate(
        symbol="NVDA",
        thesis="Nvidia has a strong business but this trade is mainly driven by social buzz.",
        catalyst="Reddit and Stocktwits chatter increased around the name today.",
        quality_case="Nvidia has data center demand and a durable AI accelerator franchise.",
        momentum_case="Shares have relative strength versus semiconductor peers.",
        bear_case="Valuation can compress if AI expectations reset.",
        confidence=0.78,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=8,
        source_urls=["https://reddit.com/r/stocks"],
        social_buzz="Social chatter is the main reason for the setup.",
        signal_weights={"social_buzz": 0.10, "congressional_signal": 0.0},
    )
    result = score_candidate(candidate)
    assert not result.approved
    assert any("Low-weight social/congress" in reason for reason in result.rejects)


def test_score_rejects_congress_signal_without_stronger_sources():
    candidate = TradeCandidate(
        symbol="MSFT",
        thesis="Microsoft has durable demand but this setup is mainly a congressional disclosure copy trade.",
        catalyst="A congressional disclosure showed a delayed purchase report.",
        quality_case="The company has recurring revenue and durable margins.",
        momentum_case="Shares show relative strength versus software peers.",
        bear_case="Disclosure timing can be stale and price may already reflect the move.",
        confidence=0.76,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=8,
        source_urls=["https://capitoltrades.com"],
        congressional_signal="Delayed congressional trade disclosure is the main catalyst.",
        signal_weights={"social_buzz": 0.0, "congressional_signal": 0.05},
    )
    result = score_candidate(candidate)
    assert not result.approved
    assert any("Low-weight social/congress" in reason for reason in result.rejects)


def test_score_rejects_listicle_only_sources():
    candidate = TradeCandidate(
        symbol="ASML",
        thesis="ASML has durable EUV lithography demand and a strong semiconductor moat.",
        catalyst="Momentum screen shows clean relative strength and sector leadership.",
        quality_case="The company has a unique technology position and strong customer demand.",
        momentum_case="Shares are trending above key moving averages with sector confirmation.",
        bear_case="Export restrictions or semi cycle weakness can pressure valuation.",
        confidence=0.75,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=7,
        source_urls=["https://example.com/best-swing-trading-stocks"],
    )
    result = score_candidate(candidate)
    assert not result.approved
    assert any("weak/listicle" in reason for reason in result.rejects)
