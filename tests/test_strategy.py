from bot.models import TradeCandidate
from bot.strategy import (
    extract_candidates,
    normalize_alphabet_exposure,
    research_prompt,
    score_candidate,
)


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
          "strategy_tags": ["chittick_cash"],
          "chittick_cash_score": 82,
          "margin_of_safety_case": "Valuation is supported by durable cash flows and downside protection.",
          "valuation_case": "Current valuation is reasonable versus business quality.",
          "growth_runway": "Cloud and AI demand provide a 30-180 day review runway.",
          "balance_sheet_risk": "Balance sheet risk is limited but expectations can reset.",
          "capital_allocation_case": "Management continues disciplined investment and buybacks.",
          "concentration_case": "Quality and liquidity justify focused attention over weaker peers.",
          "owner_hold_case": "Owner thesis remains valid while cloud demand and margins hold.",
          "chittick_reject_reason": "",
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
    assert candidates[0].strategy_tags == ["chittick_cash"]
    assert candidates[0].chittick_cash_score == 82
    assert "durable cash flows" in candidates[0].margin_of_safety_case


def test_research_prompt_requires_broader_discovery_and_self_learning_fields():
    prompt = research_prompt("--- SELF-LEARNING-POLICY.md ---\nBroaden discovery.")

    assert "SELF-LEARNING-POLICY.md" in prompt
    assert "Aim for at least three diversity buckets" in prompt
    assert '"fresh_catalyst"' in prompt
    assert '"repeat_count_48h"' in prompt
    assert '"research_tier"' in prompt


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


def test_score_blends_existing_strategy_with_chittick_cash_score():
    candidate = TradeCandidate(
        symbol="GOOGL",
        thesis="Alphabet has durable search, YouTube, cloud, and AI demand with owner-quality economics.",
        catalyst="Cloud results and AI product updates provide a near-term paper-trade catalyst.",
        quality_case="The business has a strong balance sheet, high margins, and durable cash flow.",
        momentum_case="Shares show relative strength versus large-cap software and internet peers.",
        bear_case="AI capex or ad-market weakness can compress valuation and invalidate the setup.",
        confidence=0.80,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=8,
        source_urls=["https://abc.xyz/investor", "https://www.sec.gov"],
        strategy_tags=["chittick_cash"],
        chittick_cash_score=80,
        margin_of_safety_case="Cash flow quality and valuation give a reasonable margin of safety.",
        valuation_case="Valuation is reasonable versus durable growth and balance sheet quality.",
        growth_runway="Search, YouTube, cloud, and AI provide a 30-180 day owner review runway.",
        balance_sheet_risk="Balance-sheet risk is low, but capex and antitrust risk need review.",
        capital_allocation_case="Management continues to invest in AI while returning capital.",
        concentration_case="This deserves attention over weaker peers because quality and liquidity are higher.",
        owner_hold_case="Owner thesis holds while cash flow, cloud growth, and AI adoption remain intact.",
    )

    result = score_candidate(candidate)

    assert result.base_score == 100
    assert result.chittick_cash_score == 80
    assert result.score == 94
    assert result.approved


def test_seed_watchlist_cannot_approve_weak_candidate_by_itself():
    candidate = TradeCandidate(
        symbol="INTC",
        thesis="Intel is on the seed watchlist.",
        catalyst="Seed watchlist attention only.",
        quality_case="Too thin.",
        momentum_case="Too thin.",
        bear_case="Too thin.",
        confidence=0.50,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=8,
        source_urls=[],
    )

    result = score_candidate(candidate)

    assert not result.approved
    assert result.score < 70
    assert any("thin" in reason for reason in result.rejects)


def test_chittick_reject_reason_caps_subscore_but_not_other_rejects():
    candidate = TradeCandidate(
        symbol="GT",
        thesis="Goodyear has a cyclical value setup with possible turnaround upside.",
        catalyst="Earnings and restructuring updates can clarify execution progress this week.",
        quality_case="The business has recognizable brands, but cyclicality and debt risk remain material.",
        momentum_case="Shares are trying to regain relative strength versus industrial peers.",
        bear_case="Debt, input costs, and weak demand can erase the value case quickly.",
        confidence=0.76,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=8,
        source_urls=["https://corporate.goodyear.com", "https://www.sec.gov"],
        chittick_cash_score=90,
        chittick_reject_reason="Debt risk is too high for Chittick Cash concentration today.",
    )

    result = score_candidate(candidate)

    assert result.chittick_cash_score == 35
    assert result.approved


