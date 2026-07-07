# Trading Strategy

Paper trading only.

## Portfolio Shape

- Core quality book: 50-60%.
- Momentum/catalyst book: 25-35%.
- Cash reserve: minimum 10-20%.
- Chittick Cash filter: 30% weighted lens inside candidate scoring.
- Stocks/ETFs only.
- No options, crypto, margin, short selling, or live trading in v1.

## Decision Standard

Every paper trade must explain:

- business-quality thesis
- specific catalyst
- momentum evidence
- bear case
- stop or exit plan

## Chittick Cash Lens

Chittick Cash adds a long-only concentrated-quality filter with margin of safety, growth runway, valuation discipline, balance-sheet risk review, and an owner-style 30-180 day thesis. Seed watchlist names are GOOGL, INTC, USAR, and GT, but they are research priorities only and never automatic buys.

## Policy Update - 2026-07-05

Owner decisions after the no-trades-since-May-12 diagnosis:

- Exit rules now execute automatically in the midday and close routines, before the portfolio snapshot:
  - Stop-loss: sell the full position when unrealized P&L breaches the stop documented in TRADE-LOG.md for that symbol (e.g. 6% for SPMO, 7% for NVDA), or -8% when no documented stop exists.
  - Take-profit: sell the full position when unrealized P&L reaches +25%.
  - All sells are paper-only market orders; the paper guard (assert_paper) runs before every order.
- Max open positions raised from 8 to 50. Sizing is still bounded by the 15% single-stock cap and the 10% cash reserve.
- Entry confidence gate lowered from 0.60 to 0.55.
- Banned-instrument text filter narrowed to genuine options/margin/crypto/leveraged-product/shorting context; plain research phrases like "strategic options" or "short-dated catalyst" no longer reject a stock candidate.
- Unchanged: paper trading only, stocks/ETFs only, 1-15% target allocation, 3-12% stop range, 2 new positions per day, MANAGED_CAPITAL_USD stays 10000.
