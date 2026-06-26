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

- Repeated symbols in recent watchlist: none.
- Current candidate diversity buckets: energy-structural-gas, mega-cap-semiconductor-turnaround, non-mega-cap-internet-commerce.
- Overused recent diversity buckets: none.
- Weekly review must disclose any code or prompt edits through Telegram before commit/push.

## Latest Review Input

{
  "lessons": {
    "allocation_and_risk_guards": [
      "Single‑name caps and monitor/allocation‑muted flags are working; high‑concentration risks in mega‑caps (GOOGL, NVDA, MSFT, INTC) are repeatedly blocked before execution.",
      "Max open‑position count and 1–15% allocation/3–12% stop bands reliably prevent overextension and mis‑sized trades.",
      "Banned‑instrument and leverage screens are consistently enforced (PLTR, COIN, GLD, various ETFs/funds), preserving the v1 safety envelope."
    ],
    "stale_and_repeat_catalysts": [
      "Repeat‑decay and stale‑catalyst labels correctly identify over‑reused narratives in mega‑cap tech (GOOGL, MSFT, INTC) and GT, but the pipeline still surfaces these tickers frequently, indicating upstream memory/selection logic is not sufficiently penalizing repeats.",
      "HF memory similarity flags are effective at catching pattern replays, yet they operate mainly at the rejection stage, not at candidate generation, leading to redundant daily research output."
    ],
    "sector_and_ticker_usage": [
      "Semiconductors and internet/cloud platforms (INTC, TER, GOOGL, SHOP) are heavily represented among recent candidates, while defensives, healthcare, and true non‑US diversification are underrepresented.",
      "Energy and materials show up in narrow forms (XOM, EOG, EQNR, PHX, USAR) with a mix of good fundamental catalysts (EOG, EQNR) and noise‑heavy, thin‑source names (PHX, USAR on some dates).",
      "Some high‑quality industrials/business services (PAYX, OC, APH, GLW) do make it through, but they are not used to systematically counterbalance sector concentration elsewhere."
    ],
    "research_quality_vs_noise": [
      "Fundamental catalysts (earnings beats, price‑target changes, index inclusion, major corporate investments, dated regulatory filings) appear to correlate with higher confidence and execution‑ready tiers (TER, GLW, INTC, GT, PAYX, SHOP, EQNR).",
      "Low‑weight social/congress signals repeatedly trigger rejections (PLTR, DVN, SGN, EWY, EWT, AMC, CORT, NUVL, PHX) and frequently coincide with source‑thin or micro‑cap speculation, indicating these signals add more noise than value at current thresholds and routing.",
      "HF source/hype filters correctly reject source‑thin or hype‑driven ideas (ADI, GSK, SGN, PHX, USAR on some dates), improving research quality but also highlighting that upstream candidate sourcing still drags in hype before filters cut it."
    ]
  },
  "rejected_patterns": {
    "allocation_block_and_position_limits": [
      "Repeated attempts to add names when single‑stock allocation would exceed 15% (GOOGL, NVDA, SPMO, etc.) show a pattern of selection that does not sufficiently consider existing exposure until the guardrail fires.",
      "Multiple rejections due to max open‑position count underscore that the system is often generating new ideas without first cycling or trimming existing holdings, leading to unnecessary blocked trades."
    ],
    "repeat_decay_and stale_catalysts": [
      "Mega‑cap tech (GOOGL, MSFT, INTC, AAPL) and some cyclicals (GT) repeatedly appear with repeat_decay/stale_catalyst flags; this indicates that previous catalysts are being re‑used or re‑framed without genuinely fresh, dated events.",
      "Stale_catalyst plus confidence below 0.60 shows a pattern where narrative‑only or undated commentary is being treated as soft catalysts instead of being filtered out earlier."
    ],
    "social_buzz_and congress_signals": [
      "Low‑weight social/congress signals repeatedly fail gate checks and co‑occur with micro‑cap speculation, potentially delisted tickers, or no fundamental catalyst (SGN, DVN, CORT, NUVL, EWY, EWT, AMC, PHX).",
      "These patterns suggest that when social/congress features dominate, the candidate is more likely to be speculative, poorly sourced, or incompatible with the risk framework."
    ],
    "monitor_only_and allocation_muted conflicts": [
      "Frequent rejections citing \"candida
