from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re

from .models import TradeCandidate


MEMORY_TEMPLATES: dict[str, str] = {
    "TRADING-STRATEGY.md": "# Trading Strategy\n\nQuality + catalyst + momentum barbell. Paper trading only.\n",
    "RESEARCH-LOG.md": "# Research Log\n\n",
    "TRADE-LOG.md": "# Trade Log\n\n",
    "PORTFOLIO-SNAPSHOT.md": "# Portfolio Snapshot\n\n",
    "LESSONS-LEARNED.md": "# Lessons Learned\n\n",
    "STRATEGY-PROPOSALS.md": "# Strategy Proposals\n\n",
    "WATCHLIST.md": "# Watchlist\n\n<!-- latest-candidates-json\n{\"summary\":\"\",\"candidates\":[]}\n-->\n",
    "REJECTED-TRADES.md": "# Rejected Trades\n\n",
}


def now_stamp() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def ensure_memory_files(root: Path) -> None:
    memory_dir = root / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    for filename, template in MEMORY_TEMPLATES.items():
        path = memory_dir / filename
        if not path.exists():
            path.write_text(template, encoding="utf-8")


def append_section(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    section = f"\n## {title} - {now_stamp()}\n\n{body.strip()}\n"
    path.write_text(existing.rstrip() + section + "\n", encoding="utf-8")


def read_memory_bundle(root: Path, max_chars: int = 20000) -> str:
    ensure_memory_files(root)
    chunks: list[str] = []
    for filename in MEMORY_TEMPLATES:
        path = root / "memory" / filename
        chunks.append(f"\n--- {filename} ---\n{path.read_text(encoding='utf-8')}")
    bundle = "\n".join(chunks)
    return bundle[-max_chars:]


def update_watchlist(root: Path, summary: str, candidates: list[TradeCandidate]) -> None:
    ensure_memory_files(root)
    path = root / "memory" / "WATCHLIST.md"
    data = {
        "summary": summary,
        "candidates": [candidate.to_dict() for candidate in candidates],
    }
    body = path.read_text(encoding="utf-8")
    replacement = (
        "<!-- latest-candidates-json\n"
        + json.dumps(data, indent=2, sort_keys=True)
        + "\n-->"
    )
    if "<!-- latest-candidates-json" in body:
        body = re.sub(
            r"<!-- latest-candidates-json\s*.*?\s*-->",
            replacement,
            body,
            flags=re.S,
        )
    else:
        body = body.rstrip() + "\n\n" + replacement + "\n"
    table = "\n\n## Latest Candidates - " + now_stamp() + "\n\n"
    if candidates:
        table += "| Symbol | Confidence | Allocation | Stop | Catalyst |\n"
        table += "|---|---:|---:|---:|---|\n"
        for candidate in candidates:
            table += (
                f"| {candidate.symbol} | {candidate.confidence:.2f} | "
                f"{candidate.target_allocation_percent:.1f}% | "
                f"{candidate.stop_loss_percent:.1f}% | "
                f"{candidate.catalyst.replace('|', '/')[:160]} |\n"
            )
    else:
        table += "No candidates.\n"
    path.write_text(body.rstrip() + table + "\n", encoding="utf-8")


def load_latest_candidates(root: Path) -> list[TradeCandidate]:
    path = root / "memory" / "WATCHLIST.md"
    if not path.exists():
        return []
    body = path.read_text(encoding="utf-8")
    match = re.search(r"<!-- latest-candidates-json\s*(.*?)\s*-->", body, flags=re.S)
    if not match:
        return []
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return []
    candidates: list[TradeCandidate] = []
    for item in data.get("candidates", []):
        if isinstance(item, dict):
            candidate = TradeCandidate.from_dict(item)
            if candidate.symbol:
                candidates.append(candidate)
    return candidates


def today_trade_count(root: Path) -> int:
    path = root / "memory" / "TRADE-LOG.md"
    if not path.exists():
        return 0
    today = datetime.now().strftime("%Y-%m-%d")
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if today in line and "ORDER:" in line)

