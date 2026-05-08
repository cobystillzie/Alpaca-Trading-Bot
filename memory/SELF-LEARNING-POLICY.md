# Self-Learning Policy

This policy is updated by the weekly review and must be read by research, premarket, midday, close, and weekly routines.

## Active Directives

- Use balanced diversity: penalize stale repeated tickers, but allow repeats with fresh earnings, filings, guidance, contracts, upgrades, or confirmed breakouts.
- If a repeated ticker has no fresh catalyst, lower it to `stale-watch` and research at least two alternatives from underrepresented sectors.
- Top candidate sets should aim for at least three diversity buckets before execution-ready language is used.
- Allocation-blocked candidates must either propose a smaller safe tranche or name a different-sector alternative; do not keep repeating the same 8% target.
- Do not loosen live-trading, options, crypto, margin, short-selling, cash-reserve, or secret-handling rules.

## Current Weekly Findings

- Repeated symbols in recent watchlist: SCHD x19, WS x9, GLRE x8, MUX x8, VYM x7, DT x4, PEG x4, GDX x3.
- Current candidate diversity buckets: dividend-etf-defensive, software-observability, technology-semiconductors.
- Overused recent diversity buckets: broad-market-etf x31, other x27, industrials-power x14, financials x8, consumer x4, semiconductors-ai x4.
- Weekly review must disclose any code or prompt edits through Telegram before commit/push.

## Latest Review Input

```json
{
  "lessons": [
    "SCHD dominates with 20+ repeats, confirming persistent value/dividend rotation but risking opportunity cost from overexposure.",
    "High repeat counts (SCHD 20x, VYM 11x, WS 8x, PEG 15x, MUX 7x) indicate stale memory loops prioritizing familiar tickers over fresh signals.",
    "Sector concentration: dividend ETFs (SCHD/VYM), materials-mining (MUX/GDX/FSM), industrials (WS/GWW), financials (GLRE) lack broad diversity.",
    "Allocation blocks prevent scaling into winners (e.g., MUX downgraded to watch-allocation-constrained after repeats).",
    "Fresh candidates (e.g., SIMO +100% MoM, APP/PUBM adtech beats) show quality but get overshadowed by repeat staleness."
  ],
  "rejected_patterns": [
    "Single-stock allocation >15% (NVDA, GOOGL, SPMO repeats).",
    "Banned v1 instruments/leverage references (PLTR, MUX early rejection).",
    "HF memory filter + repeat_staleness (INTC, ADI, GSK, PLTR).",
    "Source-thin hype + low-weight social/congress signals (PLTR).",
    "Market-open execution skips due to daily order limits."
  ],
  "strategy_proposals": [
    "Implement repeat decay: reduce confidence by 0.05 per repeat beyond 5, prioritize fresh signals.",
    "Sector caps: max 25% any sector (current: dividend ETFs ~30%+ implied).",
    "Allocation refresh: rotate out SCHD/VYM if repeats >15, force 20% fresh allocation quarterly.",
    "Diversity matrix: require min 5 sectors represented in top-10 candidates.",
    "Stale ticker quarantine: 7-day cooldown for execution-ready after 10+ repeats."
  ],
  "self_learning_directives": [
    "Track 'regret cost' of rejected high-conviction fresh signals vs repeat comfort trades.",
    "Analyze HF filter efficacy: SIMO/SANM (9 HF sources, 0 vetoes) succeeded where PLTR failed.",
    "Monitor Chittick Cash signal strength: consistent 74-78 scores but low differentiation power.",
    "Log 'shadow portfolio' performance of top-5 fresh vs repeat-heavy candidates daily.",
    "Self-audit: if same 4 tickers appear in 70%+ daily outputs, trigger memory compaction."
  ],
  "signal_evaluation": {
    "Chittick Cash": "Consistent 74-78 scores across repeats (SCHD 78, WS 74, GLRE 74) but fails to break staleness loops - moderate signal, low actionability.",
    "Hugging Face filters": "Strong positive: 9 sources/0 vetoes for winners (SIMO, SANM, DT); rejects hype correctly (PLTR, ADI) - high quality filter.",
    "Social buzz": "Noise source: PLTR rejections show weak signals need corroboration - downweight unless 2+ sources.",
    "Congressional signals": "Low-weight noise: PEG 15x repeats with 'low-weight congressional volume' - disable or require earnings confirmation."
  },
  "safe_code_prompt_routine_changes": [
    {
      "change": "Add repeat decay to candidate scoring",
      "prompt_snippet": "Reduce confidence by 0.05 × (repeat_count - 5) for repeat > 5; prioritize fresh=True signals"
    },
    {
      "change": "Sector diversity enforcer",
      "prompt_snippet": "Reject lists with <5 sectors in top-10; flag if any sector >25% implied allocation"
    },
    {
      "change": "Fresh signal boost",
      "prompt_snippet": "Fresh=True candidates get +0.10 confidence boost; execution-ready requires fresh within 72h unless regime confirmation"
    },
    {
      "change": "Staleness quarantine",
      "prompt_snippet": "Ticker with repeat>12 moves to 'stale-watch' tier; requires new catalyst + fresh=True for execution-ready"
    },
    {
      "change": "Allocation rotation rule",
      "prompt_snippet": "If repeat>15, downgrade to 'watch-allocation-constrained'; force 20% portfolio to <7-day old signals"
    }
  ]
}
```
