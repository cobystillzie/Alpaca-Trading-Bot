# Self-Learning Policy

This policy is updated by the weekly review and must be read by research, premarket, midday, close, and weekly routines.

## Active Directives

- Use balanced diversity: penalize stale repeated tickers, but allow repeats with fresh earnings, filings, guidance, contracts, upgrades, or confirmed breakouts.
- If a repeated ticker has no fresh catalyst, lower it to `stale-watch` and research at least two alternatives from underrepresented sectors.
- Top candidate sets should aim for at least three diversity buckets before execution-ready language is used.
- Allocation-blocked candidates must either propose a smaller safe tranche or name a different-sector alternative; do not keep repeating the same 8% target.
- Recently rejected hard-ban, low-weight-only, allocation-blocked, or max-position-blocked ideas must stay in `monitor-only` or `allocation-muted` lanes with zero allocation until the blocker is resolved.
- Generic v1 ban rejections require a current eligibility recheck; do not suppress plain long-only stocks or ETFs solely because older logs mentioned leverage without explicit options, margin, short, crypto, or leveraged/inverse product evidence.
- Do not loosen live-trading, options, crypto, margin, short-selling, cash-reserve, or secret-handling rules.

## Current Weekly Findings

- Repeated symbols in recent watchlist: APGE x3, GOOGL x3, XLK x3.
- Current candidate diversity buckets: broad-us-equity-etf, consumer-staples-defensive-compounder, financials-market-infrastructure.
- Overused recent diversity buckets: other x11, healthcare-biotech x8, industrials-power x7, consumer x6, broad-market-etf x5, semiconductors-ai x5, mega-cap-internet-cloud x3.
- Weekly review must disclose any code or prompt edits through Telegram before commit/push.

## Latest Review Input

{
  "lessons": [
    "Stale-repeat control is partially working: GOOGL, INTC, XLK, GT, and APGE keep resurfacing, but the system now labels some as stale-watch or allocation-muted instead of overcommitting.",
    "Allocation gates are the strongest rejection layer: many otherwise plausible names were blocked because the model would exceed single-stock or max-open-position limits, which prevented overconcentration.",
    "HF vetoes are filtering hype and low-evidence ideas, especially source-thin social/congress-driven candidates and leverage-adjacent instruments.",
    "The output still overweights a few sectors, especially technology, semiconductors, and broad-tech ETFs, which reduces portfolio diversity and increases correlated risk.",
    "Research quality improves when the catalyst is company-specific, time-stamped, and verifiable; generic momentum, sector leadership, or vague analyst chatter adds noise.",
    "Repeated daily research output is still too repetitive when the same large-cap and ETF themes reappear without a materially new catalyst."
  ],
  "rejected_patterns": [
    "Reject or demote candidates that repeat across multiple runs without a new company-specific catalyst.",
    "Reject candidates that are blocked only because they violate allocation or open-position constraints and do not have a fallback plan to diversify the candidate set.",
    "Reject source-thin social buzz and congressional signals when they are not corroborated by stronger primary or near-primary evidence.",
    "Reject broad sector ETFs and mega-cap tech names when they crowd out non-correlated ideas and do not provide incremental alpha over direct stock exposure.",
    "Reject stale watch candidates that recycle the same rationale across days, especially GOOGL, XLK, CRM, APGE, GT, INTC, and WSC-like patterns.",
    "Reject candidates that are monitor-only or allocation-muted if the pipeline is presenting them as near-trade ideas instead of quarantined research items."
  ],
  "strategy_proposals": [
    "Adopt a freshness-first ranking rule: if a candidate lacks a new filing, earnings event, guidance change, regulatory filing, product launch, or similarly dated catalyst, cap it at watch or monitor-only.",
    "Add sector diversification constraints to candidate generation so one run cannot be dominated by technology, semiconductors, or broad ETFs.",
    "Prefer underrepresented sectors and bucket types after a repeated sector has already been surfaced in the recent lookback window.",
    "Require a distinct catalyst delta before reissuing the same ticker; the ticker should only reappear at higher tier if the new catalyst meaningfully changes the thesis.",
    "Treat allocation-blocked candidates as a signal to search elsewhere rather than as a near-trade success.",
    "Use a diversification score alongside confidence so a high-confidence but overrepresented sector is discounted relative to a slightly lower-confidence but novel candidate."
  ],
  "self_learning_directives": [
    "Learn which catalyst types most often survive test gates: fresh filings, earnings, guidance changes, and concrete corporate actions outperform vague sentiment.",
    "Learn to down-rank repeated tickers unless the new run adds a materially different reason to act.",
    "Learn to distinguish signal from noise in social and congressional inputs by measuring how often those inputs lead to approved trades versus rejections.",
    "Learn which buckets are chronically overused and suppress them until the candidate mix rebalances.",
    "Learn from rejected trades that allocation failures are not hidden opportunities; they are evidence the candidate generation stage is too concentrated.",
    "Learn to keep stale ideas in memory for monitoring, not promotion, unless freshness and guard conditions improve."
  ],
  "safe_changes": [
    "Add a post-test-gate deduplication step that suppresses the same ticker for a defined cooling period unless a new catalyst is detected.
