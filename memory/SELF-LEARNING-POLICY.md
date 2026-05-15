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

- Repeated symbols in recent watchlist: GLD x7, LMT x5, UNP x4, COIN x3.
- Current candidate diversity buckets: consumer-discretionary-ETF, consumer-staples-defensive.
- Overused recent diversity buckets: industrials-power x11, broad-market-etf x10, other x5, healthcare-biotech x4, financials x3.
- Weekly review must disclose any code or prompt edits through Telegram before commit/push.

## Latest Review Input

{
  "lessons": {
    "1_stale_repetition": {
      "observation": [
        "SCHD appears ~20+ times with minimal new catalysts.",
        "UNP, GLD, INTC, SQ, FPS, VRT recur frequently within a few days, often with nearly identical notes.",
        "Daily tables are cluttered with high-Repeat names that are already allocation‑blocked or previously rejected."
      ],
      "takeaway": "The engine is over-surfacing the same tickers and catalysts, reducing marginal research value and masking genuinely new ideas.",
      "action_summary": [
        "Introduce a hard cool‑down window by ticker after N repeats.",
        "Down‑rank or hide stale names unless there is a clearly new, tagged catalyst.",
        "Separate a ‘rolling coverage watchlist’ from ‘new daily candidates’ so recurring coverage does not dominate daily output."
      ]
    },
    "2_allocation_and_guardrail_conflicts": {
      "observation": [
        "Many rejected trades (SPMO, GOOGL, NVDA, GLD, COIN, LMT, AEP, ROP, ORCL) fail guardrails (15% max single stock, max positions, v1 bans, low‑weight social/congress).",
        "Despite repeated guardrail failures, the same names keep appearing as ‘execution-ready’ or ‘watch’, then get blocked again at the trade gate."
      ],
      "takeaway": "Idea generation is not sufficiently conditioned on portfolio/guardrail state, causing wasted work and repetitive rejections.",
      "action_summary": [
        "Apply allocation/guardrail filters earlier in the pipeline before an idea is promoted to ‘execution-ready’.",
        "If a ticker is repeatedly blocked on structural rules (e.g., max allocation, v1 ban), treat it as ‘allocation-blocked’ and suppress further execution-ready flags until conditions change.",
        "Log and use rejection reasons as negative training signals for future candidate scoring."
      ]
    },
    "3_sector_and_theme_concentration": {
      "observation": [
        "Heavy clustering in semiconductors/AI (NVDA, INTC, PDFS, FPS, VRT, FLEX) and AI-infrastructure themes.",
        "Defensive ETFs and utilities (SCHD, SPUS, GLD, AEP, DFAT, FBND, XRT, WMT, COST) are often re-used as ‘diversification’ but repeat frequently.",
        "Some sectors (e.g., consumer discretionary ex-retail, emerging markets, small-cap quality, non-U.S. developed markets) are underrepresented."
      ],
      "takeaway": "Diversity is improving but still dominated by a few thematic clusters, causing correlation risk in hypothetical portfolios.",
      "action_summary": [
        "Explicitly track sector, factor, and theme exposure in candidate generation.",
        "Attach a diversification score to each candidate and down‑rank names that exacerbate existing concentration unless the catalyst is exceptional.",
        "Require some minimum representation of underexposed sectors/factors in daily research."
      ]
    },
    "4_daily_output_quality": {
      "observation": [
        "Many entries provide partially duplicated catalyst blurbs (GLD’s India duty hike is repeated with slightly different wording 8+ times).",
        "‘Fresh’ is sometimes marked yes even when there is no genuinely new information (e.g., UNP repeating the same grain-transport note).",
        "A few high-signal items (UNH, HUMA, AEP, WMT/COST set, DFAT/FBND) appear, but they are buried among repeated AI/GLD/SCHD items."
      ],
      "takeaway": "The signal-to-noise ratio of daily candidate tables is lower than it could be; ‘freshness’ is not strictly enforced.",
      "action_summary": [
        "Redefine ‘Fresh’ to require new event types or materially new data (e.g., new filing, rating change, guidance, macro/policy move), not just rephrasing.",
        "Cap repeated mention of the same catalyst over a short lookback window.",
        "Promote a concise ‘top 3–5 new ideas’ section separate from the rolling watchlist."
      ]
    },
    "5_hugging_face_filters_and_social_congress_signals": {
      "observation": [
        "HF Source and HF 
