from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timedelta
import os

from .alpaca import AlpacaClient
from .config import Settings, load_settings
from .git_scribe import commit_and_push_memory
from .guardrails import evaluate_candidate_for_order
from .hf_filters import apply_hf_filters, format_hf_report, run_hf_evaluation
from .huggingface import setup_report, try_download_registry
from .memory import (
    append_section,
    ensure_memory_files,
    load_latest_candidates,
    read_memory_bundle,
    today_trade_count,
    update_watchlist,
)
from .perplexity import run_sonar_research
from .self_learning import (
    build_self_learning_policy,
    enrich_candidates_with_self_learning,
    finalize_self_learning_update,
)
from .strategy import (
    congressional_prompt,
    extract_candidates,
    market_regime_prompt,
    research_prompt,
    score_candidate,
    sec_quality_prompt,
    social_buzz_prompt,
)
from .telegram import format_analyst_memo, format_research_update, send_message


SOCIAL_BUZZ_DOMAINS = ["reddit.com", "stocktwits.com", "x.com", "finance.yahoo.com"]
CONGRESSIONAL_DOMAINS = [
    "capitoltrades.com",
    "disclosures-clerk.house.gov",
    "efdsearch.senate.gov",
    "quiverquant.com",
    "unusualwhales.com",
]


def _settings() -> Settings:
    settings = load_settings()
    ensure_memory_files(settings.root)
    return settings


@contextmanager
def _daily_runtime_lock(root, name: str, stale_minutes: int = 90):
    runtime_dir = root / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    lock_path = runtime_dir / f"{name}-{datetime.now().strftime('%Y-%m-%d')}.lock"
    acquired = False
    try:
        if lock_path.exists():
            updated_at = datetime.fromtimestamp(lock_path.stat().st_mtime)
            if datetime.now() - updated_at < timedelta(minutes=stale_minutes):
                yield False
                return
            lock_path.unlink(missing_ok=True)

        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        acquired = True
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(datetime.now().isoformat())
        yield True
    except FileExistsError:
        yield False
    finally:
        if acquired:
            lock_path.unlink(missing_ok=True)


