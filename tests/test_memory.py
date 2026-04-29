from bot.memory import load_latest_candidates, update_watchlist
from bot.models import TradeCandidate


def test_update_watchlist_handles_json_unicode_escapes(tmp_path):
    candidate = TradeCandidate(
        symbol="SPY",
        thesis="Core ETF with a margin of safety and broad exposure.",
        catalyst="Market breadth improved \u2014 risk-on tone.",
        quality_case="Diversified index exposure.",
        momentum_case="Relative strength is firm.",
        bear_case="Macro shock can reverse the setup.",
        confidence=0.81,
        horizon_days=5,
        target_allocation_percent=8.0,
        stop_loss_percent=10.0,
        source_urls=["https://example.com/research?note=unicode"],
    )

    update_watchlist(tmp_path, "Unicode test summary \U0001f4c8", [candidate])

    loaded = load_latest_candidates(tmp_path)
    assert len(loaded) == 1
    assert loaded[0].symbol == "SPY"
    assert "margin of safety" in loaded[0].thesis
