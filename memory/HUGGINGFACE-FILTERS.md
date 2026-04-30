# Hugging Face Filters

HF models run after Perplexity research and before final scoring. They can downgrade or veto source-thin, hype-only, or prior-rejected patterns, but they cannot bypass Alpaca guardrails.

## Workflow

1. Perplexity gathers live market research, catalysts, SEC/company context, social buzz, and congressional notes.
2. Hugging Face sentiment models score tone and agreement.
3. Hugging Face zero-shot models classify source quality and hype risk.
4. Hugging Face rerankers prioritize official/company, SEC, and reputable evidence.
5. Hugging Face embedding models compare candidates to prior winners, rejected trades, watchlist entries, and Chittick Cash notes.
6. Dataset calibration checks model behavior without acting as live market data.

## Safety Rules

- HF can downgrade or veto, never approve alone.
- HF cannot bypass Alpaca paper-only guardrails.
- Social buzz remains capped at 10% influence.
- Congressional disclosures remain capped at 5% influence.
- Dataset outputs are calibration/evaluation only, not live trade signals.

## Eval Baseline

- `python -m bot.cli hf-eval` runs offline deterministic calibration fixtures.
- The eval script does not call Alpaca, place orders, or enable live trading.
- Public Hugging Face downloads do not require a token.
- `HF_TOKEN` is only needed later for private/gated repos, HF API fallback, or HF Jobs.
## HF Eval - 2026-04-30 16:56:17 Eastern Daylight Time

Hugging Face setup report
Enabled in research: False
Mode: hybrid
Cache: C:\Users\cobys\projects\alpaca-trading-bot\.hf_cache
API fallback: False

Python packages:
- transformers: available
- datasets: available
- sentence_transformers: available
- huggingface_hub: available
- torch: available

Models:
- mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis: sentiment ensemble; score-only.
- ProsusAI/finbert: sentiment ensemble; score-only.
- yiyanghkust/finbert-tone: sentiment ensemble; score-only.
- distilbert/distilbert-base-uncased-finetuned-sst-2-english: sentiment fallback; score-only.
- MoritzLaurer/deberta-v3-large-zeroshot-v2.0: source/hype classifier; score-plus-veto.
- facebook/bart-large-mnli: source/hype classifier fallback; score-plus-veto.
- cross-encoder/ms-marco-MiniLM-L6-v2: evidence reranker; score-only.
- BAAI/bge-reranker-base: evidence reranker; score-only.
- mixedbread-ai/mxbai-rerank-base-v1: evidence reranker; score-only.
- Qwen/Qwen3-Reranker-0.6B: evidence reranker; score-only.
- sentence-transformers/all-MiniLM-L6-v2: memory similarity; score-only.
- BAAI/bge-small-en-v1.5: memory similarity; score-only.
- Qwen/Qwen3-Embedding-0.6B: memory similarity; score-only.

Datasets:
- takala/financial_phrasebank: sentiment calibration; eval-only.
- zeroshot/twitter-financial-news-sentiment: social sentiment calibration; eval-only.
- PatronusAI/financebench: source/evidence QA calibration; eval-only.
- embedding-benchmark/FinanceBench: embedding calibration; eval-only.
- mteb/FinanceBenchRetrieval: retrieval calibration; eval-only.
- FinGPT/fingpt-sentiment-train: sentiment calibration; eval-only.
- AdaptLLM/finance-tasks: finance task calibration; eval-only.

Notes:
- Public local downloads do not require HF_TOKEN.
- HF_TOKEN is only needed later for private/gated repos, HF API fallback, or HF Jobs.
- The trading workflow can run offline tests without downloading model weights.

Offline calibration smoke test
No trades are placed. This uses deterministic fixtures so pytest and eval can run without model downloads.

- takala/financial_phrasebank: expected=positive; heuristic_sentiment=positive score=1.00; agreement=1.00
- zeroshot/twitter-financial-news-sentiment: expected=negative; heuristic_sentiment=negative score=-1.00; agreement=1.00
- PatronusAI/financebench: expected=source-quality; heuristic_sentiment=neutral score=0.00; agreement=0.50
- embedding-benchmark/FinanceBench: expected=retrieval; heuristic_sentiment=neutral score=0.00; agreement=0.50
- mteb/FinanceBenchRetrieval: expected=retrieval; heuristic_sentiment=neutral score=0.00; agreement=0.50
- FinGPT/fingpt-sentiment-train: expected=negative; heuristic_sentiment=negative score=-1.00; agreement=1.00
- AdaptLLM/finance-tasks: expected=multi-task; heuristic_sentiment=neutral score=0.00; agreement=0.50

Result: HF eval completed without Alpaca calls, order placement, or live-trading changes.

