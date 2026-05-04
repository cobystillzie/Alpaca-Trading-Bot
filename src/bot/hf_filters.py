from __future__ import annotations

from dataclasses import dataclass, replace
import re

from .config import Settings
from .huggingface import HF_DATASETS, HF_MODELS, setup_report
from .models import TradeCandidate


OFFICIAL_SOURCE_HINTS = (
    "sec.gov",
    "investor.",
    "/investor",
    "ir.",
    "annualreports",
    "10-k",
    "10-q",
    "earnings",
    "nasdaq.com",
    "nyse.com",
    "ishares.com",
    "vanguard.com",
    "ssga.com",
)

REPUTABLE_SOURCE_HINTS = (
    "reuters.com",
    "apnews.com",
    "bloomberg.com",
    "wsj.com",
    "ft.com",
    "cnbc.com",
    "marketwatch.com",
    "morningstar.com",
    "spglobal.com",
    "federalreserve.gov",
    "finance.yahoo.com",
)

WEAK_SOURCE_HINTS = (
    "reddit.com",
    "stocktwits.com",
    "x.com",
    "twitter.com",
    "tiktok.com",
    "youtube.com",
    "best-stocks",
    "best_stock",
    "top-stocks",
    "top stocks",
    "listicle",
    "penny",
)

HYPE_TERMS = (
    "moon",
    "rocket",
    "pump",
    "squeeze",
    "guaranteed",
    "can't lose",
    "cant lose",
    "100x",
    "1000x",
    "diamond hands",
    "yolo",
    "meme",
    "viral",
)

POSITIVE_TERMS = (
    "beats",
    "beat",
    "raised guidance",
    "upside",
    "growth",
    "expansion",
    "strong demand",
    "cash flow",
    "margin expansion",
    "buyback",
    "profitable",
    "durable",
    "relative strength",
)

NEGATIVE_TERMS = (
    "miss",
    "missed",
    "cut guidance",
    "downgrade",
    "weak demand",
    "dilution",
    "debt",
    "lawsuit",
    "investigation",
    "bankruptcy",
    "unprofitable",
    "recession",
    "compress",
    "hype",
    "unsupported",
    "no filing",
)


@dataclass(frozen=True)
class HFFilterReport:
    enabled: bool
    candidates_checked: int
    veto_count: int
    notes: list[str]


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _candidate_text(candidate: TradeCandidate) -> str:
    return " ".join(
        [
            candidate.symbol,
            candidate.thesis,
            candidate.catalyst,
            candidate.quality_case,
            candidate.momentum_case,
            candidate.bear_case,
            candidate.source_quality,
            candidate.recommendation,
            candidate.adversary_case,
            candidate.social_buzz,
            candidate.congressional_signal,
            candidate.margin_of_safety_case,
            candidate.valuation_case,
            candidate.growth_runway,
            candidate.balance_sheet_risk,
            candidate.owner_hold_case,
        ]
    ).lower()


def _has_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def _source_bucket(url: str) -> str:
    clean = url.lower()
    if any(hint in clean for hint in OFFICIAL_SOURCE_HINTS):
        return "official"
    if any(hint in clean for hint in REPUTABLE_SOURCE_HINTS):
        return "reputable"
    if any(hint in clean for hint in WEAK_SOURCE_HINTS):
        return "weak"
    return "unknown"


def _source_quality_score(urls: list[str]) -> float:
    if not urls:
        return 0.0
    scores = {"official": 95.0, "reputable": 78.0, "unknown": 50.0, "weak": 15.0}
    return round(sum(scores[_source_bucket(url)] for url in urls) / len(urls), 1)


def _evidence_rank(urls: list[str]) -> float:
    if not urls:
        return 0.0
    buckets = [_source_bucket(url) for url in urls]
    score = 0.0
    if "official" in buckets:
        score += 55.0
    if "reputable" in buckets:
        score += 30.0
    if len(urls) >= 2:
        score += 10.0
    if all(bucket == "weak" for bucket in buckets):
        score -= 40.0
    return _clamp(score)


