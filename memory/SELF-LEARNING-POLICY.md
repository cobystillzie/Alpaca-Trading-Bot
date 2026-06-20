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
- Current candidate diversity buckets: mega-cap-internet-cloud.
- Overused recent diversity buckets: none.
- Weekly review must disclose any code or prompt edits through Telegram before commit/push.

## Latest Review Input

{
  "lessons": {
    "1_repeats_and_stale_tickers": [
      "Mega‑caps like **GOOGL, INTC, MSFT, AAPL** repeatedly re‑surface with **stale or non‑fresh catalysts** and then get blocked by repeat_decay, stale_catalyst, confidence, or allocation rules.",
      "Memory is catching and labeling this (repeat_decay, memory_similarity), but upstream research keeps re‑proposing the same names with only marginally updated narratives.",
      "Result: wasted research cycles, noisy logs, and little incremental edge from those repeats."
    ],
    "2_allocation_and_position_gating": [
      "Allocation and max‑open rules are doing their job but are **downstream bottlenecks**: many otherwise good ideas (RRX, SLB, WMT, UNH, NSC, TER, LULU, etc.) are blocked only because capacity is used elsewhere.",
      "Frequent `single-stock allocation > 15%` and `max open-position count exceeded` rejections show that **portfolio construction logic is not tightly integrated into idea generation**; the research layer often ignores actual capacity."
    ],
    "3_sector_and_thematic_concentration": [
      "Idea flow is heavily skewed to **tech / semis / mega‑cap internet** and **biotech / healthcare** with only episodic diversification into industrials, energy, consumer defensives, and thematic ETFs.",
      "Given you are a **long‑only swing** framework, sector mix is OK but not robustly diversified; the log still shows clusters of similar factor exposures (growth/tech momentum, speculative biotech, meme-ish tickers)."
    ],
    "4_research_output_quality": [
      "Catalysts are often **event‑lite**: price action (near 52‑week highs, rebounds), insider sales, or generic thematic narratives are over‑used vs. truly fresh company‑specific fundamentals.",
      "The pipeline does show some solid special situations (e.g., NUVL M&A + FDA, GLW–NVIDIA partnership), but many other entries are more headline‑driven than thesis‑driven."
    ],
    "5_signal_filters_effectiveness": [
      "The **HF hype/source filters** are working as guardrails: they consistently veto micro‑cap speculation, source‑thin social/congress mentions, and stale repeats (SGN, ADI, GSK, PLTR, etc.).",
      "The **social buzz / congressional signals** are net additive only as *weak confirmers*; when treated as primary catalysts they trigger a lot of rejections and noise.",
      "Chittick scores and HF filters help prioritize and de‑prioritize, but the research layer is not yet fully aligned with what those filters reward (fresh, multi‑source, fundamentally grounded catalysts)."
    ]
  },
  "rejected_patterns": {
    "ticker_repetition": [
      "Re‑emitting the same mega‑caps (GOOGL, INTC, MSFT, AAPL, NVDA, PLTR) without a **clearly new fundamental event** within the swing horizon.",
      "Allowing candidates that have already hit `repeat_decay` and `stale_catalyst` to re‑enter the daily shortlist solely because they remain thematically interesting or price is moving."
    ],
    "allocation_block_ignores_capacity": [
      "Generating tradeable recommendations that **cannot fit** current constraints (single‑stock cap, total positions) and only discovering this at execution time.",
      "Repeatedly proposing SPMO, NVDA, GOOGL, etc., at size levels that breach the 15% rule rather than resizing or skipping at the research stage."
    ],
    "weak_catalyst_construction": [
      "Relying on: (a) price momentum alone, (b) insider sales alone (e.g., ABNB CEO selling), or (c) generic sector rotation stories as standalone swing catalysts.",
      "Treating social buzz or isolated congress trades as primary catalysts without robust corroborating fundamentals, leading to rejections like DVN, EWY, EWT, LMT, SGN, AMC."
    ],
    "monitor_only_and_non_tradable_names": [
      "Surface **monitor‑only** or **non‑tradable** contexts (KO, WSC, HUMA, NTCAX, GENERIC‑CLIMATE‑ETF, EPP01, TGT, XLI/XLE etc.) as if they were viable trades, only to be rejected later.",
      "Including instruments that hit
