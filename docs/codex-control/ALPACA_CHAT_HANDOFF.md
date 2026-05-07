# Alpaca Chat Handoff

This file transfers the useful context from the long mixed Codex chat into the
Alpaca trading bot repo. Use it when starting a new Codex chat from
`C:\Users\cobys\projects\alpaca-trading-bot`.

## Current Repo State

- Repo root: `C:\Users\cobys\projects\alpaca-trading-bot`
- GitHub remote: `https://github.com/cobystillzie/Alpaca-Trading-Bot.git`
- Verified local `HEAD` before this handoff: `02f9341ee2185c7804532e5317229a44f3f6da8d`
- Verified GitHub `origin/main` before this handoff: `02f9341ee2185c7804532e5317229a44f3f6da8d`
- Primary package layout: deterministic code in `src/bot/`, memory in `memory/`, routine cards in `routines/`, and user-safe PowerShell wrappers in `scripts/`.

## Implemented Decisions To Preserve

- This is the active Alpaca long-term paper-trading bot.
- The bot uses Perplexity Sonar Pro for maximum-depth market research.
- Telegram is the human-facing output layer and should receive analyst-style memos.
- Alpaca paper trading is the only execution target.
- Alpaca may show a larger paper account, but bot sizing is self-limited through `MANAGED_CAPITAL_USD=10000`.
- Strategy is a quality + catalyst + momentum barbell:
  - Core quality book: 50-60%.
  - Momentum/catalyst book: 25-35%.
  - Minimum cash reserve: 10-20%.
- Chittick Cash is a 30% weighted scoring lens, not a hard buy signal.
- Chittick Cash seed watchlist names are `GOOGL`, `INTC`, `USAR`, and `GT`, but they are never automatic buys.
- Social buzz is capped at 10% influence and can only support attention/volume context.
- Congressional disclosures are capped at 5% influence and can only support delayed secondary catalyst context.
- Hugging Face filters run after Perplexity and before final scoring:
  - sentiment ensemble
  - source/hype classifier
  - evidence reranker
  - memory similarity
  - dataset calibration/evaluation
- Hugging Face filters may downgrade or veto weak evidence but cannot approve trades by themselves.
- Weekly self-learning may edit code, markdown, routine prompts, and automation-support files only through the Friday self-learning lane.
- Friday self-learning must test, compile, disclose exact changes to Telegram, then commit/push only if those gates pass.

## Hard Safety Boundaries

- Paper trading only.
- Do not enable live trading.
- Do not submit live securities trades.
- Do not trade options in this long-term bot.
- Do not trade crypto.
- Do not use margin.
- Do not short sell.
- Do not commit `.env.local`, API keys, tokens, secrets, account credentials, or generated secret files.
- Social buzz and congressional activity must never be the main reason for a trade.
- Hugging Face filters must never bypass Alpaca guardrails.
- Normal daily routines must not edit executable trading code.

## Active Alpaca Automations

See `docs/codex-control/AUTOMATION_MAP.md` for the portable automation mirror.
The live Codex app automation configs still live under:

```text
C:\Users\cobys\.codex\automations\
```

The Alpaca automation IDs are:

- `alpaca-research-agent`
- `alpaca-premarket-plan`
- `alpaca-market-open-execution`
- `alpaca-midday-risk-scan`
- `alpaca-end-of-day-summary`
- `alpaca-friday-weekly-review`

## Important Memory Files

- `memory/TRADING-STRATEGY.md`: portfolio shape and core strategy.
- `memory/CHITTICK-CASH.md`: Chittick Cash filter.
- `memory/SELF-LEARNING-POLICY.md`: active weekly learning directives.
- `memory/WATCHLIST.md`: latest candidates and current candidate JSON.
- `memory/REJECTED-TRADES.md`: rejected setups and reasons.
- `memory/PERFORMANCE-LEDGER.md`: observation-only performance, drawdown, rejection, source attribution, and patience-gate reporting.
- `memory/LESSONS-LEARNED.md`: weekly review output.
- `memory/STRATEGY-PROPOSALS.md`: strategy ideas and self-learning proposals.
- `memory/HUGGINGFACE-FILTERS.md`: HF filter and evaluation notes.
- `memory/TELEGRAM-SUMMARIES.md`: human-facing memo history.

## New Alpaca Folder Chat Starter Prompt

Paste this into a new Codex chat opened from the Alpaca repo folder:

```text
You are now working in C:\Users\cobys\projects\alpaca-trading-bot.

First read AGENTS.md, README.md, SETUP.md, memory/SELF-LEARNING-POLICY.md, memory/TRADING-STRATEGY.md, memory/CHITTICK-CASH.md, docs/codex-control/ALPACA_CHAT_HANDOFF.md, and docs/codex-control/AUTOMATION_MAP.md.

This repo is the active Alpaca paper-trading long-term bot. Keep all guardrails: paper trading only, no live trading, no options, no crypto, no margin, no short selling, no secrets, and do not edit .env.local.

Before proposing or changing anything, summarize current repo state, active automations, latest memory lessons, and the safest next action.
```

## Safe Next Actions

1. Open a new Codex chat from `C:\Users\cobys\projects\alpaca-trading-bot`.
2. Paste the starter prompt above.
3. Ask the new chat to summarize state before it edits anything.
4. Keep options/volatility bot and shortform-content-ops in their own future handoff packs.
