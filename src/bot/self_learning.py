from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from pathlib import Path
import re
import subprocess

from .config import Settings
from .models import TradeCandidate
from .telegram import send_message


FRESH_CATALYST_TERMS = (
    "earnings",
    "guidance",
    "sec filing",
    "10-k",
    "10-q",
    "8-k",
    "contract",
    "announced",
    "upgrade",
    "breakout",
    "fda",
    "approval",
    "trial",
    "today",
    "this morning",
    "after close",
    "pre-market",
)

UNSAFE_DIFF_PATTERNS = (
    r"LIVE_TRADING_ENABLED\s*=\s*true",
    r"ALPACA_ENV\s*=\s*live",
    r"paper-api\.alpaca\.markets.*api\.alpaca\.markets",
    r"(?m)^\+(?!.*\bdo not\b).*\bsubmit\s+live\b",
    r"(?m)^\+(?!.*\bdo not\b).*\b(?:place|send|execute)\s+live securities trades?\b",
)

DISALLOWED_SELF_LEARNING_FILES = (
    ".env.local",
    ".env",
)

DISALLOWED_SELF_LEARNING_PREFIXES = (
    ".hf_cache/",
    ".pytest_cache/",
    "__pycache__/",
    "runtime/",
    "logs/",
)


@dataclass(frozen=True)
class SelfLearningFinalizeDecision:
    approved: bool
    reasons: list[str]


def _section_datetimes_and_bodies(watchlist_text: str) -> list[tuple[datetime, str]]:
    sections: list[tuple[datetime, str]] = []
    matches = list(
        re.finditer(r"^## Latest Candidates - (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*$", watchlist_text, flags=re.M)
    )
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(watchlist_text)
        try:
            stamp = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        sections.append((stamp, watchlist_text[start:end]))
    return sections


def recent_symbol_counts(root: Path, *, hours: int = 48, now: datetime | None = None) -> dict[str, int]:
    path = root / "memory" / "WATCHLIST.md"
    if not path.exists():
        return {}
    current = now or datetime.now()
    cutoff = current - timedelta(hours=hours)
    counts: dict[str, int] = {}
    for stamp, body in _section_datetimes_and_bodies(path.read_text(encoding="utf-8")):
        if stamp < cutoff:
            continue
        for symbol in re.findall(r"^\|\s*([A-Z][A-Z0-9.\-]{1,9})\s*\|", body, flags=re.M):
            if symbol in {"Symbol", "---"}:
                continue
            counts[symbol] = counts.get(symbol, 0) + 1
    return counts


