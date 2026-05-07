from pathlib import Path

from bot.performance import (
    build_performance_report,
    format_performance_report,
    format_performance_summary,
    parse_rejections,
    parse_trade_log,
    source_bucket,
)


def write_memory(root: Path, filename: str, body: str) -> None:
    memory = root / "memory"
    memory.mkdir(exist_ok=True)
    (memory / filename).write_text(body, encoding="utf-8")


def sample_trade_log() -> str:
    return """# Trade Log
## ORDER: Paper Buy SPMO - 2026-04-28 23:59:30 Eastern Daylight Time

Symbol: SPMO
Notional: $800.00
Order id: order-1
Thesis: Momentum ETF thesis.
Catalyst: Breadth and momentum.
Bear case: Momentum reversal.
Stop plan: 6.0% stop/trailing review.
Warnings: none
## ORDER: Paper Buy GOOGL - 2026-04-30 09:49:21 Eastern Daylight Time

Symbol: GOOGL
Notional: $800.00
Order id: order-2
Thesis: Alphabet thesis.
Catalyst: Cloud earnings.
Bear case: Regulatory pressure.
Stop plan: 7.0% stop/trailing review.
Warnings: none
"""


def sample_snapshots() -> str:
    return """# Portfolio Snapshot
## Midday Risk Scan - 2026-04-29 12:32:25 Eastern Daylight Time

Portfolio value: 99996.45
Cash: 99200
Buying power: 199196.45

Positions:
- SPMO: qty=6.1, market_value=796.45, unrealized_pl=-3.55
## End Of Day Summary - 2026-04-30 16:30:02 Eastern Daylight Time

Portfolio value: 100045.01
Cash: 98400
Buying power: 198445.01

Positions:
- SPMO: qty=6.1, market_value=817.99, unrealized_pl=17.99
- GOOGL: qty=2.1, market_value=827.02, unrealized_pl=27.02
## End Of Day Summary - 2026-05-01 16:30:01 Eastern Daylight Time

Portfolio value: 100030.00
Cash: 98400
Buying power: 198430.00

Positions:
- SPMO: qty=6.1, market_value=810.00, unrealized_pl=10.00
- GOOGL: qty=2.1, market_value=820.00, unrealized_pl=20.00
"""


def sample_watchlist() -> str:
    return """# Watchlist

<!-- latest-candidates-json
{"summary":"latest","candidates":[{"symbol":"SPY","source_urls":["https://www.sec.gov/x","https://investor.microsoft.com/y"],"hf_filter_vetoes":["veto"]},{"symbol":"QQQ","source_urls":["https://reddit.com/r/stocks"],"hf_filter_vetoes":[]}]}
-->

## Latest Candidates - 2026-04-30 10:00:00 Eastern Daylight Time

| Symbol | Sector | Recommendation |
|---|---|---|
| SPMO | ETF | watch |
| GOOGL | Internet | execute-if-guards-pass |
## Latest Candidates - 2026-05-01 10:00:00 Eastern Daylight Time

| Symbol | Sector | Recommendation |
|---|---|---|
| SPMO | ETF | watch |
| MSFT | Software | watch |
"""


def test_parse_trade_log_extracts_notional_and_stop():
    trades = parse_trade_log(sample_trade_log())

    assert [trade.symbol for trade in trades] == ["SPMO", "GOOGL"]
    assert trades[0].notional == 800
    assert trades[1].stop_loss_percent == 7


def test_rejection_parser_counts_symbols_and_reasons():
    records = parse_rejections(
        """# Rejected Trades
## Rejected SPMO - 2026-04-29 09:47:13 Eastern Daylight Time

Single-stock allocation would exceed 15%.
## Market Open Execution Skipped - 2026-05-06 09:55:01 Eastern Daylight Time

A market-open order is already logged for today. No backup order was placed.
"""
    )

    assert len(records) == 2
    assert records[0].symbol == "SPMO"
    assert "already logged" in records[1].reason


def test_performance_report_summarizes_returns_and_patience_gate(tmp_path):
    write_memory(tmp_path, "TRADE-LOG.md", sample_trade_log())
    write_memory(tmp_path, "PORTFOLIO-SNAPSHOT.md", sample_snapshots())
    write_memory(tmp_path, "WATCHLIST.md", sample_watchlist())
    write_memory(
        tmp_path,
        "REJECTED-TRADES.md",
        """# Rejected Trades
## Rejected SPMO - 2026-04-29 09:47:13 Eastern Daylight Time

Single-stock allocation would exceed 15%.
""",
    )
    (tmp_path / ".env.local").write_text("SECRET_SHOULD_NOT_APPEAR=1", encoding="utf-8")

    report = build_performance_report(tmp_path, managed_capital_usd=10000)
    text = format_performance_report(report)
    summary = format_performance_summary(report)

    assert "Portfolio value: $100,030.00" in text
    assert "Managed-capital return: 0.30%" in text
    assert "Max snapshot drawdown: $15.01" in text
    assert "SPMO: appeared 2 times; open position P/L $10.00" in text
    assert "Data threshold not met: 2/15 trades" in text
    assert "SECRET_SHOULD_NOT_APPEAR" not in text
    assert "managed cash reserve" in summary


def test_source_bucket_classification():
    assert source_bucket("https://www.sec.gov/Archives/test") == "sec"
    assert source_bucket("https://investor.microsoft.com/news") == "official_or_sponsor"
    assert source_bucket("https://www.morningstar.com/etfs") == "reputable_financial_news"
    assert source_bucket("https://reddit.com/r/stocks") == "social"
    assert source_bucket("https://example.com/top-stocks") == "listicle_or_screen"
