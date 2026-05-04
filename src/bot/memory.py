from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re

from .models import TradeCandidate


MEMORY_TEMPLATES: dict[str, str] = {
    "TRADING-STRATEGY.md": "# Trading Strategy\n\nQuality + catalyst + momentum barbell. Paper trading only.\n",
    "CHITTICK-CASH.md": (
        "# Chittick Cash\n\n"
        "30% weighted paper-trading filter. Long-only concentrated-quality mindset with margin of safety, "
        "growth runway, valuation discipline, balance-sheet risk review, and an owner-style 30-180 day thesis. "
        "Seed watchlist: GOOGL, INTC, USAR, GT. Seed names are research priorities only, never automatic buys.\n"
    ),
    "RESEARCH-LOG.md": "# Research Log\n\n",
    "TRADE-LOG.md": "# Trade Log\n\n",
    "PORTFOLIO-SNAPSHOT.md": "# Portfolio Snapshot\n\n",
    "MARKET-REGIME.md": "# Market Regime\n\n",
    "SOURCE-QUALITY.md": "# Source Quality And Signals\n\nSocial buzz and congressional disclosures are low-weight context only.\n\n",
    "HUGGINGFACE-FILTERS.md": (
        "# Hugging Face Filters\n\n"
        "HF models run after Perplexity research and before final scoring. They can downgrade or veto "
        "source-thin, hype-only, or prior-rejected patterns, but they cannot bypass Alpaca guardrails.\n\n"
    ),
    "SELF-LEARNING-POLICY.md": (
        "# Self-Learning Policy\n\n"
        "Weekly review writes active instructions here for the next week. Research, premarket, midday, "
        "close, and weekly routines must read this before acting.\n\n"
        "Default: balanced diversity, penalize stale repeated tickers without fresh catalysts, and never "
        "loosen paper-only or banned-instrument guardrails.\n"
    ),
    "TELEGRAM-SUMMARIES.md": "# Telegram Summaries\n\n",
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
            lambda _: replacement,
            body,
            flags=re.S,
        )
    else:
        body = body.rstrip() + "\n\n" + replacement + "\n"
    table = "\n\n## Latest Candidates - " + now_stamp() + "\n\n"
    if candidates:
        table += "| Symbol | Sector | Tier | Bucket | Repeat | Fresh | Confidence | Chittick | HF Source | HF Vetoes | Allocation | Stop | Recommendation | Catalyst |\n"
        table += "|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|\n"
        for candidate in candidates:
            table += (
                f"| {candidate.symbol} | {candidate.sector.replace('|', '/')[:80]} | "
                f"{candidate.research_tier.replace('|', '/')[:40]} | "
                f"{candidate.diversity_bucket.replace('|', '/')[:50]} | "
                f"{candidate.repeat_count_48h} | "
                f"{'yes' if candidate.fresh_catalyst else 'no'} | "
                f"{candidate.confidence:.2f} | "
                f"{candidate.chittick_cash_score:.0f} | "
                f"{candidate.hf_source_quality_score:.0f} | "
                f"{len(candidate.hf_filter_vetoes)} | "
                f"{candidate.target_allocation_percent:.1f}% | "
                f"{candidate.stop_loss_percent:.1f}% | "
                f"{candidate.recommendation.replace('|', '/')[:120]} | "
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