def _watchlist_rows(body: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    headers: list[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or line.count("|") < 2:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells:
            continue
        if all(set(cell) <= {"-", ":"} for cell in cells if cell):
            continue
        if any(cell.lower() == "symbol" for cell in cells):
            headers = [cell.lower() for cell in cells]
            continue
        if not headers or len(cells) < len(headers):
            continue
        rows.append(dict(zip(headers, cells, strict=False)))
    return rows


def recent_diversity_bucket_counts(root: Path, *, hours: int = 48, now: datetime | None = None) -> dict[str, int]:
    path = root / "memory" / "WATCHLIST.md"
    if not path.exists():
        return {}
    current = now or datetime.now()
    cutoff = current - timedelta(hours=hours)
    counts: dict[str, int] = {}
    for stamp, body in _section_datetimes_and_bodies(path.read_text(encoding="utf-8")):
        if stamp < cutoff:
            continue
        for row in _watchlist_rows(body):
            symbol = row.get("symbol", "").upper().strip()
            if not symbol:
                continue
            bucket = classify_diversity_text(symbol, row.get("sector", ""))
            counts[bucket] = counts.get(bucket, 0) + 1
    return counts


def _candidate_text(candidate: TradeCandidate) -> str:
    return " ".join(
        [
            candidate.symbol,
            candidate.sector,
            candidate.thesis,
            candidate.catalyst,
            candidate.quality_case,
            candidate.momentum_case,
            candidate.source_quality,
            candidate.recommendation,
            candidate.adversary_case,
            candidate.allocation_learning_note,
        ]
    ).lower()


def has_fresh_catalyst(candidate: TradeCandidate) -> bool:
    if candidate.fresh_catalyst:
        return True
    return any(term in _candidate_text(candidate) for term in FRESH_CATALYST_TERMS)


def classify_catalyst_type(candidate: TradeCandidate) -> str:
    if candidate.catalyst_type:
        return candidate.catalyst_type
    text = _candidate_text(candidate)
    if any(term in text for term in ("earnings", "guidance", "revenue", "eps")):
        return "earnings"
    if any(term in text for term in ("breakout", "relative strength", "moving average", "momentum")):
        return "momentum"
    if any(term in text for term in ("sec filing", "10-k", "10-q", "8-k", "balance sheet")):
        return "filing-quality"
    if any(term in text for term in ("contract", "capex", "data center", "ai infrastructure")):
        return "structural"
    return "general"


def classify_diversity_bucket(candidate: TradeCandidate) -> str:
    if candidate.diversity_bucket:
        return candidate.diversity_bucket
    return classify_diversity_text(candidate.symbol, _candidate_text(candidate))


def classify_diversity_text(symbol: str, text: str) -> str:
    clean = f"{symbol} {text}".lower()
    if any(term in clean for term in ("semiconductor", "gpu", "chip", "nvda", "amd", "asml", "lrcx")):
        return "semiconductors-ai"
    if any(term in clean for term in ("internet", "cloud", "googl", "google", "search", "youtube")):
        return "mega-cap-internet-cloud"
    if any(term in clean for term in ("etf", "s&p", "spmo", "spy", "broad equity")):
        return "broad-market-etf"
    if any(term in clean for term in ("industrial", "power", "energy", "utility", "eaton")):
        return "industrials-power"
    if any(term in clean for term in ("health", "biotech", "pharma", "fda", "trial")):
        return "healthcare-biotech"
    if any(term in clean for term in ("financial", "bank", "insurance")):
        return "financials"
    if any(term in clean for term in ("consumer", "retail", "restaurant")):
        return "consumer"
    if any(term in clean for term in ("oil", "gas", "energy")):
        return "energy"
    return "other"


def _allocation_constraint_note(symbol: str, rejected_text: str) -> str:
    if not symbol:
        return ""
    pattern = rf"{re.escape(symbol)}[\s\S]{{0,300}}(?:allocation|ceiling|15%|concentration|cash reserve)"
    if re.search(pattern, rejected_text, flags=re.I):
        return "Prior allocation or concentration rejection: research must propose a smaller safe tranche or a different-sector alternative."
    return ""


def enrich_candidates_with_self_learning(root: Path, candidates: list[TradeCandidate]) -> list[TradeCandidate]:
    counts = recent_symbol_counts(root)
    bucket_counts = recent_diversity_bucket_counts(root)
    total_bucket_mentions = sum(bucket_counts.values())
    rejected_path = root / "memory" / "REJECTED-TRADES.md"
    rejected_text = rejected_path.read_text(encoding="utf-8") if rejected_path.exists() else ""
    enriched: list[TradeCandidate] = []
    for candidate in candidates:
        repeat_count = max(candidate.repeat_count_48h, counts.get(candidate.symbol, 0))
        fresh = has_fresh_catalyst(candidate)
        allocation_note = candidate.allocation_learning_note or _allocation_constraint_note(candidate.symbol, rejected_text)
        has_allocation_constraint = bool(allocation_note)
        diversity_bucket = classify_diversity_bucket(candidate)
        bucket_count = bucket_counts.get(diversity_bucket, 0)
        bucket_share = (bucket_count / total_bucket_mentions) if total_bucket_mentions else 0.0
        if bucket_share >= 0.60 and bucket_count >= 3:
            sector_note = (
                f"Recent research is over-concentrated in {diversity_bucket}; compare with underrepresented sectors before increasing allocation."
            )
            allocation_note = f"{allocation_note} {sector_note}".strip()
        tier = candidate.research_tier
        if not tier:
            if repeat_count >= 3 and not fresh:
                tier = "stale-watch"
            elif has_allocation_constraint:
                tier = "watch-allocation-constrained"
            elif "execute" in candidate.recommendation.lower() and candidate.confidence >= 0.70:
                tier = "execution-ready"
            else:
                tier = "watch"
        enriched.append(
            replace(
                candidate,
                catalyst_type=classify_catalyst_type(candidate),
                fresh_catalyst=fresh,
                repeat_count_48h=repeat_count,
                diversity_bucket=diversity_bucket,
                research_tier=tier,
                allocation_learning_note=allocation_note,
            )
        )
    return enriched


def build_self_learning_policy(root: Path, review: str, candidates: list[TradeCandidate]) -> str:
    counts = recent_symbol_counts(root)
    bucket_counts = recent_diversity_bucket_counts(root)
    repeated = sorted(((symbol, count) for symbol, count in counts.items() if count >= 3), key=lambda item: (-item[1], item[0]))
    buckets = sorted({classify_diversity_bucket(candidate) for candidate in candidates if candidate.symbol})
    repeated_line = ", ".join(f"{symbol} x{count}" for symbol, count in repeated[:8]) or "none"
    bucket_line = ", ".join(buckets) or "none"
    overused_buckets = [
        f"{bucket} x{count}"
        for bucket, count in sorted(bucket_counts.items(), key=lambda item: (-item[1], item[0]))
        if count >= 3
    ]
    overused_bucket_line = ", ".join(overused_buckets[:8]) or "none"
    return "\n".join(
        [
            "# Self-Learning Policy",
            "",
            "This policy is updated by the weekly review and must be read by research, premarket, midday, close, and weekly routines.",
            "",
            "## Active Directives",
            "",
            "- Use balanced diversity: penalize stale repeated tickers, but allow repeats with fresh earnings, filings, guidance, contracts, upgrades, or confirmed breakouts.",
            "- If a repeated ticker has no fresh catalyst, lower it to `stale-watch` and research at least two alternatives from underrepresented sectors.",
            "- Top candidate sets should aim for at least three diversity buckets before execution-ready language is used.",
            "- Allocation-blocked candidates must either propose a smaller safe tranche or name a different-sector alternative; do not keep repeating the same 8% target.",
            "- Do not loosen live-trading, options, crypto, margin, short-selling, cash-reserve, or secret-handling rules.",
            "",
            "## Current Weekly Findings",
            "",
            f"- Repeated symbols in recent watchlist: {repeated_line}.",
            f"- Current candidate diversity buckets: {bucket_line}.",
            f"- Overused recent diversity buckets: {overused_bucket_line}.",
            "- Weekly review must disclose any code or prompt edits through Telegram before commit/push.",
            "",
            "## Latest Review Input",
            "",
            review.strip()[:4000],
        ]
    )


def format_self_learning_disclosure(
    *,
    changed_files: list[str],
    behavior_changes: list[str],
    test_summary: str,
    safety_summary: str,
) -> str:
    lines = [
        "Weekly Self-Learning Change Disclosure",
        "",
        "Changed files:",
        *(f"- {path}" for path in changed_files[:80]),
        "",
        "Behavior changes:",
        *(f"- {change}" for change in behavior_changes[:20]),
        "",
        f"Tests: {test_summary}",
        f"Safety scan: {safety_summary}",
    ]
    return "\n".join(lines)


def evaluate_self_learning_finalize(
    *,
    changed_files: list[str],
    tests_passed: bool,
    telegram_sent: bool,
    diff_text: str,
) -> SelfLearningFinalizeDecision:
    reasons: list[str] = []
    if not changed_files:
        reasons.append("No changed files to commit.")
    if not tests_passed:
        reasons.append("Tests did not pass.")
    if not telegram_sent:
        reasons.append("Telegram disclosure was not sent.")
    for path in changed_files:
        clean = path.replace("\\", "/").lstrip()
        if clean in DISALLOWED_SELF_LEARNING_FILES or any(clean.startswith(prefix) for prefix in DISALLOWED_SELF_LEARNING_PREFIXES):
            reasons.append(f"Disallowed file in self-learning commit: {path}")
    for pattern in UNSAFE_DIFF_PATTERNS:
        if re.search(pattern, diff_text, flags=re.I):
            reasons.append("Safety scan found a live-trading or banned-risk change.")
            break
    return SelfLearningFinalizeDecision(approved=not reasons, reasons=reasons)


def _run_command(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=str(root), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def _git(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return _run_command(root, ["git", *args])


def _changed_files(root: Path) -> list[str]:
    result = _git(root, ["status", "--porcelain"])
    files: list[str] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        files.append(path)
    return files


def finalize_self_learning_update(settings: Settings) -> int:
    pytest_result = _run_command(settings.root, ["python", "-m", "pytest"])
    compile_result = _run_command(settings.root, ["python", "-m", "compileall", "-q", "src"])
    tests_passed = pytest_result.returncode == 0 and compile_result.returncode == 0
    changed_files = _changed_files(settings.root)
    diff = _git(settings.root, ["diff", "--", *changed_files] if changed_files else ["diff"]).stdout
    test_summary = (
        f"pytest={pytest_result.returncode}, compileall={compile_result.returncode}"
    )
    behavior_changes = [
        "Weekly review may update code/prompts/memory after reviewing failures.",
        "Research scoring now penalizes stale repeated candidates unless a fresh catalyst exists.",
        "Research must broaden ticker and sector discovery after repeated GOOGL/NVDA/SPMO-style loops.",
    ]
    preliminary = evaluate_self_learning_finalize(
        changed_files=changed_files,
        tests_passed=tests_passed,
        telegram_sent=True,
        diff_text=diff,
    )
    safety_summary = "passed" if preliminary.approved else "; ".join(preliminary.reasons)
    disclosure = format_self_learning_disclosure(
        changed_files=changed_files,
        behavior_changes=behavior_changes,
        test_summary=test_summary,
        safety_summary=safety_summary,
    )
    telegram_sent = send_message(settings, disclosure)
    decision = evaluate_self_learning_finalize(
        changed_files=changed_files,
        tests_passed=tests_passed,
        telegram_sent=telegram_sent,
        diff_text=diff,
    )
    if not decision.approved:
        print("Self-learning finalize refused:")
        for reason in decision.reasons:
            print(f"- {reason}")
        return 1

    add = _git(settings.root, ["add", "--", *changed_files])
    if add.returncode != 0:
        print(add.stderr.strip() or add.stdout.strip())
        return 1
    commit = _git(settings.root, ["commit", "-m", "weekly self-learning update"])
    if commit.returncode != 0:
        print(commit.stderr.strip() or commit.stdout.strip())
        return 1
    remotes = _git(settings.root, ["remote"])
    if "origin" not in remotes.stdout.split():
        print("Self-learning update committed locally; no origin remote to push.")
        return 0
    push = _git(settings.root, ["push"])
    if push.returncode != 0:
        print(push.stderr.strip() or push.stdout.strip())
        return 1
    print("Self-learning update committed and pushed.")
    return 0