def test_chittick_pass_text_does_not_cap_subscore():
    candidate = TradeCandidate(
        symbol="LLY",
        thesis="Eli Lilly has durable GLP-1 demand and large-cap pharma quality.",
        catalyst="Upcoming earnings can confirm revenue growth and manufacturing capacity progress.",
        quality_case="The business has a strong balance sheet, durable demand, and high margins.",
        momentum_case="Shares hold relative strength versus large-cap pharmaceutical peers.",
        bear_case="Pricing pressure and competition can reduce the growth premium.",
        confidence=0.76,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=6,
        source_urls=["https://investor.lilly.com", "https://www.sec.gov"],
        chittick_cash_score=86,
        chittick_reject_reason="Passes Chittick Cash discipline with durable demand.",
    )

    result = score_candidate(candidate)

    assert result.chittick_cash_score == 86
    assert result.approved


def test_normalize_alphabet_exposure_treats_goog_and_googl_as_equivalent():
    assert normalize_alphabet_exposure("GOOG") == "GOOGL"
    assert normalize_alphabet_exposure("googl") == "GOOGL"
    assert normalize_alphabet_exposure("INTC") == "INTC"


def test_repeated_candidate_without_fresh_catalyst_gets_self_learning_penalty():
    stale = TradeCandidate(
        symbol="NVDA",
        thesis="Nvidia has durable data center demand and strong AI accelerator economics.",
        catalyst="Same general AI demand narrative already reviewed repeatedly this week.",
        quality_case="The business has high margins, strong demand, and a durable competitive position.",
        momentum_case="Shares remain above trend with relative strength versus semiconductor peers.",
        bear_case="Valuation can compress if AI demand expectations reset or margins disappoint.",
        confidence=0.80,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=8,
        source_urls=["https://investor.nvidia.com", "https://www.sec.gov"],
        chittick_cash_score=80,
        repeat_count_48h=4,
        fresh_catalyst=False,
        research_tier="watch",
        diversity_bucket="semiconductors-ai",
    )
    fresh = TradeCandidate(
        **{
            **stale.to_dict(),
            "catalyst": "Fresh earnings guidance raised today after close, changing the setup.",
            "fresh_catalyst": True,
            "research_tier": "execution-ready",
        }
    )

    stale_result = score_candidate(stale)
    fresh_result = score_candidate(fresh)

    assert stale_result.score < fresh_result.score
    assert any("stale repeat penalty" in reason for reason in stale_result.reasons)
    assert any("fresh catalyst" in reason for reason in fresh_result.reasons)


def test_fresh_high_repeat_candidate_gets_repeat_decay():
    candidate = TradeCandidate(
        symbol="SCHD",
        thesis="SCHD has broad dividend quality exposure and liquid ETF structure.",
        catalyst="Fresh sector rotation confirmation supports defensive dividend demand today.",
        quality_case="ETF holdings have durable cash flows and diversified balance-sheet risk.",
        momentum_case="Shares remain resilient versus broad growth benchmarks this week.",
        bear_case="The setup can lag if high-beta technology leadership accelerates.",
        confidence=0.82,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=8,
        source_urls=["https://www.schwabassetmanagement.com", "https://www.morningstar.com"],
        chittick_cash_score=78,
        repeat_count_48h=20,
        fresh_catalyst=True,
        research_tier="watch-allocation-constrained",
        diversity_bucket="dividend-etf-defensive",
        allocation_learning_note="High repeat count 20: cap allocation language.",
    )

    result = score_candidate(candidate)

    assert result.approved
    assert any("repeat decay" in reason for reason in result.reasons)
    assert any("allocation constraint" in reason for reason in result.reasons)


def test_execution_ready_repeat_without_fresh_catalyst_is_rejected():
    candidate = TradeCandidate(
        symbol="SPMO",
        thesis="SPMO has broad momentum ETF exposure and liquidity for a short paper trade.",
        catalyst="Same broad market momentum setup that has appeared repeatedly this week.",
        quality_case="ETF exposure is diversified but does not add a new company-quality thesis.",
        momentum_case="Trend remains constructive versus broad market alternatives.",
        bear_case="A market reversal can quickly invalidate the momentum ETF setup.",
        confidence=0.78,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=8,
        source_urls=["https://www.invesco.com", "https://example.com/market-data"],
        repeat_count_48h=5,
        fresh_catalyst=False,
        research_tier="execution-ready",
        diversity_bucket="broad-market-etf",
    )

    result = score_candidate(candidate)

    assert not result.approved
    assert any("fresh catalyst" in reason for reason in result.rejects)
