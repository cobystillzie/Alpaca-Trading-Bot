from __future__ import annotations

from .alpaca import AlpacaClient
from .config import Settings, load_settings
from .git_scribe import commit_and_push_memory
from .guardrails import evaluate_candidate_for_order
from .memory import (
    append_section,
    ensure_memory_files,
    load_latest_candidates,
    read_memory_bundle,
    today_trade_count,
    update_watchlist,
)
from .perplexity import run_sonar_research
from .strategy import extract_candidates, research_prompt, score_candidate
from .telegram import send_message


def _settings() -> Settings:
    settings = load_settings()
    ensure_memory_files(settings.root)
    return settings


def setup_check() -> int:
    settings = _settings()
    issues = settings.setup_issues()
    if issues:
        print("Setup issues:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Setup looks complete.")
    print("Alpaca mode: paper")
    print("Perplexity key: present")
    print("Telegram: present")
    print("Live trading: disabled")
    return 0


def run_research() -> int:
    settings = _settings()
    prompt = research_prompt(read_memory_bundle(settings.root))
    response = run_sonar_research(settings, prompt)
    summary, candidates = extract_candidates(response)
    if not summary:
        summary = "Research completed, but no summary was returned."
    update_watchlist(settings.root, summary, candidates)
    append_section(
        settings.root / "memory" / "RESEARCH-LOG.md",
        "Two-Hour Research Agent",
        f"{summary}\n\nCandidates found: {len(candidates)}",
    )
    send_message(
        settings,
        f"Research agent complete.\nCandidates: {len(candidates)}\n{summary[:1200]}",
    )
    print(commit_and_push_memory(settings, "research update"))
    print(f"Research complete. Candidates: {len(candidates)}")
    return 0


def run_premarket() -> int:
    settings = _settings()
    candidates = load_latest_candidates(settings.root)
    lines = ["Premarket plan built from latest watchlist.", ""]
    if not candidates:
        lines.append("No candidates available. Run research first.")
    for candidate in candidates:
        score = score_candidate(candidate)
        lines.append(
            f"- {candidate.symbol}: score={score.score}, approved={score.approved}, "
            f"allocation={candidate.target_allocation_percent:.1f}%, stop={candidate.stop_loss_percent:.1f}%"
        )
        if score.rejects:
            lines.append(f"  rejects: {'; '.join(score.rejects)}")
    append_section(
        settings.root / "memory" / "RESEARCH-LOG.md",
        "Premarket Plan",
        "\n".join(lines),
    )
    send_message(settings, "Premarket plan complete.\n" + "\n".join(lines[:10]))
    print(commit_and_push_memory(settings, "premarket plan"))
    print("Premarket complete.")
    return 0


def _alpaca_or_log(settings: Settings, title: str) -> AlpacaClient | None:
    if not settings.alpaca_configured or not settings.is_paper:
        append_section(
            settings.root / "memory" / "REJECTED-TRADES.md",
            title,
            "Alpaca is not configured for safe paper trading. No order was placed.",
        )
        send_message(settings, f"{title}: Alpaca paper trading is not configured. No order placed.")
        return None
    return AlpacaClient(settings)


