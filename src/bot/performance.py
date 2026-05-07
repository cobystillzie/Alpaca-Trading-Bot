from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
import re
from urllib.parse import urlparse


ACCOUNT_BASELINE_USD = 100000.0
PATIENCE_MIN_TRADES = 15
PATIENCE_MIN_DAYS = 21


@dataclass(frozen=True)
class PaperTrade:
    symbol: str
    timestamp: datetime | None
    timestamp_text: str
    notional: float
    thesis: str = ""
    catalyst: str = ""
    bear_case: str = ""
    stop_loss_percent: float = 0.0


@dataclass(frozen=True)
class PositionSnapshot:
    symbol: str
    qty: float
    market_value: float
    unrealized_pl: float


@dataclass(frozen=True)
class PortfolioSnapshot:
    title: str
    timestamp: datetime | None
    timestamp_text: str
    portfolio_value: float
    cash: float
    buying_power: float
    positions: list[PositionSnapshot] = field(default_factory=list)


@dataclass(frozen=True)
class RejectionRecord:
    kind: str
    symbol: str
    timestamp: datetime | None
    timestamp_text: str
    reason: str


@dataclass(frozen=True)
class WatchlistSection:
    timestamp: datetime | None
    timestamp_text: str
    rows: list[dict[str, str]]


@dataclass(frozen=True)
class PerformanceReport:
    first_snapshot: PortfolioSnapshot | None
    latest_snapshot: PortfolioSnapshot | None
    snapshots: list[PortfolioSnapshot]
    trades: list[PaperTrade]
    rejections: list[RejectionRecord]
    watchlist_sections: list[WatchlistSection]
    latest_candidate_json: list[dict]
    managed_capital_usd: float
    benchmark_note: str

    @property
    def trade_count(self) -> int:
        return len(self.trades)

    @property
    def deployed_basis(self) -> float:
        return sum(trade.notional for trade in self.trades)

    @property
    def latest_position_value(self) -> float:
        if not self.latest_snapshot:
            return 0.0
        return sum(position.market_value for position in self.latest_snapshot.positions)

    @property
    def latest_unrealized_pl(self) -> float:
        if not self.latest_snapshot:
            return 0.0
        return sum(position.unrealized_pl for position in self.latest_snapshot.positions)

    @property
    def account_return_percent(self) -> float:
        if not self.latest_snapshot:
            return 0.0
        return (self.latest_snapshot.portfolio_value / ACCOUNT_BASELINE_USD - 1) * 100

    @property
    def managed_return_percent(self) -> float:
        if not self.latest_snapshot or self.managed_capital_usd <= 0:
            return 0.0
        return (self.latest_snapshot.portfolio_value - ACCOUNT_BASELINE_USD) / self.managed_capital_usd * 100

    @property
    def deployed_return_percent(self) -> float:
        if self.deployed_basis <= 0:
            return 0.0
        return self.latest_unrealized_pl / self.deployed_basis * 100

    @property
    def managed_cash_reserve_percent(self) -> float:
        if self.managed_capital_usd <= 0:
            return 0.0
        return max(0.0, (self.managed_capital_usd - self.latest_position_value) / self.managed_capital_usd * 100)


def _to_float(value: str | None) -> float:
    try:
        return float(str(value or "").replace(",", "").strip())
    except ValueError:
        return 0.0


def _parse_timestamp(text: str) -> datetime | None:
    match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", text)
    if not match:
        return None
    try:
        return datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def parse_trade_log(text: str) -> list[PaperTrade]:
    trades: list[PaperTrade] = []
    pattern = r"^## ORDER: Paper Buy ([A-Z0-9.\-]+) - (.*?)\n\n([\s\S]*?)(?=^## |\Z)"
    for match in re.finditer(pattern, text, flags=re.M):
        symbol, timestamp_text, body = match.groups()
        stop_match = re.search(r"Stop plan:\s*([0-9.]+)%", body)
        trades.append(
            PaperTrade(
                symbol=symbol.strip().upper(),
                timestamp=_parse_timestamp(timestamp_text),
                timestamp_text=timestamp_text.strip(),
                notional=_to_float(_field(body, "Notional").replace("$", "")),
                thesis=_field(body, "Thesis"),
                catalyst=_field(body, "Catalyst"),
                bear_case=_field(body, "Bear case"),
                stop_loss_percent=_to_float(stop_match.group(1) if stop_match else None),
            )
        )
    return trades


def _field(body: str, label: str) -> str:
    match = re.search(rf"^{re.escape(label)}:\s*(.*?)$", body, flags=re.M)
    return match.group(1).strip() if match else ""


