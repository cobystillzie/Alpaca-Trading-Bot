from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import os
from pathlib import Path

from .config import Settings


@dataclass(frozen=True)
class HFArtifact:
    repo_id: str
    kind: str
    role: str
    task: str
    weight: str


HF_MODELS: tuple[HFArtifact, ...] = (
    HFArtifact(
        "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis",
        "model",
        "sentiment ensemble",
        "financial-news sentiment",
        "score-only",
    ),
    HFArtifact("ProsusAI/finbert", "model", "sentiment ensemble", "financial sentiment", "score-only"),
    HFArtifact("yiyanghkust/finbert-tone", "model", "sentiment ensemble", "financial tone", "score-only"),
    HFArtifact(
        "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
        "model",
        "sentiment fallback",
        "generic sentiment",
        "score-only",
    ),
    HFArtifact(
        "MoritzLaurer/deberta-v3-large-zeroshot-v2.0",
        "model",
        "source/hype classifier",
        "zero-shot source classification",
        "score-plus-veto",
    ),
    HFArtifact(
        "facebook/bart-large-mnli",
        "model",
        "source/hype classifier fallback",
        "zero-shot source classification",
        "score-plus-veto",
    ),
    HFArtifact(
        "cross-encoder/ms-marco-MiniLM-L6-v2",
        "model",
        "evidence reranker",
        "cross-encoder relevance",
        "score-only",
    ),
    HFArtifact(
        "BAAI/bge-reranker-base",
        "model",
        "evidence reranker",
        "reranking",
        "score-only",
    ),
    HFArtifact(
        "mixedbread-ai/mxbai-rerank-base-v1",
        "model",
        "evidence reranker",
        "reranking",
        "score-only",
    ),
    HFArtifact(
        "Qwen/Qwen3-Reranker-0.6B",
        "model",
        "evidence reranker",
        "reranking",
        "score-only",
    ),
    HFArtifact(
        "sentence-transformers/all-MiniLM-L6-v2",
        "model",
        "memory similarity",
        "embedding similarity",
        "score-only",
    ),
    HFArtifact(
        "BAAI/bge-small-en-v1.5",
        "model",
        "memory similarity",
        "embedding similarity",
        "score-only",
    ),
    HFArtifact(
        "Qwen/Qwen3-Embedding-0.6B",
        "model",
        "memory similarity",
        "embedding similarity",
        "score-only",
    ),
)

HF_DATASETS: tuple[HFArtifact, ...] = (
    HFArtifact("takala/financial_phrasebank", "dataset", "sentiment calibration", "finance sentiment", "eval-only"),
    HFArtifact(
        "zeroshot/twitter-financial-news-sentiment",
        "dataset",
        "social sentiment calibration",
        "finance social sentiment",
        "eval-only",
    ),
    HFArtifact("PatronusAI/financebench", "dataset", "source/evidence QA calibration", "financial QA", "eval-only"),
    HFArtifact(
        "embedding-benchmark/FinanceBench",
        "dataset",
        "embedding calibration",
        "finance retrieval",
        "eval-only",
    ),
    HFArtifact("mteb/FinanceBenchRetrieval", "dataset", "retrieval calibration", "finance retrieval", "eval-only"),
    HFArtifact("FinGPT/fingpt-sentiment-train", "dataset", "sentiment calibration", "finance sentiment", "eval-only"),
    HFArtifact("AdaptLLM/finance-tasks", "dataset", "finance task calibration", "finance NLP tasks", "eval-only"),
)


def hf_cache_path(settings: Settings) -> Path:
    cache = Path(settings.hf_cache_dir)
    if not cache.is_absolute():
        cache = settings.root / cache
    return cache


def configure_hf_environment(settings: Settings) -> Path:
    cache = hf_cache_path(settings)
    cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HF_HOME", str(cache))
    os.environ.setdefault("HF_HUB_CACHE", str(cache / "hub"))
    if settings.hf_token:
        os.environ.setdefault("HF_TOKEN", settings.hf_token)
    return cache


def dependency_status() -> dict[str, bool]:
    return {
        "transformers": importlib.util.find_spec("transformers") is not None,
        "datasets": importlib.util.find_spec("datasets") is not None,
        "sentence_transformers": importlib.util.find_spec("sentence_transformers") is not None,
        "huggingface_hub": importlib.util.find_spec("huggingface_hub") is not None,
        "torch": importlib.util.find_spec("torch") is not None,
    }


def registry_lines() -> list[str]:
    lines = ["Models:"]
    for artifact in HF_MODELS:
        lines.append(f"- {artifact.repo_id}: {artifact.role}; {artifact.weight}.")
    lines.append("")
    lines.append("Datasets:")
    for artifact in HF_DATASETS:
        lines.append(f"- {artifact.repo_id}: {artifact.role}; {artifact.weight}.")
    return lines


def setup_report(settings: Settings) -> str:
    cache = configure_hf_environment(settings)
    deps = dependency_status()
    lines = [
        "Hugging Face setup report",
        f"Enabled in research: {settings.hf_research_enabled}",
        f"Mode: {settings.hf_mode}",
        f"Cache: {cache}",
        f"API fallback: {settings.hf_allow_api_fallback}",
        "",
        "Python packages:",
    ]
    for name, available in deps.items():
        lines.append(f"- {name}: {'available' if available else 'missing'}")
    lines.extend(["", *registry_lines()])
    lines.extend(
        [
            "",
            "Notes:",
            "- Public local downloads do not require HF_TOKEN.",
            "- HF_TOKEN is only needed later for private/gated repos, HF API fallback, or HF Jobs.",
            "- The trading workflow can run offline tests without downloading model weights.",
        ]
    )
    return "\n".join(lines)


def try_download_registry(settings: Settings, *, include_large: bool = False) -> list[str]:
    configure_hf_environment(settings)
    results: list[str] = []
    if importlib.util.find_spec("huggingface_hub") is None:
        return ["huggingface_hub is missing. Run scripts/setup-huggingface.ps1 first."]
    from huggingface_hub import snapshot_download  # type: ignore

    allow_patterns = None if include_large else ["config.json", "tokenizer*", "*.md", "*.json"]
    for artifact in HF_MODELS:
        try:
            snapshot_download(
                artifact.repo_id,
                cache_dir=str(hf_cache_path(settings)),
                allow_patterns=allow_patterns,
            )
            suffix = "full snapshot" if include_large else "metadata/tokenizer snapshot"
            results.append(f"{artifact.repo_id}: cached {suffix}.")
        except Exception as exc:  # noqa: BLE001 - setup should report per-artifact failures.
            results.append(f"{artifact.repo_id}: cache failed: {exc}")
    return results
