# Codex/Alpaca Paper Trading Bot

This repo is a Codex-native paper-trading system built around a quality + catalyst + momentum barbell:

- quality/business filter inspired by Buffett and Munger
- scheduled catalyst and momentum scans inspired by Nate Herk's trading-bot workflow
- portfolio-aware review inspired by Samin's advisor-style workflow
- tight feedback loops inspired by YC-style weekly iteration
- low-weight social buzz and congressional disclosure signals for context only
- Hugging Face post-research filters for sentiment, source/hype risk, evidence ranking, and memory similarity

The first version is paper trading only. Live trading is intentionally blocked by default.
Alpaca may show a $100,000 paper account, but the bot self-limits managed capital
to $10,000 by default via `MANAGED_CAPITAL_USD`.

## Core Commands

```powershell
.\scripts\setup-check.ps1
.\scripts\run-research.ps1
.\scripts\run-premarket.ps1
.\scripts\run-hf-eval.ps1
.\scripts\run-market-open.ps1
.\scripts\run-midday.ps1
.\scripts\run-close.ps1
.\scripts\run-performance-report.ps1
.\scripts\run-weekly-review.ps1
.\scripts\run-self-learning-finalize.ps1
```

## Safety Boundary

The code refuses live trading unless code is deliberately changed later. Version one supports:

- Alpaca paper trading only
- stocks and ETFs only
- no options
- no crypto
- no margin
- no short selling
- social buzz cannot exceed 10% influence
- congressional disclosure signals cannot exceed 5% influence
- neither social nor congressional signals can approve trades by themselves
- Hugging Face filters may downgrade or veto weak evidence, but cannot bypass guardrails
- normal routines use markdown-only auto commits/pushes
- Friday self-learning can commit code/prompt changes only after tests pass and Telegram disclosure succeeds
- performance reporting is observation-only and must not increase strategy aggressiveness by itself

Read [SETUP.md](SETUP.md) before running scheduled automations.
