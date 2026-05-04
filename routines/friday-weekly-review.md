# Friday Weekly Review Routine

Run `.\scripts\run-weekly-review.ps1`.

Produce lessons learned, strategy proposals, and active self-learning instructions in `memory/SELF-LEARNING-POLICY.md`.

Evaluate whether Chittick Cash, Hugging Face filters, social buzz, and congressional-disclosure signals helped decisions or added noise.

This routine may edit code, markdown, routine prompts, and automation prompts when the weekly evidence shows repeated stale tickers, allocation-blocked candidates, overused sectors, weak diversity, or repetitive daily research output.

Required finalization:

1. Run `python -m pytest`.
2. Run `python -m compileall -q src`.
3. Run `.\scripts\run-self-learning-finalize.ps1`.
4. Commit/push only if tests pass and Telegram disclosure succeeds.

Never enable live trading, options, margin, crypto, short selling, secrets, or `.env.local` changes.
