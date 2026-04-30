# Chittick Cash

Chittick Cash is a 30% weighted paper-trading filter layered on top of the existing quality + catalyst + momentum strategy.

## Strategy Intent

- Long-only stocks and ETFs only.
- Concentrated-quality mindset, but execution still obeys the 15% max single-stock cap.
- Favor high margin of safety plus real growth potential.
- Prefer businesses the bot can explain like an owner, not just chart setups.
- Use a 1-10 day paper execution review plus a 30-180 day owner thesis.

## Seed Watchlist

- GOOGL: default Alphabet exposure; treat GOOG and GOOGL as equivalent business exposure in research.
- INTC: turnaround and national-strategic semiconductor exposure.
- USAR: rare-earth supply chain and strategic materials exposure.
- GT: cyclical value and turnaround exposure.

Seed names are research priorities only. They are never automatic buys.

## Required Analysis

Every Chittick Cash review should cover:

- margin of safety versus the current valuation
- growth runway and industry tailwinds
- balance-sheet risk, debt, dilution, or cyclicality
- management and capital allocation
- why the name deserves concentration versus a broad ETF or better alternative
- owner-style hold or re-review thesis over 30-180 days
- strongest bear case and reject reason if the setup is not good enough

## Scoring Rule

The final candidate score is:

`existing_strategy_score * 0.70 + chittick_cash_score * 0.30`

Chittick Cash is a weighted filter, not a hard gate. It cannot override guardrail rejections, weak sources, banned instruments, poor risk/reward, or paper-only limits.
