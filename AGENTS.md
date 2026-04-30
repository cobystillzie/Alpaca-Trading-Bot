# Codex Operating Rules

This repo is a paper-trading automation system. The safety rules are part of the product.

## Hard Boundaries

- Do not submit live securities trades.
- Do not enable live trading.
- Do not commit secrets, API keys, tokens, `.env.local`, or account credentials.
- Do not auto-edit executable trading code during routine runs.
- Auto Git updates may include markdown memory/log/proposal files only.

## Routine Behavior

- Read `memory/` before acting.
- Run only the script associated with the routine.
- Use Alpaca paper trading only.
- Send Telegram summaries when configured.
- Log every proposed trade, rejected trade, paper order, and strategy proposal.
- Keep version-one trading limited to stocks and ETFs.
- Treat social buzz as low-weight attention context only, capped at 10% influence.
- Treat congressional disclosures as delayed, low-weight catalyst context only, capped at 5% influence.
- Never approve a trade because of social buzz or congressional activity alone.
- Prefer official/company, SEC, ETF sponsor, earnings, reputable financial news, and market data sources.
