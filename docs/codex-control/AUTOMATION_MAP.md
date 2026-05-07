# Alpaca Automation Map

This is a portable repo mirror of the live Codex Alpaca automations. It is not
the live scheduler config. The live configs are under
`C:\Users\cobys\.codex\automations\`.

All listed Alpaca automations currently run against:

```text
C:\Users\cobys\projects\alpaca-trading-bot
```

## Active Automations

| Automation ID | Name | Schedule | Model | Script | Purpose |
|---|---|---|---|---|---|
| `alpaca-research-agent` | Alpaca Research Agent | Weekdays every 2 hours | `gpt-5.5` | `.\scripts\run-research.ps1` | Maximum-depth research for market regime, quality/momentum candidates, social buzz, congressional disclosures, source quality, SEC/company risks, and HF post-research filters. No orders. |
| `alpaca-premarket-plan` | Alpaca Premarket Plan | Weekdays at 8:15 AM | `gpt-5.5` | `.\scripts\run-premarket.ps1` | Builds the day candidate plan, Chittick/HF readouts, source-quality notes, low-weight social/congress notes, and risk plan. No orders. |
| `alpaca-market-open-execution` | Alpaca Market Open Execution | Weekdays at 9:45 AM | `gpt-5.5` | `.\scripts\run-market-open.ps1` | May place Alpaca paper orders only when all strategy, HF, self-learning, and guardrail checks pass. No live trading. |
| `alpaca-midday-risk-scan` | Alpaca Midday Risk Scan | Weekdays at 12:30 PM | `gpt-5.5` | `.\scripts\run-midday.ps1` | Reviews portfolio state, open positions, cash reserve, concentration, thesis drift, performance ledger, source quality, social/congress noise, stop plans, and self-learning issues. |
| `alpaca-end-of-day-summary` | Alpaca End Of Day Summary | Weekdays at 4:20 PM | `gpt-5.5` | `.\scripts\run-close.ps1` | Updates portfolio snapshot, performance ledger, trade observations, source-quality notes, social/congress signal review, and Telegram recap. |
| `alpaca-friday-weekly-review` | Alpaca Friday Weekly Review | Fridays at 5:15 PM | `gpt-5.5` | `.\scripts\run-weekly-review.ps1` plus `.\scripts\run-self-learning-finalize.ps1` | Reviews what went wrong, updates self-learning policy, may edit code/prompts/docs through the Friday exception, then tests, compiles, discloses to Telegram, commits, and pushes only if gates pass. |

## Routine Files

- Research: `routines/agents/research-agent.md`, `routines/premarket-research.md`
- Execution: `routines/market-open-execution.md`, `routines/agents/execution-agent.md`
- Risk: `routines/midday-risk-scan.md`, `routines/agents/risk-agent.md`
- Close: `routines/end-of-day-summary.md`
- Weekly learning: `routines/friday-weekly-review.md`
- Agent support cards: `routines/agents/*.md`

## Memory Files The Automations Should Read

- `memory/TRADING-STRATEGY.md`
- `memory/CHITTICK-CASH.md`
- `memory/SELF-LEARNING-POLICY.md`
- `memory/WATCHLIST.md`
- `memory/REJECTED-TRADES.md`
- `memory/LESSONS-LEARNED.md`
- `memory/STRATEGY-PROPOSALS.md`
- `memory/HUGGINGFACE-FILTERS.md`
- `memory/SOURCE-QUALITY.md`
- `memory/MARKET-REGIME.md`
- `memory/PERFORMANCE-LEDGER.md`
- `memory/TELEGRAM-SUMMARIES.md`

## Safety Rules By Automation

- Research and premarket routines must not place orders.
- Market-open execution may place paper orders only through `run-market-open.ps1`.
- Midday and close routines are review/reporting only.
- Performance ledger output is observation-only; it must not place orders or change sizing by itself.
- Friday self-learning is the only routine allowed to edit executable code.
- Friday self-learning must run tests and compile checks before finalizing.
- Friday self-learning must disclose exact changed files to Telegram before commit/push.
- No automation may enable live trading, options, crypto, margin, short selling, or secrets.

## Updating This Map

When live Codex app automations change, update this file as a portable mirror.
Do not treat this file as the live scheduler. Use the Codex automation tools or
the app automation UI for the actual recurring jobs.
