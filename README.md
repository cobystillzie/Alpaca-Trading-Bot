# Codex/Alpaca Paper Trading Bot

This repo is a Codex-native paper-trading system built around a quality + catalyst + momentum barbell:

- quality/business filter inspired by Buffett and Munger
- scheduled catalyst and momentum scans inspired by Nate Herk's trading-bot workflow
- portfolio-aware review inspired by Samin's advisor-style workflow
- tight feedback loops inspired by YC-style weekly iteration
- low-weight social buzz and congressional disclosure signals for context only

The first version is paper trading only. Live trading is intentionally blocked by default.
Alpaca may show a $100,000 paper account, but the bot self-limits managed capital
to $10,000 by default via `MANAGED_CAPITAL_USD`.

## Core Commands

```powershell
.\scripts\setup-check.ps1
.\scripts\run-research.ps1
.\scripts\run-premarket.ps1
.\scripts\run-market-open.ps1
.\scripts\run-midday.ps1
.\scripts\run-close.ps1
.\scripts\run-weekly-review.ps1
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
- markdown-only auto commits/pushes

Read [SETUP.md](SETUP.md) before running scheduled automations.