def run_market_open() -> int:
    settings = _settings()
    client = _alpaca_or_log(settings, "Market Open Execution")
    if client is None:
        print(commit_and_push_memory(settings, "market open setup rejection"))
        return 0

    candidates = sorted(
        load_latest_candidates(settings.root),
        key=lambda candidate: score_candidate(candidate).score,
        reverse=True,
    )
    if not candidates:
        append_section(
            settings.root / "memory" / "REJECTED-TRADES.md",
            "Market Open Execution",
            "No candidates available. No order was placed.",
        )
        print(commit_and_push_memory(settings, "market open no candidates"))
        return 0

    account = client.account()
    positions = client.positions()
    trade_count = today_trade_count(settings.root)

    for candidate in candidates:
        result = evaluate_candidate_for_order(
            candidate,
            account,
            positions,
            today_order_count=trade_count,
        )
        if not result.approved:
            append_section(
                settings.root / "memory" / "REJECTED-TRADES.md",
                f"Rejected {candidate.symbol}",
                "\n".join(result.reasons),
            )
            continue

        asset = client.asset(candidate.symbol)
        if not asset.get("tradable", False) or asset.get("class") not in {"us_equity", "us_equity_fractionable"}:
            append_section(
                settings.root / "memory" / "REJECTED-TRADES.md",
                f"Rejected {candidate.symbol}",
                "Alpaca asset is not tradable as a supported stock/ETF.",
            )
            continue

        order = client.place_market_notional_order(candidate.symbol, result.order_notional)
        append_section(
            settings.root / "memory" / "TRADE-LOG.md",
            f"ORDER: Paper Buy {candidate.symbol}",
            (
                f"Symbol: {candidate.symbol}\n"
                f"Notional: ${result.order_notional:.2f}\n"
                f"Order id: {order.get('id', 'unknown')}\n"
                f"Thesis: {candidate.thesis}\n"
                f"Catalyst: {candidate.catalyst}\n"
                f"Bear case: {candidate.bear_case}\n"
                f"Stop plan: {candidate.stop_loss_percent:.1f}% stop/trailing review.\n"
                f"Warnings: {'; '.join(result.warnings) if result.warnings else 'none'}"
            ),
        )
        send_message(
            settings,
            f"Paper order placed: {candidate.symbol}\nNotional: ${result.order_notional:.2f}\nOrder: {order.get('id', 'unknown')}",
        )
        print(commit_and_push_memory(settings, f"paper order {candidate.symbol}"))
        print(f"Paper order placed for {candidate.symbol}.")
        return 0

    send_message(settings, "Market-open execution found no approved paper trades.")
    print(commit_and_push_memory(settings, "market open rejections"))
    print("No approved trades.")
    return 0


def run_midday() -> int:
    settings = _settings()
    client = _alpaca_or_log(settings, "Midday Risk Scan")
    if client is None:
        print(commit_and_push_memory(settings, "midday setup issue"))
        return 0
    account = client.account()
    positions = client.positions()
    body = _portfolio_body(account, positions)
    append_section(settings.root / "memory" / "PORTFOLIO-SNAPSHOT.md", "Midday Risk Scan", body)
    send_message(settings, "Midday risk scan complete.\n" + body[:1200])
    print(commit_and_push_memory(settings, "midday risk scan"))
    print("Midday complete.")
    return 0


def run_close() -> int:
    settings = _settings()
    client = _alpaca_or_log(settings, "End Of Day Summary")
    if client is None:
        print(commit_and_push_memory(settings, "close setup issue"))
        return 0
    account = client.account()
    positions = client.positions()
    body = _portfolio_body(account, positions)
    append_section(settings.root / "memory" / "PORTFOLIO-SNAPSHOT.md", "End Of Day Summary", body)
    send_message(settings, "End-of-day summary complete.\n" + body[:1200])
    print(commit_and_push_memory(settings, "end of day summary"))
    print("Close complete.")
    return 0


def run_weekly_review() -> int:
    settings = _settings()
    memory_bundle = read_memory_bundle(settings.root, max_chars=30000)
    prompt = (
        "Review this paper-trading bot memory. Produce concise lessons, rejected-patterns, "
        "strategy proposals, and guardrail changes. Do not propose enabling options, margin, "
        "shorting, crypto, or live trading.\n\n"
        + memory_bundle
    )
    review = run_sonar_research(settings, prompt)
    append_section(settings.root / "memory" / "LESSONS-LEARNED.md", "Weekly Review", review)
    append_section(
        settings.root / "memory" / "STRATEGY-PROPOSALS.md",
        "Weekly Strategy Proposals",
        review,
    )
    send_message(settings, "Weekly review complete.\n" + review[:1200])
    print(commit_and_push_memory(settings, "weekly strategy review"))
    print("Weekly review complete.")
    return 0


def _portfolio_body(account: dict, positions: list[dict]) -> str:
    lines = [
        f"Portfolio value: {account.get('portfolio_value', 'unknown')}",
        f"Cash: {account.get('cash', 'unknown')}",
        f"Buying power: {account.get('buying_power', 'unknown')}",
        "",
        "Positions:",
    ]
    if not positions:
        lines.append("- none")
    for pos in positions:
        lines.append(
            f"- {pos.get('symbol')}: qty={pos.get('qty')}, market_value={pos.get('market_value')}, unrealized_pl={pos.get('unrealized_pl')}"
        )
    return "\n".join(lines)

