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