def setup_check() -> int:
    settings = _settings()
    issues = settings.setup_issues()
    if issues:
        print("Setup issues:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    try:
        account = AlpacaClient(settings).account()
        print(f"Alpaca paper account OK. Portfolio value: {account.get('portfolio_value', 'unknown')}")
    except Exception as exc:  # noqa: BLE001 - setup check should show user-facing failures.
        print(f"Alpaca check failed: {exc}")
        return 1
    try:
        response = run_sonar_research(
            settings,
            'Return this exact JSON: {"summary":"setup check ok","candidates":[]}',
        )
        print("Perplexity check OK." if "setup check" in response.lower() else "Perplexity responded.")
    except Exception as exc:  # noqa: BLE001
        print(f"Perplexity check failed: {exc}")
        return 1
    try:
        sent = send_message(settings, "Alpaca trading bot setup-check passed.")
        print("Telegram check OK." if sent else "Telegram skipped.")
    except Exception as exc:  # noqa: BLE001
        print(f"Telegram check failed: {exc}")
        return 1
    print("Setup looks complete.")
    print("Alpaca mode: paper")
    print("Perplexity key: present")
    print("Telegram: present")
    print("Live trading: disabled")
    print(f"Hugging Face filters: {'enabled' if settings.hf_research_enabled else 'disabled'}")
    return 0


def run_hf_setup(*, download: bool = False, include_large: bool = False) -> int:
    settings = _settings()
    print(setup_report(settings))
    if download:
        print("")
        print("Caching Hugging Face registry artifacts...")
        for line in try_download_registry(settings, include_large=include_large):
            print(line)
    return 0


def run_hf_eval() -> int:
    settings = _settings()
    report = run_hf_evaluation(settings)
    append_section(settings.root / "memory" / "HUGGINGFACE-FILTERS.md", "HF Eval", report)
    print(report)
    print(commit_and_push_memory(settings, "hf eval"))
    return 0


def _research_passes(settings: Settings, memory_bundle: str) -> dict[str, str]:
    context: dict[str, str] = {}
    context["market_regime"] = run_sonar_research(
        settings,
        market_regime_prompt(memory_bundle),
        system_content="Return valid JSON. Analyze market regime for a cautious paper-trading workflow.",
    )
    context["social_buzz"] = run_sonar_research(
        settings,
        social_buzz_prompt(memory_bundle),
        system_content="Return valid JSON. Social buzz is weak context only, never a trade reason.",
        search_domain_filter=SOCIAL_BUZZ_DOMAINS,
    )
    context["congressional_disclosures"] = run_sonar_research(
        settings,
        congressional_prompt(memory_bundle),
        system_content="Return valid JSON. Congressional disclosures are delayed, low-weight context only.",
        search_domain_filter=CONGRESSIONAL_DOMAINS,
    )
    context["sec_quality"] = run_sonar_research(
        settings,
        sec_quality_prompt(memory_bundle),
        system_content="Return valid JSON. Use SEC/company filing evidence for risk and quality checks.",
        search_mode="sec",
    )
    return context


def run_research() -> int:
    settings = _settings()
    memory_bundle = read_memory_bundle(settings.root, max_chars=30000)
    research_context = _research_passes(settings, memory_bundle)
    prompt = research_prompt(
        memory_bundle,
        settings=settings,
        research_context=research_context,
    )
    response = run_sonar_research(settings, prompt)
    summary, candidates = extract_candidates(response)
    candidates = enrich_candidates_with_self_learning(settings.root, candidates)
    if not summary:
        summary = "Research completed, but no summary was returned."
    hf_report_text = ""
    if settings.hf_research_enabled:
        candidates, hf_report = apply_hf_filters(
            settings,
            candidates,
            memory_bundle=memory_bundle,
            research_context=research_context,
        )
        hf_report_text = format_hf_report(hf_report)
        append_section(
            settings.root / "memory" / "HUGGINGFACE-FILTERS.md",
            "Research Filter Run",
            hf_report_text,
        )
    update_watchlist(settings.root, summary, candidates)
    append_section(
        settings.root / "memory" / "MARKET-REGIME.md",
        "Market Regime Research",
        research_context.get("market_regime", ""),
    )
    append_section(
        settings.root / "memory" / "SOURCE-QUALITY.md",
        "Source And Signal Research",
        (
            "Social buzz, max 10% influence:\n"
            + research_context.get("social_buzz", "")
            + "\n\nCongressional disclosures, max 5% influence:\n"
            + research_context.get("congressional_disclosures", "")
            + "\n\nSEC/company quality check:\n"
            + research_context.get("sec_quality", "")
        ),
    )
    append_section(
        settings.root / "memory" / "RESEARCH-LOG.md",
        "Two-Hour Research Agent",
        f"{summary}\n\nCandidates found: {len(candidates)}"
        + (f"\n\n{hf_report_text}" if hf_report_text else ""),
    )
    telegram_text = format_research_update(summary, candidates)
    append_section(settings.root / "memory" / "TELEGRAM-SUMMARIES.md", "Research Update", telegram_text)
    send_message(settings, telegram_text)
    print(commit_and_push_memory(settings, "research update"))
    print(f"Research complete. Candidates: {len(candidates)}")
    return 0


def run_premarket() -> int:
    settings = _settings()
    candidates = enrich_candidates_with_self_learning(
        settings.root,
        load_latest_candidates(settings.root),
    )
    rejected: list[str] = []
    lines = ["Premarket plan built from latest watchlist.", ""]
    if not candidates:
        lines.append("No candidates available. Run research first.")
    for candidate in candidates:
        score = score_candidate(candidate)
        lines.append(
            f"- {candidate.symbol}: score={score.score}, base={score.base_score}, "
            f"chittick={score.chittick_cash_score}, approved={score.approved}, "
            f"allocation={candidate.target_allocation_percent:.1f}%, stop={candidate.stop_loss_percent:.1f}%"
        )
        if score.rejects:
            lines.append(f"  rejects: {'; '.join(score.rejects)}")
            rejected.append(f"{candidate.symbol}: {'; '.join(score.rejects)}")
    append_section(
        settings.root / "memory" / "RESEARCH-LOG.md",
        "Premarket Plan",
        "\n".join(lines),
    )
    summary = candidates[0].market_regime if candidates else "No current market regime from watchlist."
    memo = format_analyst_memo(
        "Premarket Analyst Memo",
        summary=summary or "Premarket plan built from latest research and watchlist.",
        candidates=candidates,
        action="Execute only if guardrails pass; otherwise hold cash and wait for cleaner evidence.",
        rejected=rejected,
    )
    append_section(settings.root / "memory" / "TELEGRAM-SUMMARIES.md", "Premarket Memo", memo)
    send_message(settings, memo)
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
    with _daily_runtime_lock(settings.root, "market-open") as lock_acquired:
        if not lock_acquired:
            print("Market-open execution is already running; skipped duplicate launch.")
            return 0
        return _run_market_open_impl(settings)


def _run_market_open_impl(settings: Settings) -> int:
    client = _alpaca_or_log(settings, "Market Open Execution")
    if client is None:
        print(commit_and_push_memory(settings, "market open setup rejection"))
        return 0

    candidates = sorted(
        enrich_candidates_with_self_learning(
            settings.root,
            load_latest_candidates(settings.root),
        ),
        key=lambda candidate: score_candidate(candidate).score,
        reverse=True,
    )
    if not candidates:
        append_section(
            settings.root / "memory" / "REJECTED-TRADES.md",
            "Market Open Execution",
            "No candidates available. No order was placed.",
        )
        send_message(
            settings,
            format_analyst_memo(
                "Market Open Execution Memo",
                summary="No candidates available. No order was placed.",
                action="Skip execution and preserve cash.",
            ),
        )
        print(commit_and_push_memory(settings, "market open no candidates"))
        return 0

    account = client.account()
    positions = client.positions()
    trade_count = today_trade_count(settings.root)
    if trade_count > 0:
        append_section(
            settings.root / "memory" / "REJECTED-TRADES.md",
            "Market Open Execution Skipped",
            "A market-open order is already logged for today. No backup order was placed.",
        )
        send_message(settings, "Market-open execution skipped because an order is already logged for today.")
        print(commit_and_push_memory(settings, "market open duplicate skip"))
        print("Market-open already handled today.")
        return 0

    rejected: list[str] = []
    for candidate in candidates:
        result = evaluate_candidate_for_order(
            candidate,
            account,
            positions,
            today_order_count=trade_count,
            managed_capital_usd=settings.managed_capital_usd,
        )
        if not result.approved:
            append_section(
                settings.root / "memory" / "REJECTED-TRADES.md",
                f"Rejected {candidate.symbol}",
                "\n".join(result.reasons),
            )
            rejected.append(f"{candidate.symbol}: {'; '.join(result.reasons)}")
            continue

        asset = client.asset(candidate.symbol)
        if not asset.get("tradable", False) or asset.get("class") not in {"us_equity", "us_equity_fractionable"}:
            append_section(
                settings.root / "memory" / "REJECTED-TRADES.md",
                f"Rejected {candidate.symbol}",
                "Alpaca asset is not tradable as a supported stock/ETF.",
            )
            rejected.append(f"{candidate.symbol}: Alpaca asset is not tradable as a supported stock/ETF.")
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
            format_analyst_memo(
                "Market Open Execution Memo",
                summary=candidate.market_regime or "Market-open order placed after guardrail approval.",
                candidates=[candidate],
                portfolio=_portfolio_body(account, positions),
                action=f"Paper order placed: {candidate.symbol}, notional ${result.order_notional:.2f}, order {order.get('id', 'unknown')}.",
                rejected=rejected,
            ),
        )
        print(commit_and_push_memory(settings, f"paper order {candidate.symbol}"))
        print(f"Paper order placed for {candidate.symbol}.")
        return 0

    send_message(
        settings,
        format_analyst_memo(
            "Market Open Execution Memo",
            summary="Market-open execution found no approved paper trades.",
            candidates=candidates,
            portfolio=_portfolio_body(account, positions),
            action="Skip execution; preserve cash until evidence and guardrails improve.",
            rejected=rejected,
        ),
    )
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
    candidates = enrich_candidates_with_self_learning(settings.root, load_latest_candidates(settings.root))
    memo = format_analyst_memo(
        "Midday Risk Memo",
        summary="Review current paper positions, thesis drift, concentration, stop discipline, and cash reserve.",
        candidates=candidates,
        portfolio=body,
        action="Hold only positions whose thesis still matches the research; do not add unless guardrails pass.",
    )
    append_section(settings.root / "memory" / "TELEGRAM-SUMMARIES.md", "Midday Memo", memo)
    send_message(settings, memo)
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
    candidates = enrich_candidates_with_self_learning(settings.root, load_latest_candidates(settings.root))
    memo = format_analyst_memo(
        "End Of Day Analyst Memo",
        summary="End-of-day review of paper portfolio, trade quality, risk notes, and next-day watchlist.",
        candidates=candidates,
        portfolio=body,
        action="Carry forward only evidence-backed candidates; review stops before the next market-open run.",
    )
    append_section(settings.root / "memory" / "TELEGRAM-SUMMARIES.md", "End Of Day Memo", memo)
    send_message(settings, memo)
    print(commit_and_push_memory(settings, "end of day summary"))
    print("Close complete.")
    return 0