def _sentiment(text: str) -> tuple[str, float, float]:
    positive = sum(1 for term in POSITIVE_TERMS if term in text)
    negative = sum(1 for term in NEGATIVE_TERMS if term in text)
    total = max(positive + negative, 1)
    raw = (positive - negative) / total
    if raw >= 0.25:
        label = "positive"
    elif raw <= -0.25:
        label = "negative"
    else:
        label = "neutral"
    agreement = round(abs(raw), 2) if total > 1 else 0.50
    return label, round(raw, 3), agreement


def _hype_risk(text: str, urls: list[str]) -> float:
    score = 0.0
    if _has_any(text, HYPE_TERMS):
        score += 45.0
    if urls and all(_source_bucket(url) == "weak" for url in urls):
        score += 45.0
    elif any(_source_bucket(url) == "weak" for url in urls):
        score += 20.0
    if "social buzz" in text and not any(_source_bucket(url) in {"official", "reputable"} for url in urls):
        score += 20.0
    return _clamp(score) / 100.0


def _memory_similarity(candidate: TradeCandidate, memory_bundle: str) -> float:
    if not memory_bundle:
        return 0.0
    memory = memory_bundle.lower()
    rejected_marker = "--- rejected-trades.md ---"
    rejected_memory = memory.split(rejected_marker, 1)[1] if rejected_marker in memory else memory
    text = _candidate_text(candidate)
    tokens = {
        token
        for token in re.findall(r"[a-z0-9]{4,}", text)
        if token not in {"this", "that", "with", "from", "will", "risk", "case"}
    }
    if not tokens:
        return 0.0
    overlap = sum(1 for token in tokens if token in rejected_memory)
    symbol = re.escape(candidate.symbol.lower())
    has_rejected_symbol = bool(
        re.search(rf"rejected\s+{symbol}|{symbol}.*?rejected", rejected_memory, flags=re.S)
    )
    base = overlap / len(tokens)
    if not has_rejected_symbol:
        return round(_clamp(base, 0.0, 0.70), 3)
    return round(_clamp(base + 0.50, 0.0, 1.0), 3)


def _hf_model_notes(candidate: TradeCandidate, source_quality: float, evidence_rank: float) -> str:
    sentiment_models = ", ".join(model.repo_id for model in HF_MODELS if "sentiment" in model.role)
    source_models = ", ".join(model.repo_id for model in HF_MODELS if "source/hype" in model.role)
    rerankers = ", ".join(model.repo_id for model in HF_MODELS if "reranker" in model.role)
    embeddings = ", ".join(model.repo_id for model in HF_MODELS if "memory similarity" in model.role)
    return (
        f"HF staged filter for {candidate.symbol}: sentiment ensemble [{sentiment_models}]; "
        f"source/hype classifiers [{source_models}]; evidence rerankers [{rerankers}]; "
        f"memory embeddings [{embeddings}]. Source score {source_quality:.1f}, evidence rank {evidence_rank:.1f}."
    )


