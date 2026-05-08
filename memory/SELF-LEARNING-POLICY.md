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
  "analysis_date": "2026-05-08",
  "status": "CAUTIOUS - SIGNIFICANT OPERATIONAL ISSUES DETECTED",
  "critical_findings": {
    "stale_ticker_concentration": {
      "severity": "HIGH",
      "evidence": [
        "SCHD: 20 repeat cycles in 48 hours (2026-05-06 to 2026-05-08)",
        "MUX: 7 repeat cycles, confidence degrading (0.82→0.78), HF veto flag appeared",
        "GLRE: 7 repeat cycles, static catalyst text",
        "WS: 8 repeat cycles, identical 10-K commentary",
        "VYM: 11 repeat cycles, allocation-constrained status"
      ],
      "root_cause": "Memory system not pruning stale candidates; research loop recycling same tickers without new catalyst discovery",
      "impact": "Portfolio concentration risk; diminishing research signal-to-noise ratio"
    },
    "allocation_blocking_pattern": {
      "severity": "HIGH",
      "evidence": [
        "VYM flagged 'watch-allocation-constrained' (2026-05-07 07:16:10)",
        "MUX flagged 'watch-allocation-constrained' (2026-05-08 10:51:27)",
        "SCHD locked at 8.0% allocation across 20 cycles",
        "No portfolio rebalancing or exit signals observed"
      ],
      "root_cause": "Allocation ceiling hit but no position-sizing strategy or trim logic triggered",
      "impact": "Execution paralysis on high-conviction candidates; capital inefficiency"
    },
    "rejected_trade_analysis": {
      "severity": "MEDIUM",
      "pattern": "Allocation ceiling + leverage ban + social-signal weakness",
      "rejected_count": 13,
      "key_rejections": [
        "SPMO: 3x rejected (allocation ceiling)",
        "GOOGL: 3x rejected (allocation ceiling)",
        "NVDA: 2x rejected (allocation ceiling)",
        "PLTR: 4x rejected (banned v1 leverage + weak social signal + staleness)",
        "INTC/ADI/GSK: Rejected for staleness + HF memory filter similarity flags"
      ],
      "interpretation": "System correctly blocking over-concentration but lacks dynamic rebalancing to unlock capital"
    }
  },
  "filter_quality_assessment": {
    "chittick_cash_score": {
      "rating": "NEUTRAL_TO_WEAK",
      "observation": "Scores range 42–78; no clear correlation with execution-ready tier or confidence",
      "example_noise": [
        "DRCT (adtech): Chittick 42, HF Source 0, confidence 0.55 → still execution-ready",
        "INUV (adtech): Chittick 52, confidence 0.68 → watch tier",
        "Inconsistent weighting suggests Chittick not primary decision driver"
      ],
      "verdict": "Added complexity without improving candidate ranking; consider deprecating or reweighting"
    },
    "hugging_face_filters": {
      "rating": "MIXED_SIGNAL",
      "positive": [
        "HF Source/Veto flags caught PLTR leverage references (correct)",
        "Memory similarity filter flagged ADI/GSK/INTC repeats (correct)"
      ],
      "negative": [
        "HF Source counts (0, 7, 8, 9) lack transparency; unclear what constitutes 'source'",
        "HF Veto column mostly 0–1; low signal frequency",
        "MUX veto appeared late (2026-05-08) after 7 cycles; delayed detection"
      ],
      "verdict": "Useful for hard blocks (leverage, banned instruments) but noisy for ranking; improve source taxonomy"
    },
    "social_buzz_congressional_signals": {
      "rating": "WEAK_TO_NOISE",
      "evidence": [
        "PEG: 15 repeats on 'low-weight congressional volume signal' alone",
        "FATE: Officer option exercise flagged as +49.67% monthly gainer (insider activity ≠ catalyst)",
        "DRCT: Hermes awards (9,360% ROI claim) cited but no earnings/guidance follow-up",
        "Congressional signal on PEG never escalated despite 15 cycles"
      ],
      "verdict": "Social/congressional signals are low-conviction noise; require corroboration with earnings, guidance, or technical setup"
    }
  },
  "sector_diversity_audit": {
    "overweight_sectors": [
      "Materials/Mining: MUX, GDX, FSM, OLA (4 candidates, 7–8% allocations)",
      "Dividend/Value ETFs: SCHD, V
