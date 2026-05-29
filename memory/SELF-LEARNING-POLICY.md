# Self-Learning Policy

This policy is updated by the weekly review and must be read by research, premarket, midday, close, and weekly routines.

## Active Directives

- Use balanced diversity: penalize stale repeated tickers, but allow repeats with fresh earnings, filings, guidance, contracts, upgrades, or confirmed breakouts.
- If a repeated ticker has no fresh catalyst, lower it to `stale-watch` and research at least two alternatives from underrepresented sectors.
- Top candidate sets should aim for at least three diversity buckets before execution-ready language is used.
- Allocation-blocked candidates must either propose a smaller safe tranche or name a different-sector alternative; do not keep repeating the same 8% target.
- Recently rejected hard-ban, low-weight-only, allocation-blocked, or max-position-blocked ideas must stay in `monitor-only` or `allocation-muted` lanes with zero allocation until the blocker is resolved.
- Do not loosen live-trading, options, crypto, margin, short-selling, cash-reserve, or secret-handling rules.

## Current Weekly Findings

- Repeated symbols in recent watchlist: APGE x3, GOOGL x3, XLK x3.
- Current candidate diversity buckets: broad-us-equity-etf, consumer-staples-defensive-compounder, financials-market-infrastructure.
- Overused recent diversity buckets: other x11, healthcare-biotech x8, industrials-power x7, consumer x6, broad-market-etf x5, semiconductors-ai x5, mega-cap-internet-cloud x3.
- Weekly review must disclose any code or prompt edits through Telegram before commit/push.

## Latest Review Input

{
  "lessons": [
    "Repeated tickers became a drag on research quality: GOOGL, XLK, CRM, APGE, WSC, and NEOV reappeared across multiple runs, often with only weakly changed catalysts, which indicates the memory layer is not suppressing stale follow-ups well.",
    "Allocation-blocked candidates were a persistent failure mode: several otherwise plausible names were repeatedly rejected because the single-name allocation cap, max open-position count, or muted allocation state prevented execution, so the bot kept resurfacing non-actionable candidates.",
    "Sector concentration was too heavy in technology, semiconductors, biotech, and broad ETFs, with limited diversification into other defensible buckets, which suggests the candidate generator is overfitting to a small set of familiar themes.",
    "Freshness handling improved some decisions when the bot forced a new catalyst requirement, but it still allowed stale-watch behavior to persist for names like GOOGL and XLK, meaning the freshness gate is present but not strict enough.",
    "The repeated appearance of low-conviction ETF and mega-cap names suggests the system is leaning too much on market narrative and sector momentum instead of distinct, company-specific edges.",
    "Congressional and social signals appear to have had mixed value: they occasionally supported coverage quality, but they also triggered repeated rejections for being too weak or under-sourced, especially when used without a stronger fundamental catalyst.",
    "Hugging Face source and veto logic appears useful as a guardrail against source-thin hype, but it also seems to contribute to candidate starvation when the upstream research is already thin or repetitive.",
    "Chittick Cash appears to have improved triage by separating execution-ready, watch, and monitor-only outputs, but it did not fully solve repetition or prevent stale candidates from cycling back into the queue."
  ],
  "rejected_patterns": [
    "Stale repeated tickers with no new catalyst, especially GOOGL, XLK, CRM, APGE, WSC, and INTC.",
    "Allocation-blocked but still resurfacing candidates that cannot pass the single-name or position-count constraints.",
    "Broad sector echoing, especially repeated tech, semiconductor, biotech, and ETF exposure without compensating diversification.",
    "Low-weight social or congressional signals used as primary justification rather than as secondary confirmation.",
    "Source-thin hype and vague narrative catalysts that do not create a time-stamped, company-specific edge.",
    "Monitor-only or allocation-muted names being repeatedly surfaced as if they were near-term trade ideas.",
    "Candidates with no fresh company-specific catalyst being retained too long in the active queue.",
    "Repetitive daily research phrasing that restates momentum, analyst interest, or sector leadership without adding new evidence."
  ],
  "strategy_proposals": [
    "Add a hard stale-ticker suppression window so repeated names are excluded unless a materially new catalyst appears, such as earnings, guidance, filing, confirmed contract news, or a verified technical breakout.",
    "Create an allocation-feasibility precheck before candidate promotion so the system suppresses any name that cannot fit current allocation, position-count, or tier constraints.",
    "Implement sector cooling rules that down-rank sectors that have already produced multiple recent candidates, especially technology, semiconductors, biotech, and broad ETFs.",
    "Require a diversity quota across sector, market cap, and catalyst type before daily output is finalized, to prevent repeated clustering around the same theme set.",
    "Make social and congressional signals confirmatory only: they should not move a candidate into watch or execution-ready unless supported by a stronger fundamental, filing, or event-based catalyst.",
    "Prefer time-stamped, source-specific catalysts over narrative momentum language, particularly for mega-cap and