def parse_portfolio_snapshots(text: str) -> list[PortfolioSnapshot]:
    snapshots: list[PortfolioSnapshot] = []
    pattern = r"^## (.+?) - (.*?)\n\n([\s\S]*?)(?=^## |\Z)"
    for match in re.finditer(pattern, text, flags=re.M):
        title, timestamp_text, body = match.groups()
        portfolio_value = _to_float(_field(body, "Portfolio value"))
        if portfolio_value <= 0:
            continue
        positions: list[PositionSnapshot] = []
        for pos in re.finditer(
            r"^- ([A-Z0-9.\-]+): qty=([^,]+), market_value=([^,]+), unrealized_pl=([^\n]+)",
            body,
            flags=re.M,
        ):
            positions.append(
                PositionSnapshot(
                    symbol=pos.group(1).upper(),
                    qty=_to_float(pos.group(2)),
                    market_value=_to_float(pos.group(3)),
                    unrealized_pl=_to_float(pos.group(4)),
                )
            )
        snapshots.append(
            PortfolioSnapshot(
                title=title.strip(),
                timestamp=_parse_timestamp(timestamp_text),
                timestamp_text=timestamp_text.strip(),
                portfolio_value=portfolio_value,
                cash=_to_float(_field(body, "Cash")),
                buying_power=_to_float(_field(body, "Buying power")),
                positions=positions,
            )
        )
    return snapshots


def parse_rejections(text: str) -> list[RejectionRecord]:
    records: list[RejectionRecord] = []
    pattern = r"^## (Rejected|Market Open Execution Skipped)\s*([A-Z0-9.\-]*)? - (.*?)\n\n([\s\S]*?)(?=^## |\Z)"
    for match in re.finditer(pattern, text, flags=re.M):
        kind, symbol, timestamp_text, body = match.groups()
        reason = " ".join(line.strip() for line in body.splitlines() if line.strip())
        records.append(
            RejectionRecord(
                kind=kind.strip(),
                symbol=(symbol or "").strip().upper(),
                timestamp=_parse_timestamp(timestamp_text),
                timestamp_text=timestamp_text.strip(),
                reason=reason or "No reason recorded.",
            )
        )
    return records


def parse_watchlist_sections(text: str) -> list[WatchlistSection]:
    sections: list[WatchlistSection] = []
    pattern = r"^## Latest Candidates - (.*?)\n\n([\s\S]*?)(?=^## Latest Candidates|\Z)"
    for match in re.finditer(pattern, text, flags=re.M):
        timestamp_text, body = match.groups()
        rows = _parse_markdown_table(body)
        sections.append(
            WatchlistSection(
                timestamp=_parse_timestamp(timestamp_text),
                timestamp_text=timestamp_text.strip(),
                rows=rows,
            )
        )
    return sections


