# Codex Operating Rules

This repo is a paper-trading automation system. The safety rules are part of the product.

## Hard Boundaries

- Do not submit live securities trades.
- Do not enable live trading.
- Do not commit secrets, API keys, tokens, `.env.local`, or account credentials.
- Do not auto-edit executable trading code during routine runs except the Friday weekly self-learning routine described below.
- Auto Git updates may include markdown memory/log/proposal files only, except the Friday weekly self-learning finalizer after tests and Telegram disclosure pass.

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
- Run Hugging Face filters only after Perplexity research and before final scoring.
- Hugging Face filters may downgrade or veto source-thin, hype-only, or prior-rejected patterns, but may not approve trades by themselves or bypass guardrails.

## Friday Self-Learning Exception

The Friday weekly review may edit code, markdown, routine prompts, and automation prompts when it is fixing repeated stale tickers, allocation-blocked candidates, overused sectors, weak diversity, or repetitive research behavior.

Required order:

1. Read `memory/`, including `SELF-LEARNING-POLICY.md`.
2. Run `.\scripts\run-weekly-review.ps1`.
3. Make scoped self-learning edits.
4. Run `python -m pytest` and `python -m compileall -q src`.
5. Send Telegram disclosure with exact changed files, behavior changes, and test result.
6. Commit and push only after tests and Telegram disclosure pass.

The Friday self-learning routine must still refuse live trading, secrets, options, margin, crypto, short selling, and any change that weakens paper-only guardrails.
