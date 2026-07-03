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
- Current candidate diversity buckets: consumer-internet-streaming, consumer-staples, mega-cap-internet-cloud.
- Overused recent diversity buckets: other x6, mega-cap-internet-cloud x3.
- Weekly review must disclose any code or prompt edits through Telegram before commit/push.

## Latest Review Input

{
  "lessons": {
    "stale_and_repeated_tickers": [
      {
        "issue": "Mega-cap, AI-adjacent names keep resurfacing with decaying catalysts",
        "evidence": [
          "GOOGL appears repeatedly with `repeat_decay`, `stale_catalyst`, and `memory_similarity` in rejections, and again as monitor-only with no fresh catalyst.",
          "INTC shows multiple `repeat_decay` / `stale_catalyst` rejections, then reappears later as execution-ready once a clearly new TPU order catalyst is found.",
          "USAR, GT, MSFT, ARM, META, SMCI also show multiple passes where catalysts degrade from fresh to stale or source-thin."
        ],
        "lesson": "The memory and candidate generation pipelines are too willing to re-surface names on weakly updated narratives. Catalysts must be treated as expiring objects with explicit freshness windows and decay profiles."
      },
      {
        "issue": "Allocation-blocked tickers consume research bandwidth without incremental benefit",
        "evidence": [
          "Repeated GOOGL, NVDA, SPMO, XLK, MSFT rejections due to 15% single-stock cap, max open-position count, or allocation-muted flags.",
          "Several days where the system tries to trade allocation-muted or monitor-only tickers (XLK, VST, JBHT, KO etc.) even after prior similar rejections."
        ],
        "lesson": "Guard-rail conditions (position limits, monitor-only, allocation-muted) are being checked too late in the pipeline. This leads to repeated work on candidates that cannot be acted on."
      }
    ],
    "sector_concentration_and_diversity": [
      {
        "issue": "Overweight AI/tech/infrastructure narratives, underweight broader market",
        "evidence": [
          "Frequent candidates: NVDA, INTC, ARM, SMCI, VRT, PLTR, META, GOOGL, plus AI-infrastructure industrials.",
          "Relatively scarce non-AI sectors: only occasional appearances from financials (C), staples (CAG), transports/industrials (GE, JBHT, UPS, WMT, NSC), healthcare (GNFT, GSK, HUMA) and energy/materials (MP, USAR, EMAT).",
          "Morgan Stanley-type commentary stresses broadening earnings and leadership into Consumer Discretionary, Transports, and Regional Banks, but the bot’s candidates remain heavily clustered in a narrow AI/mega-cap theme.[12]"
        ],
        "lesson": "Theme concentration is high; the engine is not sufficiently enforcing portfolio and research diversification rules. It gravitates toward the same AI / mega-cap stacks even when the macro context favors broadening leadership."
      },
      {
        "issue": "Diversity at the research-output level is weak",
        "evidence": [
          "Many daily outputs center on similar catalyst types: AI cloud narratives, analyst initiations, funding/PIPEs, and congressional/social noise.",
          "There is minimal rotation into under-owned but strengthening groups highlighted by macro/breadth commentary (e.g., transports, regional banks, small caps).[12][24]"
        ],
        "lesson": "The research engine is not explicitly enforcing diversity across sectors, factor exposures, or catalyst types. This leads to repetitive daily research output uncorrelated with broader opportunity sets."
      }
    ],
    "signal_quality_evaluation": [
      {
        "issue": "Low-weight social/congress signals mostly add noise unless strictly gated",
        "evidence": [
          "Dozens of rejections explicitly cite: `Low-weight social/congress signal needs at least two stronger sources.`",
          "Names driven mainly by congress/social (EWY, EWT, DVN, AMC, PHX, VST, CAG, SPOT, C, GE, CORT, NUVL, OKLO, etc.) systematically fail due to `no_fundamental_catalyst`, `source_thin`, low confidence, or monitor-only status.",
          "Where congressional activity is cited (GE, C, SPOT, CAG), it is already treated as low-weight, and the resulting candidates rarely survive guard-rails."
        ],
        "lesson": "The current treatment (congress/social as secondary-