def run_weekly_review() -> int:
    settings = _settings()
    memory_bundle = read_memory_bundle(settings.root, max_chars=30000)
    prompt = (
        "Review this paper-trading bot memory. Produce concise lessons, rejected-patterns, "
        "strategy proposals, self-learning directives, and any safe code/prompt/routine changes "
        "that should be made after test gates. Focus on stale repeated tickers, allocation-blocked "
        "candidates, overused sectors, weak diversity, and repetitive daily research output. "
        "Evaluate whether Chittick Cash, Hugging Face filters, social buzz, and congressional "
        "signals improved research quality or added noise. Do not propose enabling options, "
        "margin, shorting, crypto, live trading, secrets, or credential changes.\n\n"
        + memory_bundle
    )
    review = run_sonar_research(settings, prompt)
    latest_candidates = enrich_candidates_with_self_learning(
        settings.root,
        load_latest_candidates(settings.root),
    )
    append_section(settings.root / "memory" / "LESSONS-LEARNED.md", "Weekly Review", review)
    append_section(
        settings.root / "memory" / "STRATEGY-PROPOSALS.md",
        "Weekly Strategy Proposals",
        review,
    )
    policy = build_self_learning_policy(settings.root, review, latest_candidates)
    (settings.root / "memory" / "SELF-LEARNING-POLICY.md").write_text(policy + "\n", encoding="utf-8")
    memo = format_analyst_memo(
        "Weekly Strategy Review Memo",
        summary=review,
        candidates=latest_candidates,
        action="Self-learning policy updated. Friday automation may apply safe code/prompt edits only after tests pass and Telegram disclosure succeeds.",
    )
    append_section(settings.root / "memory" / "TELEGRAM-SUMMARIES.md", "Weekly Memo", memo)
    send_message(settings, memo)
    print(commit_and_push_memory(settings, "weekly strategy review"))
    print("Weekly review complete.")
    return 0


def run_self_learning_finalize() -> int:
    settings = _settings()
    return finalize_self_learning_update(settings)


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