def _parse_markdown_table(text: str) -> list[dict[str, str]]:
    headers: list[str] = []
    rows: list[dict[str, str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or line.count("|") < 2:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if all(set(cell) <= {"-", ":"} for cell in cells if cell):
            continue
        if any(cell.lower() == "symbol" for cell in cells):
            headers = [cell.lower() for cell in cells]
            continue
        if headers and len(cells) >= len(headers):
            row = dict(zip(headers, cells, strict=False))
            if row.get("symbol") and row.get("symbol") not in {"---", "Symbol"}:
                rows.append(row)
    return rows


def latest_candidate_json(watchlist_text: str) -> list[dict]:
    match = re.search(r"<!-- latest-candidates-json\s*(.*?)\s*-->", watchlist_text, flags=re.S)
    if not match:
        return []
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return []
    candidates = data.get("candidates", [])
    return candidates if isinstance(candidates, list) else []


def build_performance_report(root: Path, *, managed_capital_usd: float = 10000.0) -> PerformanceReport:
    portfolio_text = _read(root / "memory" / "PORTFOLIO-SNAPSHOT.md")
    watchlist_text = _read(root / "memory" / "WATCHLIST.md")
    snapshots = parse_portfolio_snapshots(portfolio_text)
    return PerformanceReport(
        first_snapshot=snapshots[0] if snapshots else None,
        latest_snapshot=snapshots[-1] if snapshots else None,
        snapshots=snapshots,
        trades=parse_trade_log(_read(root / "memory" / "TRADE-LOG.md")),
        rejections=parse_rejections(_read(root / "memory" / "REJECTED-TRADES.md")),
        watchlist_sections=parse_watchlist_sections(watchlist_text),
        latest_candidate_json=latest_candidate_json(watchlist_text),
        managed_capital_usd=managed_capital_usd,
        benchmark_note=(
            "Benchmark price series is not stored in repo memory yet; compare against SPY/SPMO "
            "after benchmark snapshots are added."
        ),
    )


def max_drawdown(snapshots: list[PortfolioSnapshot]) -> tuple[float, str, str]:
    peak = 0.0
    peak_time = ""
    drawdown = 0.0
    drawdown_from = ""
    drawdown_to = ""
    for snapshot in snapshots:
        if snapshot.portfolio_value > peak:
            peak = snapshot.portfolio_value
            peak_time = snapshot.timestamp_text
        current = peak - snapshot.portfolio_value
        if current > drawdown:
            drawdown = current
            drawdown_from = peak_time
            drawdown_to = snapshot.timestamp_text
    return drawdown, drawdown_from, drawdown_to


def format_performance_summary(report: PerformanceReport) -> str:
    latest = report.latest_snapshot
    if not latest:
        return "No portfolio snapshots are available yet."
    return (
        f"Performance: value ${latest.portfolio_value:,.2f}, "
        f"P/L vs $100k ${latest.portfolio_value - ACCOUNT_BASELINE_USD:,.2f}, "
        f"managed return {report.managed_return_percent:.2f}%, "
        f"deployed return {report.deployed_return_percent:.2f}%, "
        f"managed cash reserve {report.managed_cash_reserve_percent:.1f}%."
    )


def format_performance_report(report: PerformanceReport) -> str:
    latest = report.latest_snapshot
    if not latest:
        return "No portfolio snapshots are available yet."

    drawdown, drawdown_from, drawdown_to = max_drawdown(report.snapshots)
    lines = [
        "Performance Ledger",
        "",
        "Account Summary",
        f"- First snapshot: {report.first_snapshot.timestamp_text if report.first_snapshot else 'none'}",
        f"- Latest snapshot: {latest.timestamp_text}",
        f"- Portfolio value: ${latest.portfolio_value:,.2f}",
        f"- P/L vs $100k baseline: ${latest.portfolio_value - ACCOUNT_BASELINE_USD:,.2f}",
        f"- Full paper-account return: {report.account_return_percent:.3f}%",
        f"- Managed-capital return: {report.managed_return_percent:.2f}%",
        f"- Deployed basis: ${report.deployed_basis:,.2f}",
        f"- Return on deployed basis: {report.deployed_return_percent:.2f}%",
        f"- Latest position value: ${report.latest_position_value:,.2f}",
        f"- Full-account cash reserve: {latest.cash / latest.portfolio_value * 100:.1f}%",
        f"- Managed-capital cash reserve: {report.managed_cash_reserve_percent:.1f}%",
        f"- Max snapshot drawdown: ${drawdown:,.2f}"
        + (f" from {drawdown_from} to {drawdown_to}" if drawdown_from else ""),
        "",
        "Open Position Review",
    ]
    trades_by_symbol = {trade.symbol: trade for trade in report.trades}
    if not latest.positions:
        lines.append("- No open positions in the latest snapshot.")
    for position in latest.positions:
        trade = trades_by_symbol.get(position.symbol)
        status = "winner" if position.unrealized_pl > 0 else "loser" if position.unrealized_pl < 0 else "flat"
        age = _age_days(trade.timestamp, latest.timestamp) if trade else None
        stop = f"{trade.stop_loss_percent:.1f}%" if trade and trade.stop_loss_percent else "not logged"
        lines.append(
            f"- {position.symbol}: {status}, value ${position.market_value:,.2f}, "
            f"unrealized P/L ${position.unrealized_pl:,.2f}, entry {trade.timestamp_text if trade else 'unknown'}, "
            f"thesis age {age if age is not None else 'unknown'} days, stop {stop}, "
            "catalyst status open, thesis validity requires next close review, next review next reporting cycle."
        )
    lines.extend(
        [
            "",
            "Candidate Outcome Tracker",
            *_candidate_outcome_lines(report),
            "",
            "Rejection Analytics",
            *_rejection_lines(report),
            "",
            "Source Quality Attribution",
            *_source_quality_lines(report),
            "",
            "Patience Gate",
            *_patience_gate_lines(report),
            "",
            "Benchmark Context",
            f"- {report.benchmark_note}",
        ]
    )
    return "\n".join(lines)


def _age_days(start: datetime | None, end: datetime | None) -> int | None:
    if not start or not end:
        return None
    return max(0, (end.date() - start.date()).days)


def _candidate_outcome_lines(report: PerformanceReport) -> list[str]:
    latest = report.latest_snapshot
    if not report.watchlist_sections:
        return ["- No watchlist candidate history is available yet."]
    counts: dict[str, int] = {}
    for section in report.watchlist_sections:
        for row in section.rows:
            symbol = row.get("symbol", "").upper()
            if symbol:
                counts[symbol] = counts.get(symbol, 0) + 1
    position_pl = {
        position.symbol: position.unrealized_pl
        for position in latest.positions
    } if latest else {}
    lines: list[str] = []
    for symbol, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:12]:
        if symbol in position_pl:
            outcome = f"open position P/L ${position_pl[symbol]:,.2f}"
        else:
            outcome = "market outcome unavailable until benchmark/candidate price history is captured"
        lines.append(f"- {symbol}: appeared {count} times; {outcome}.")
    return lines


def _rejection_lines(report: PerformanceReport) -> list[str]:
    if not report.rejections:
        return ["- No rejections logged yet."]
    by_reason: dict[str, int] = {}
    by_symbol: dict[str, int] = {}
    for rejection in report.rejections:
        by_reason[rejection.reason] = by_reason.get(rejection.reason, 0) + 1
        if rejection.symbol:
            by_symbol[rejection.symbol] = by_symbol.get(rejection.symbol, 0) + 1
    lines = ["- By reason:"]
    lines.extend(f"  - {reason}: {count}" for reason, count in sorted(by_reason.items(), key=lambda item: (-item[1], item[0]))[:8])
    if by_symbol:
        lines.append("- By symbol:")
        lines.extend(f"  - {symbol}: {count}" for symbol, count in sorted(by_symbol.items(), key=lambda item: (-item[1], item[0]))[:8])
    return lines


def _source_quality_lines(report: PerformanceReport) -> list[str]:
    if not report.latest_candidate_json:
        return ["- Latest candidate JSON is unavailable; source attribution cannot be computed."]
    buckets: dict[str, int] = {}
    hf_vetoes = 0
    for candidate in report.latest_candidate_json:
        urls = candidate.get("source_urls", [])
        if isinstance(urls, list):
            for url in urls:
                bucket = source_bucket(str(url))
                buckets[bucket] = buckets.get(bucket, 0) + 1
        vetoes = candidate.get("hf_filter_vetoes", [])
        if isinstance(vetoes, list):
            hf_vetoes += len(vetoes)
    lines = [f"- HF vetoes on latest candidates: {hf_vetoes}"]
    if not buckets:
        lines.append("- No source URLs are stored for latest candidates.")
    else:
        lines.extend(f"- {bucket}: {count}" for bucket, count in sorted(buckets.items()))
    lines.append("- Attribution is observational only until candidate outcome history is captured.")
    return lines


def source_bucket(url: str) -> str:
    host = urlparse(url).netloc.lower()
    text = url.lower()
    if "sec.gov" in host:
        return "sec"
    if any(domain in host for domain in ("investor.", "ir.", "invesco.com", "schwabassetmanagement.com", "vanguard.com", "ishares.com")):
        return "official_or_sponsor"
    if any(domain in host for domain in ("reuters.com", "bloomberg.com", "cnbc.com", "marketwatch.com", "morningstar.com", "wsj.com", "nasdaq.com")):
        return "reputable_financial_news"
    if any(domain in host for domain in ("reddit.com", "stocktwits.com", "x.com")):
        return "social"
    if any(domain in host for domain in ("capitoltrades.com", "house.gov", "senate.gov", "quiverquant.com", "unusualwhales.com")):
        return "congressional"
    if any(term in text for term in ("best-", "top-", "listicle", "hot-stocks")):
        return "listicle_or_screen"
    return "unknown"


def _patience_gate_lines(report: PerformanceReport) -> list[str]:
    first_trade = next((trade for trade in report.trades if trade.timestamp), None)
    latest_time = report.latest_snapshot.timestamp if report.latest_snapshot else None
    days = _age_days(first_trade.timestamp, latest_time) if first_trade and latest_time else 0
    enough = report.trade_count >= PATIENCE_MIN_TRADES or days >= PATIENCE_MIN_DAYS
    if enough:
        return [
            f"- Data threshold met: {report.trade_count} trades over {days} days.",
            "- Strategy tuning may be reviewed, but safety guardrails still apply.",
        ]
    return [
        f"- Data threshold not met: {report.trade_count}/{PATIENCE_MIN_TRADES} trades and {days}/{PATIENCE_MIN_DAYS} days.",
        "- Keep strategy aggressiveness unchanged; prefer automation, logging, and review improvements.",
    ]
