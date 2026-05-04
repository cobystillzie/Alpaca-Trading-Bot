from datetime import datetime, timedelta

from bot.models import TradeCandidate
from bot.self_learning import (
    build_self_learning_policy,
    enrich_candidates_with_self_learning,
    evaluate_self_learning_finalize,
    format_self_learning_disclosure,
    recent_diversity_bucket_counts,
    recent_symbol_counts,
)


def candidate(symbol: str = "NVDA", *, catalyst: str = "Strong setup.") -> TradeCandidate:
    return TradeCandidate(
        symbol=symbol,
        thesis=f"{symbol} has a clear business thesis with durable demand and quality.",
        catalyst=catalyst,
        quality_case="The business quality case is documented with balance-sheet and demand evidence.",
        momentum_case="Relative strength and trend confirmation support a defined paper setup.",
        bear_case="Valuation or market weakness can invalidate the setup quickly.",
        confidence=0.76,
        horizon_days=5,
        target_allocation_percent=8,
        stop_loss_percent=8,
        source_urls=["https://example.com/company", "https://www.sec.gov"],
        recommendation="execute-if-guards-pass",
    )


def test_recent_symbol_counts_uses_latest_48_hours(tmp_path):
    memory = tmp_path / "memory"
    memory.mkdir()
    now = datetime(2026, 5, 4, 12, 0, 0)
    recent = (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    old = (now - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S")
    (memory / "WATCHLIST.md").write_text(
        "\n".join(
            [
                "# Watchlist",
                f"## Latest Candidates - {old} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| NVDA | Semiconductors |",
                f"## Latest Candidates - {recent} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| NVDA | Semiconductors |",
                "| GOOGL | Internet |",
                f"## Latest Candidates - {recent} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| NVDA | Semiconductors |",
            ]
        ),
        encoding="utf-8",
    )

    assert recent_symbol_counts(tmp_path, now=now) == {"NVDA": 2, "GOOGL": 1}


def test_recent_diversity_bucket_counts_uses_watchlist_sectors(tmp_path):
    memory = tmp_path / "memory"
    memory.mkdir()
    now = datetime(2026, 5, 4, 12, 0, 0)
    recent = (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    old = (now - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S")
    (memory / "WATCHLIST.md").write_text(
        "\n".join(
            [
                "# Watchlist",
                f"## Latest Candidates - {old} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| NVDA | Semiconductors |",
                f"## Latest Candidates - {recent} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| NVDA | Semiconductors |",
                "| GOOGL | Internet Services |",
                "| SPMO | Broad Equity Momentum ETF |",
            ]
        ),
        encoding="utf-8",
    )

    assert recent_diversity_bucket_counts(tmp_path, now=now) == {
        "semiconductors-ai": 1,
        "mega-cap-internet-cloud": 1,
        "broad-market-etf": 1,
    }


def test_enrich_marks_stale_repeat_without_fresh_catalyst(tmp_path):
    memory = tmp_path / "memory"
    memory.mkdir()
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sections = []
    for _ in range(3):
        sections.extend(
            [
                f"## Latest Candidates - {stamp} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| NVDA | Semiconductors |",
            ]
        )
    (memory / "WATCHLIST.md").write_text("\n".join(sections), encoding="utf-8")

    enriched = enrich_candidates_with_self_learning(tmp_path, [candidate("NVDA")])[0]

    assert enriched.repeat_count_48h == 3
    assert not enriched.fresh_catalyst
    assert enriched.research_tier == "stale-watch"
    assert enriched.diversity_bucket == "semiconductors-ai"


def test_enrich_keeps_fresh_repeat_eligible(tmp_path):
    memory = tmp_path / "memory"
    memory.mkdir()
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    (memory / "WATCHLIST.md").write_text(
        "\n".join(
            [
                f"## Latest Candidates - {stamp} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| NVDA | Semiconductors |",
                f"## Latest Candidates - {stamp} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| NVDA | Semiconductors |",
                f"## Latest Candidates - {stamp} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| NVDA | Semiconductors |",
            ]
        ),
        encoding="utf-8",
    )

    enriched = enrich_candidates_with_self_learning(
        tmp_path,
        [candidate("NVDA", catalyst="Fresh earnings guidance raised today after close.")],
    )[0]

    assert enriched.repeat_count_48h == 3
    assert enriched.fresh_catalyst
    assert enriched.research_tier == "execution-ready"
    assert enriched.catalyst_type == "earnings"


def test_enrich_adds_note_for_overused_diversity_bucket(tmp_path):
    memory = tmp_path / "memory"
    memory.mkdir()
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    (memory / "WATCHLIST.md").write_text(
        "\n".join(
            [
                f"## Latest Candidates - {stamp} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| NVDA | Semiconductors |",
                "| ASML | Semiconductors |",
                "| LRCX | Semiconductors |",
            ]
        ),
        encoding="utf-8",
    )

    enriched = enrich_candidates_with_self_learning(
        tmp_path,
        [candidate("AMD", catalyst="Fresh earnings guidance raised today after close.")],
    )[0]

    assert enriched.diversity_bucket == "semiconductors-ai"
    assert "over-concentrated in semiconductors-ai" in enriched.allocation_learning_note


def test_build_self_learning_policy_mentions_repeats_and_diversity(tmp_path):
    memory = tmp_path / "memory"
    memory.mkdir()
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    (memory / "WATCHLIST.md").write_text(
        "\n".join(
            [
                f"## Latest Candidates - {stamp} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| GOOGL | Internet |",
                f"## Latest Candidates - {stamp} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| GOOGL | Internet |",
                f"## Latest Candidates - {stamp} EDT",
                "| Symbol | Sector |",
                "|---|---|",
                "| GOOGL | Internet |",
            ]
        ),
        encoding="utf-8",
    )

    policy = build_self_learning_policy(tmp_path, "Weekly review says diversify.", [candidate("GOOGL")])

    assert "GOOGL x3" in policy
    assert "mega-cap-internet-cloud" in policy
    assert "Overused recent diversity buckets" in policy
    assert "Weekly review says diversify." in policy


def test_self_learning_finalize_refuses_failed_tests():
    decision = evaluate_self_learning_finalize(
        changed_files=["src/bot/strategy.py"],
        tests_passed=False,
        telegram_sent=True,
        diff_text="",
    )

    assert not decision.approved
    assert "Tests did not pass." in decision.reasons


def test_self_learning_finalize_refuses_missing_telegram_disclosure():
    decision = evaluate_self_learning_finalize(
        changed_files=["src/bot/strategy.py"],
        tests_passed=True,
        telegram_sent=False,
        diff_text="",
    )

    assert not decision.approved
    assert "Telegram disclosure was not sent." in decision.reasons


def test_self_learning_finalize_refuses_live_trading_diff():
    decision = evaluate_self_learning_finalize(
        changed_files=["src/bot/config.py"],
        tests_passed=True,
        telegram_sent=True,
        diff_text="+LIVE_TRADING_ENABLED=true",
    )

    assert not decision.approved
    assert any("live-trading" in reason for reason in decision.reasons)


def test_self_learning_finalize_allows_guardrail_text_about_live_trades():
    decision = evaluate_self_learning_finalize(
        changed_files=["AGENTS.md"],
        tests_passed=True,
        telegram_sent=True,
        diff_text="+- Do not submit live securities trades.",
    )

    assert decision.approved


def test_self_learning_finalize_refuses_secrets_file():
    decision = evaluate_self_learning_finalize(
        changed_files=[".env.local"],
        tests_passed=True,
        telegram_sent=True,
        diff_text="",
    )

    assert not decision.approved
    assert any(".env.local" in reason for reason in decision.reasons)


def test_telegram_disclosure_lists_exact_changed_files():
    disclosure = format_self_learning_disclosure(
        changed_files=["src/bot/strategy.py", "routines/friday-weekly-review.md"],
        behavior_changes=["Penalize stale repeated tickers."],
        test_summary="pytest=0, compileall=0",
        safety_summary="passed",
    )

    assert "src/bot/strategy.py" in disclosure
    assert "routines/friday-weekly-review.md" in disclosure
    assert "Penalize stale repeated tickers." in disclosure
    assert "pytest=0, compileall=0" in disclosure


def test_weekly_routine_no_longer_says_proposal_only():
    body = (
        __import__("pathlib")
        .Path("routines/friday-weekly-review.md")
        .read_text(encoding="utf-8")
    )

    assert "Do not rewrite executable trading code" not in body
    assert "may edit code" in body
    assert "run-self-learning-finalize.ps1" in body
