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
  "lessons": [
    {
      "id": "lesson_repeat_staleness",
      "text": "The bot is repeatedly surfacing the same tickers (e.g., SCHD 20+ times, UNP ~9 times, GLD multiple times in 48 hours, SQ/INTC with 7–8 repeats) with near-identical catalysts. Staleness penalties exist but are too weak; the research output is dominated by recycled names instead of new opportunities."
    },
    {
      "id": "lesson_allocation_constraints",
      "text": "Allocation and max-position rules are working (many trades rejected for >15% single-name or max open positions), but upstream candidate generation is not aware enough of these constraints and keeps re-proposing allocation-blocked or position-count-blocked names (e.g., FPS, GOOGL, NVDA, AEP). This wastes research bandwidth."
    },
    {
      "id": "lesson_sector_concentration",
      "text": "There is persistent over-focus on a few themes: semiconductors/AI (NVDA, INTC, PDFS, AI infra names), dividend/value ETFs (SCHD, DFAT, SPUS), and a handful of industrials/defensive names (UNP, GLD, LMT, utilities). Other sectors (e.g., diversified healthcare, global ex-US equity, broader consumer, small-cap non-AI) are under-researched."
    },
    {
      "id": "lesson_execution_vs_research_mismatch",
      "text": "Multiple candidates reach 'execution-ready' (GLD, UNH, AEP, HUMA, XRT), but many are then blocked by v1 bans or max-position rules. The research pipeline does not sufficiently incorporate the current execution constraints and banned patterns, leading to repeated generation of un-executable ideas."
    },
    {
      "id": "lesson_filter_rigidity",
      "text": "HF filters and the banned-v1 logic are very conservative (blocking GLD, COIN, LMT, FPS/VRT/FLEX, AEP/ORCL/ROP even when catalysts appear solid), which helps avoid hype, but the current implementation is blunt: once a name or pattern is flagged, subsequent higher-quality evidence is often ignored instead of reassessed."
    },
    {
      "id": "lesson_signal_quality",
      "text": "The bot correctly de-emphasizes low-weight social/congress buzz (rejections of PLTR, EWY, EWT, LMT, ORCL where social/congress is thin). However, this sometimes leads to discarding otherwise valid ideas without first checking if fundamental or institutional evidence can independently justify a trade."
    },
    {
      "id": "lesson_daily_output_pattern",
      "text": "Daily candidate tables show a pattern of incremental tweaks to the same stories (e.g., UNP grain volumes, India gold duty, SEC semiannual reporting) instead of novel angles or risk updates. This leads to repetitive daily research output with low marginal information gain."
    }
  ],
  "rejected_patterns": [
    {
      "pattern": "stale_repeated_tickers",
      "description": "Tickers with high repeat counts and no materially new catalysts continue to be surfaced. Examples: SCHD (20+ repeats with similar value/dividend rotation thesis), UNP (same grain-volume and SEC reporting angle re-used), GLD (same India duty hike catalyst repeated multiple times), SQ/INTC (upgrades and price action recycled).",
      "risk": "Crowds out fresher ideas, encourages overfitting to a small ticker universe, and can nudge the bot towards 'story addiction' rather than balanced portfolio research.",
      "action": "Introduce explicit hard caps and cool-downs on repeats and require a genuinely new catalyst or thesis update to re-qualify."
    },
    {
      "pattern": "allocation_blocked_resurfacing",
      "description": "Names repeatedly re-enter the candidate list even when allocation/margin/position-count constraints make them untradeable (GOOGL, NVDA, SPMO, FPS, AEP, etc.).",
      "risk": "Wastes candidate slots and adds noise to the research stream, while also encouraging frustration-oriented overrides in future versions.",
      "action": "Pre-check allocation/position constraints at candidate selection time and tag such names as 'allocation-muted' so they appear only in a diagnostic list, n