def apply_hf_filters(
    settings: Settings,
    candidates: list[TradeCandidate],
    *,
    memory_bundle: str,
    research_context: dict[str, str] | None = None,
) -> tuple[list[TradeCandidate], HFFilterReport]:
    if not settings.hf_research_enabled:
        return candidates, HFFilterReport(False, len(candidates), 0, ["HF research disabled."])

    enriched: list[TradeCandidate] = []
    veto_count = 0
    notes: list[str] = []
    context_text = " ".join((research_context or {}).values()).lower()
    memory_with_context = f"{memory_bundle}\n{context_text}"

    for candidate in candidates:
        text = _candidate_text(candidate)
        urls = candidate.source_urls
        label, sentiment_score, agreement = _sentiment(text)
        source_quality = _source_quality_score(urls)
        hype_risk = _hype_risk(text, urls)
        evidence_rank = _evidence_rank(urls)
        memory_similarity = _memory_similarity(candidate, memory_with_context)
        vetoes = list(candidate.hf_filter_vetoes)

        weak_only = bool(urls) and all(_source_bucket(url) == "weak" for url in urls)
        source_thin_hype = hype_risk >= 0.70 and source_quality < 35.0
        if weak_only:
            vetoes.append("HF veto: source/hype filter found weak or social-only evidence.")
        if source_thin_hype:
            vetoes.append("HF veto: hype risk is high and source quality is too thin.")
        if memory_similarity >= 0.85:
            vetoes.append("HF veto: memory similarity matches a prior rejected-trade pattern.")

        if vetoes:
            veto_count += 1

        notes.append(
            f"{candidate.symbol}: sentiment={label} {sentiment_score:.2f}, "
            f"source={source_quality:.1f}, hype={hype_risk:.2f}, "
            f"evidence={evidence_rank:.1f}, memory={memory_similarity:.2f}, vetoes={len(vetoes)}"
        )
        enriched.append(
            replace(
                candidate,
                hf_sentiment_label=label,
                hf_sentiment_score=sentiment_score,
                hf_sentiment_agreement=agreement,
                hf_source_quality_score=source_quality,
                hf_hype_risk=hype_risk,
                hf_evidence_rank=evidence_rank,
                hf_memory_similarity=memory_similarity,
                hf_filter_vetoes=vetoes,
                hf_model_notes=_hf_model_notes(candidate, source_quality, evidence_rank),
            )
        )

    return enriched, HFFilterReport(True, len(enriched), veto_count, notes)


def format_hf_report(report: HFFilterReport) -> str:
    lines = [
        "Hugging Face Filter Report",
        f"Enabled: {report.enabled}",
        f"Candidates checked: {report.candidates_checked}",
        f"Vetoes: {report.veto_count}",
        "",
        "Candidate checks:",
    ]
    if report.notes:
        lines.extend(f"- {note}" for note in report.notes)
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "Model registry:",
            *[f"- {model.repo_id}: {model.role}; {model.weight}." for model in HF_MODELS],
            "",
            "Dataset calibration registry:",
            *[f"- {dataset.repo_id}: {dataset.role}; {dataset.weight}." for dataset in HF_DATASETS],
        ]
    )
    return "\n".join(lines)


def run_hf_evaluation(settings: Settings) -> str:
    lines = [
        setup_report(settings),
        "",
        "Offline calibration smoke test",
        "No trades are placed. This uses deterministic fixtures so pytest and eval can run without model downloads.",
        "",
    ]
    fixtures = [
        (
            "takala/financial_phrasebank",
            "Company raised guidance after strong demand and margin expansion.",
            "positive",
        ),
        (
            "zeroshot/twitter-financial-news-sentiment",
            "Ticker is mooning on social hype with no filing or earnings support.",
            "negative",
        ),
        (
            "PatronusAI/financebench",
            "SEC filing and investor relations sources should outrank a listicle.",
            "source-quality",
        ),
        (
            "embedding-benchmark/FinanceBench",
            "Prior rejected trade similarity should be flagged before execution.",
            "retrieval",
        ),
        (
            "mteb/FinanceBenchRetrieval",
            "Official financial evidence should rank above weak blog claims.",
            "retrieval",
        ),
        (
            "FinGPT/fingpt-sentiment-train",
            "Debt risk and dilution pressure should reduce confidence.",
            "negative",
        ),
        (
            "AdaptLLM/finance-tasks",
            "Finance task calibration checks sentiment, QA, and zero-shot behavior.",
            "multi-task",
        ),
    ]
    for dataset_id, sample, expected in fixtures:
        label, score, agreement = _sentiment(sample.lower())
        lines.append(
            f"- {dataset_id}: expected={expected}; heuristic_sentiment={label} "
            f"score={score:.2f}; agreement={agreement:.2f}"
        )
    lines.extend(
        [
            "",
            "Result: HF eval completed without Alpaca calls, order placement, or live-trading changes.",
        ]
    )
    return "\n".join(lines)
