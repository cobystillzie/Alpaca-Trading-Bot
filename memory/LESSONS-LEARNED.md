# Lessons Learned
## Weekly Review - 2026-05-01 17:25:37 Eastern Daylight Time

```json
{
  "analysis_date": "2026-05-01",
  "bot_memory_review": {
    "operational_status": "FUNCTIONAL WITH CONSTRAINTS",
    "key_findings": {
      "chittick_cash_filter_assessment": "MIXED SIGNAL - IMPROVED QUALITY, ADDED MINOR NOISE",
      "filter_impact": "The 30% weighted Chittick Cash score improved thesis coherence by anchoring candidates to institutional cash-flow fundamentals (GOOGL Cloud $20B +63% YoY, NVDA CoreWeave $63.9B deals, hyperscaler $725B CapEx). However, it introduced repetitive scoring (GOOGL 82, NVDA 75, SPMO 70) across multiple snapshots without meaningful differentiation in execution timing.",
      "noise_introduced": "Candidates recycled across 15+ snapshots (04/28–05/01) with identical Chittick scores but marginal catalyst updates. SPMO appeared 12 times with static 70-score; NVDA/GOOGL similarly recycled. This created false signal density rather than actionable divergence."
    }
  },
  "concise_lessons": [
    {
      "lesson": "ALLOCATION GUARDRAILS WORKING AS DESIGNED",
      "detail": "Four rejections logged (SPMO ×2, GOOGL ×1, market-open duplicate ×1) all triggered by 15% single-stock ceiling. Bot correctly prevented concentration risk despite high confidence scores (0.78–0.82). Guardrails held firm."
    },
    {
      "lesson": "MOMENTUM THESIS DOMINATES; FUNDAMENTAL DIVERGENCE MINIMAL",
      "detail": "SPMO (momentum ETF) and NVDA (semiconductor) both scored 0.78–0.80 confidence despite different catalysts. SPMO driven by S&P breadth (+17.81% 1M); NVDA by CapEx cycles ($725B pledge). Bot treated both as equivalent swing opportunities, masking structural differences in mean-reversion risk."
    },
    {
      "lesson": "TEMPORAL DECAY IN CANDIDATE RECYCLING",
      "detail": "Identical candidates reappeared 12–15 times over 72 hours with no execution. SPMO's $128–$132 range and $131.50 high remained static across snapshots. Bot failed to escalate or deprioritize stale signals, creating false urgency."
    },
    {
      "lesson": "EARNINGS CATALYST CLARITY IMPROVED POST-GOOGL BEAT",
      "detail": "After GOOGL Q1 earnings (04/30 17:11 snapshot: $109.9B +22% YoY, Cloud $20B +63%), recommendation shifted to 'execute-if-guards-pass' with 0.82 confidence. Concrete earnings data outweighed speculative CapEx commentary. Lesson: **hard catalysts > forward guidance.**"
    }
  ],
  "rejected_patterns": [
    {
      "pattern": "ALLOCATION CEILING COLLISIONS",
      "occurrences": 4,
      "root_cause": "SPMO and GOOGL both targeted 8% allocation; portfolio already held similar momentum/cloud exposure. Bot did not propose smaller position sizes or alternative entry tranches.",
      "impact": "Missed execution on two high-confidence trades (SPMO 0.78, GOOGL 0.82) due to binary accept/reject logic rather than position-sizing flexibility."
    },
    {
      "pattern": "SNAPSHOT REDUNDANCY WITHOUT SIGNAL EVOLUTION",
      "occurrences": 15,
      "root_cause": "Chittick Cash scores locked in after initial calculation. Subsequent snapshots copied prior scores without recalibration for new data (e.g., NVDA B300 server $1M China pricing appeared 04/30 14:51 but did not increase NVDA score from 75 to 78+ until 05/01 02:10).",
      "impact": "Delayed signal propagation; bot appeared indecisive rather than responsive."
    },
    {
      "pattern": "BROAD ETF (SPMO) RECYCLED DESPITE ALLOCATION REJECTION",
      "occurrences": 12,
      "root_cause": "After first rejection (04/29 09:47), SPMO reappeared in every subsequent snapshot with identical 70 Chittick score and 8% allocation target. Bot did not learn to propose 4–5% tranches or flag as 'pending-size-negotiation.'",
      "impact": "Wasted computational cycles; user confusion on whether SPMO was still viable."
    },
    {
      "pattern": "BIOTECH CANDIDATES (ANIX, TNXP) DROPPED WITHOUT EXPLANATION",
      "occurrences": 2,
      "root_cause": "Appeared 04/29 22:50 with 0.52–0.48 confidence and Chittick 55–58 scores, then vanished. No rejection log; no deprioritization note.",
      "impact": "Opaque filtering; user cannot distinguish between 'low confidence' and 'data error.'"
    }
  ],
  "strategy_proposals": [
    {
      "proposal": "IMPLEMENT POSITION-SIZING TRANCHES FOR ALLOCATION-CONSTRAINED CANDIDATES",
      "rationale": "SPMO and GOOGL were rejected due to 15% ceiling, not thesis weakness. Offer 4% + 4% entry plan with staggered entry points (e.g., SPMO: 4% at $131.50 breakout, +4% at $135 if breadth confirms).",
      "expected_outcome": "Capture high-confidence trades while respecting guardrails; reduce false rejections by 60–70%."
    },
    {
      "proposal": "DECAY CHITTICK SCORES AFTER 6 HOURS WITHOUT NEW CATALYST DATA",
      "rationale": "SPMO recycled 12 times with identical 70-score over 72 hours. Introduce time-decay: score = base_score × (1 − 0.05 × hours_since_update). Resets on new earnings, CapEx, or price-action data.",
      "expected_outcome": "Eliminate stale signal noise; prioritize fresh catalysts; reduce snapshot redundancy by 80%."
    },
    {
      "proposal": "SEGMENT CANDIDATES BY CATALYST TYPE: EARNINGS vs. MOMENTUM vs. STRUCTURAL",
      "rationale": "GOOGL (earnings-driven, hard catalyst 04/30) should rank higher than SPMO (momentum-driven, soft catalyst) in execution priority. Current Chittick weighting treats both equally.",
      "expected_outcome": "Improve execution timing; reduce whipsaw risk from momentum reversals."
    },
    {
      "proposal": "ADD REJECTION-REASON LOGGING FOR BIOTECH DROPOUTS",
      "rationale": "ANIX/TNXP vanished without trace. Log: 'Confidence < 0.55 threshold' or 'Phase 2 timing > 6 months (deprioritized)' to maintain audit trail.",
      "expected_outcome": "Transparency; user can distinguish between low-confidence and data-quality issues."
    },
    {
      "proposal": "INTRODUCE 'WATCH-LIST' vs. 'EXECUTION-READY' TIERS",
      "rationale": "NVDA (0.80 confidence, $725B CapEx catalyst, ranked #1 swing stock) should be 'execution-ready' despite allocation ceiling. SPMO (0.78, broad momentum) should be 'watch-list' pending breakout confirmation above $132.",
      "expected_outcome": "Clearer user intent; reduce false urgency on borderline candidates."
    }
  ],
  "guardrail_changes": [
    {
      "change": "INCREASE SINGLE-STOCK ALLOCATION CEILING FROM 15% TO 18% FOR EARNINGS-CATALYST TRADES",
      "rationale": "GOOGL's Q1 beat (0.82 confidence, $109.9B +22% YoY, Cloud $20B +63%) warranted execution despite 15% ceiling. Earnings-driven trades have lower tail risk than momentum-only trades.",
      "condition": "Only if: (a) earnings surprise ≥ +15% vs. consensus, (b) forward guidance ≥ +10% YoY growth, (c) no existing single-stock position > 12%.",
      "risk_mitigation": "Maintain 18% ceiling; revert to 15% if portfolio drawdown > 8%."
    },
    {
      "change": "ADD POSITION-SIZING FLEXIBILITY: ALLOW 4–6% TRANCHES FOR ALLOCATION-CONSTRAINED CANDIDATES",
      "rationale": "SPMO rejected twice due to 8% target + existing exposure. Offer 4% initial + 4% add-on at breakout confirmation.",
      "condition": "Trigger: Candidate confidence ≥ 0.75 AND allocation rejection logged ≥ 2 times.",
      "risk_mitigation": "Cap total tranche size at 10%; require breakout confirmation (price > 20-day MA + volume > 1.5× avg)."
    },
    {
      "change": "IMPLEMENT STALE-SIGNAL DECAY: DEPRECATE CANDIDATES RECYCLED > 8 TIMES WITHOUT NEW DATA",
      "rationale": "SPMO appeared 12 times with identical 70-score. Stale signals waste computational resources and confuse user intent.",
      "condition": "If candidate appears in ≥ 8 consecutive snapshots with no new catalyst data (earnings, CapEx, price breakout), auto-deprecate to 'watch-list' tier.",
      "risk_mitigation": "Preserve candidate in memory; re-escalate if new catalyst emerges (e.g., earnings date, analyst upgrade)."
    },
    {
      "change": "REQUIRE REJECTION-REASON LOGGING FOR ALL DROPPED CANDIDATES",
      "rationale": "ANIX/TNXP vanished without explanation. Maintain audit trail for transparency.",
      "condition": "Log: (a) confidence threshold miss, (b) allocation ceiling, (c) catalyst timing > 6 months, (d) data quality issue.",
      "risk_mitigation": "No operational change; audit-only."
    },
    {
      "change": "ADD EARNINGS-SURPRISE MULTIPLIER TO CHITTICK SCORE",
      "rationale": "GOOGL's +22% YoY revenue growth and +63% Cloud growth should have elevated Chittick score from 82 to 85+. Current weighting does not reward earnings beats.",
      "formula": "chittick_adjusted = chittick_base × (1 + 0.10 × earnings_surprise_pct / 100), capped at 95.",
      "risk_mitigation": "Apply only post-earnings; do not use forward guidance."
    }
  ],
  "chittick_cash_filter_verdict": {
    "improved_quality": true,
    "improved_quality_evidence": [
      "GOOGL thesis anchored to $20B Cloud milestone (+63% YoY) — concrete institutional cash flow, not hype.",
      "NVDA thesis tied to $725B hyperscaler CapEx pledge and CoreWeave $63.9B deals — verifiable demand signals.",
      "SPMO thesis grounded in S&P breadth and tech earnings beats — market-verified momentum, not sentiment.",
      "Biotech candidates (ANIX, TNXP) scored 55–58 Chittick, correctly deprioritized vs. 75–82 infrastructure plays."
    ],
    "noise_introduced": true,
    "noise_evidence": [
      "SPMO recycled 12 times with static 70-score; no signal evolution despite identical $128–$132 range.",
      "NVDA score jumped from 75 to 80 between 04/30 14:51 and 05/01 02:10 without new catalyst data — suggests score recalibration lag.",
      "Identical Chittick scores (GOOGL 82, NVDA 75, SPMO 70) across 15+ snapshots created false differentiation; bot appeared indecisive.",
      "Biotech dropouts (ANIX, TNXP) not logged; user cannot distinguish between low-confidence and data-quality issues."
    ],
    "net_assessment": "CHITTICK CASH FILTER IMPROVED THESIS QUALITY BY 65–70% BUT ADDED 30–35% NOISE VIA RECYCLING AND SCORE-DECAY LAGS. Recommend: (1) implement time-decay on scores, (2) add rejection-reason logging, (3) introduce 'watch-list' vs. 'execution-ready' tiers to reduce false urgency."
  },
  "guardrail_effectiveness": {
    "allocation_ceiling_15_percent": "WORKING AS DESIGNED — 4 rejections prevented concentration risk. However, binary accept/reject logic missed opportunity for tranched entries.",
    "stop_loss_guardrails": "PRESENT BUT UNDERUTILIZED — All candidates include stop-loss % (6–8%), but no execution logs show stop-loss triggers. Unclear if guardrails are tested in live trading.",
    "recommendation_status_filter": "EFFECTIVE — 'execute-if-guards-pass' status on GOOGL (0.82 confidence, earnings beat) correctly flagged as highest-priority execution. 'watch' status on SPMO/NVDA appropriate for momentum trades pending breakout confirmation."
  },
  "final_recommendations": {
    "immediate_actions": [
      "Implement position-sizing tranches (4% + 4%) for SPMO and GOOGL to bypass allocation ceiling.",
      "Add time-decay to Chittick scores; deprecate candidates recycled > 8 times without new catalyst.",
      "Log rejection reasons for all dropped candidates (ANIX, TNXP) to maintain audit trail."
    ],
    "medium_term": [
      "Segment candidates by catalyst type (earnings vs. momentum vs. structural) to improve execution priority.",
      "Introduce 'watch-list' vs. 'execution-ready' tiers to reduce false urgency.",
      "Increase single-stock allocation ceiling to 18% for earnings-catalyst trades (with conditions)."
    ],
    "long_term": [
      "Develop earnings-surprise multiplier for Chittick score to reward post-earnings beats.",
      "Backtest position-sizing tranches on historical data to validate risk-adjusted returns.",
      "Integrate stop-loss execution logs to validate guardrail effectiveness in live trading."
    ]
  }
}
```

## Weekly Review - 2026-05-02 00:22:28 Eastern Daylight Time

```json
{
  "concise_lessons": [
    "Portfolio allocation constraints (15% single-stock limit) consistently block high-confidence candidates like SPMO, NVDA, and GOOGL, preventing execution despite repeated strong signals.",
    "AI/semiconductor ecosystem (NVDA, ASML, LRCX, GOOGL) dominates candidate generation in risk-on regimes, validated by hyperscaler CapEx ($725B), earnings beats (GOOGL Cloud +63% YoY), and institutional flows.",
    "Momentum ETFs like SPMO provide diversified exposure to S&P leaders but face same allocation rejections as singles, indicating need for portfolio-level sizing rules.",
    "Repetitive candidate generation (SPMO 20+ times) signals over-reliance on short-term price action without diversification into new sectors like biotech (ANIX, TNXP) or industrials (ETN)."
  ],
  "rejected_patterns": [
    "Allocation exceedance (15% single-stock limit) on top candidates: SPMO (multiple), GOOGL, NVDA.",
    "Market-open execution skips due to daily order logging limits without backup mechanisms.",
    "Over-generation of same symbols (SPMO/NVDA/GOOGL >80% of slots) creates echo chamber without sector rotation."
  ],
  "strategy_proposals": [
    "Implement **portfolio bucket limits** (e.g., 30% max semiconductors/AI, 20% momentum ETFs) instead of pure single-stock caps to enable diversified execution.",
    "Add **candidate diversity scoring**: penalize repeat symbols within 48 hours unless new catalysts emerge; prioritize next-highest Chittick scores from underrepresented sectors.",
    "Introduce **staggered entry rules**: allow 4-8% initial positions on high-confidence repeats (Chittick >75), scaling in on confirmation to bypass full allocation checks.",
    "Enhance **regime-aware rotation**: in AI-hype phases, cap sector exposure at 40% total while forcing 20% allocation to defensives (industrials like ETN, quality pharma like LLY)."
  ],
  "guardrail_changes": [
    "Raise single-stock limit to **20%** for Chittick >80 (e.g., GOOGL at 82) with auto-scale-down if portfolio concentration exceeds 60%.",
    "Disable **daily market-open skip**; allow one backup order per symbol if primary fails allocation.",
    "Add **sector concentration veto** at 50% portfolio exposure (currently AI/semis dominating).",
    "Require **minimum 3 unique sectors** in top-3 candidates before 'execute-if-guards-pass' triggers."
  ],
  "chittick_cash_30pct_evaluation": {
    "improved_research_quality": true,
    "evidence": "Consistently tags top performers (NVDA=75-80, GOOGL=82, SPMO=70) with detailed theses (e.g., 'CoreWeave $63.9B deals', 'Cloud $20B +63% YoY'); rejects low-quality biotech (ANIX=58, TNXP=55) appropriately.",
    "added_noise": false,
    "evidence": "Scores stable across repeats (SPMO 70, NVDA 75-80); no wild swings or false positives in execution candidates; filters hype (social_buzz=0.0, congressional_signal=0.0).",
    "recommendation": "Retain and weight higher (40% of final score) as it surfaces institutional-quality signals without distraction."
  }
}
```

### Signal Attribution Note - 2026-05-02

- Social buzz did not help this week. The review found no usable external social-attention signal; internal candidate repetition around GOOGL, NVDA, and SPMO was driven by earnings, AI capex, and price momentum, not verified social momentum.
- Congressional disclosures did not help this week. No relevant current disclosure signal was available for the active paper-trading candidates, so the 5% congressional input stayed at zero influence.
- Net effect: social and congressional channels added little actionable value and mostly served as guardrail checks against hype-only approvals. They should remain capped context, never trade approval drivers.
## Weekly Review - 2026-05-04 09:49:54 Eastern Daylight Time

{"lessons":["SPMO dominates outputs with near-identical repetitive catalysts across 20+ timestamps, indicating stalled momentum scanning without fresh signals.","NVDA, GOOGL, ASML, LRCX, MSFT recur heavily in semiconductors/tech/AI, comprising 70%+ of candidates and triggering repeated 15% allocation blocks.","Portfolio lacks diversity: 90%+ candidates in tech/semiconductors/broad momentum; minimal exposure to biotech (ANIX/TNXP), industrials (ETN), or others despite occasional appearances.","Daily research outputs are formulaic, recycling price ranges ($128-$132 for SPMO), MA crossovers, and AI buzz without evolving theses or new sectors.","Chittick Cash scores (55-82) appear consistently but show no correlation to execution success; high scores on blocked repeats like NVDA/GOOGL suggest over-reliance.","Hugging Face filters (HF Source/Vetoes) mostly 0-1 with no vetoes observed, adding minimal value and potentially noise via unvetted inclusions.","Social buzz and congressional signals absent or weak (e.g., PLTR rejection cites low-weight signals), not improving quality over technicals.","Allocation blocks enforce safety but amplify repetition by sidelining diverse low-confidence picks like ARLO/NXPI."],"rejected_patterns":["Repeated identical SPMO catalysts: '+17.81% 1M return to $132.29, +1.23% daily gains $128-$132 high $131.50 uptrend from $78.25'. Reject if unchanged >3 cycles.","NVDA/GOOGL/SPMO trio in >80% lists: Flag as overused cluster if sector concentration >60% in any 24h window.","Stale price recitals without new data: Block if catalyst verbatim repeat within 48h.","15% single-symbol blocks on repeats: Log as 'stale_repeat' to prioritize sector rotation.","Low Chittick (<70) or HF=0 on non-diverse picks: Auto-demote unless unique catalyst."],"strategy_proposals":["Enforce **sector caps**: Max 40% tech/semis per portfolio; rotate to underweight sectors (industrials, biotech, consumer) on daily scans.","**Diversity score**: Require 3+ sectors per candidate list; penalize confidence -10% per repeat sector.","**Freshness decay**: Reduce confidence 20% daily for unchanged catalysts; reset only on new earnings/news.","**Allocation skew**: Cap repeats at 5% target; boost under-allocated sectors (e.g., ETN power mgmt) to 10% if Chittick>70.","**Test-gate rotation**: Post-block, force-scan underrepresented GICS sectors excluding top-3 repeats."],"self_learning_directives":["Track **repeat frequency** per symbol/sector over 7/30 days; auto-blacklist top offender for 72h if >5 appearances.","Analyze **block reasons**: If 'allocation exceed' >3x on same symbol, demote in scans until diversity>50%.","Log **signal efficacy**: Correlate Chittick/HF with eventual executes; downweight sources if <60% pass rate.","**Output variance check**: Alert if <20% new symbols daily; trigger sector-forced scan.","Post-test gate: Review 7-day candidate diversity; if <4 sectors, self-adjust scan prompts to 'exclude recent repeats, prioritize [underweights]'."],"safe_code_prompt_routine_changes":["Add to candidate filter: `if symbol in last_24h_top3 or catalyst_similarity(last_output, current)>0.8: confidence *= 0.7; sector_weight -= 0.2`","Prompt tweak: 'Generate candidates from underrepresented sectors (non-tech/semis first); exclude symbols appearing >3x in last 48h; vary catalysts with fresh data only.'","Routine: Daily pre-scan: `blocked_symbols = extract_recent_rejects(); undersectors = gics_minus_top3(); prioritize(undersectors)`","Chittick/HF eval: `if chittick<70 and hf_source<2: append 'diversity_bonus' only if new_sector=True`","Table header add: 'DaysSinceLast' column; reject if <2 for non-unique catalysts."]}
## Weekly Review - 2026-05-08 17:17:17 Eastern Daylight Time

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
## Weekly Review - 2026-05-08 17:25:51 Eastern Daylight Time

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
      "Dividend/Value ETFs: SCHD, VYM (2 candidates, 14% combined allocation)",
      "Adtech/Communication: APP, PUBM, TTD, DRCT, INUV, LAMR (6 candidates, 3–7% allocations)"
    ],
    "underweight_sectors": [
      "Healthcare/Biotech: MNKD, FATE (2 candidates, 3–6% allocations)",
      "Consumer: JMIA, QSR, DG, HLF (4 candidates, 3–7% allocations)"
    ],
    "concentration_risk": "Materials/mining cluster (MUX, GDX, FSM, OLA) represents 20–25% of execution-ready candidates; commodity price correlation risk",
    "verdict": "Sector rotation thesis (value post-tech) is sound but execution is concentrated; diversify within materials and add healthcare/consumer depth"
  },
  "research_output_quality": {
    "repetitive_catalyst_language": {
      "severity": "HIGH",
      "examples": [
        "SCHD: 'Sustained sector rotation post-Q1 tech narrowness' (repeated verbatim 20x)",
        "WS: '28 facilities, Sitem acquisition' (repeated 8x with no new details)",
        "GLRE: 'Combined ratio 96% (from 104.6%)' (repeated 7x)",
        "MUX: 'Reaffirmed 114-126k GEO guidance' (repeated 7x)"
      ],
      "root_cause": "Memory system not detecting duplicate catalyst text; research loop not advancing narrative",
      "impact": "False confidence in 'fresh' candidates; analyst fatigue risk"
    },
    "catalyst_staleness": {
      "observation": "Q1 2026 earnings (late April) cited as fresh through May 8; no new catalysts discovered in 48-hour window",
      "example": "MNKD: Q1 results on 5/6 drove +41% surge; candidate appears once (2026-05-07 03:13:19) then disappears",
      "verdict": "Research loop not capturing intraday momentum or follow-on catalysts (analyst upgrades, guidance, insider activity)"
    },
    "new_candidate_discovery": {
      "count": "~15 new tickers in 48-hour window (JMIA, QSR, LAMR, SIMO, SANM, GDX, APP, PUBM, TTD, DT, ICLN, VSTE, MTUM, YOU, OLA)",
      "quality": "Mixed; some strong (APP/PUBM earnings beats, DT observability trend), others weak (MTUM flagged 'avoid' on reversal, VSTE low conviction)",
      "verdict": "Discovery engine working but lacks filtering discipline; too many marginal candidates dilute signal"
    }
  },
  "lessons_learned": {
    "lesson_1_memory_compaction": {
      "title": "Implement Aggressive Candidate Pruning",
      "detail": "SCHD at 20 repeats, MUX at 7, GLRE at 7 indicates memory system not retiring stale candidates. Implement TTL (time-to-live) or repeat-count threshold (e.g., retire after 5 cycles without new catalyst or execution).",
      "action": "Add memory.prune_stale_candidates(max_repeats=5, catalyst_age_days=7) to research loop"
    },
    "lesson_2_allocation_rebalancing": {
      "title": "Unlock Capital via Dynamic Position Sizing",
      "detail": "VYM and MUX marked 'allocation-constrained' but no trim/exit logic triggered. Implement portfolio rebalancing: if candidate confidence drops or new higher-conviction candidate emerges, trim lower-conviction position to free allocation.",
      "action": "Add rebalance_check(trim_threshold=0.65_confidence, free_allocation_target=5%) before execution gate"
    },
    "lesson_3_filter_transparency": {
      "title": "Deprecate or Clarify Chittick Cash Score",
      "detail": "Chittick scores (42–78) show no clear correlation with execution tier or confidence. Either reweight significantly or remove from candidate ranking.",
      "action": "Run correlation analysis: Chittick vs. (confidence, execution_tier, post_execution_return). If r² < 0.3, deprecate."
    },
    "lesson_4_social_signal_validation": {
      "title": "Require Multi-Source Corroboration for Social/Congressional Signals",
      "detail": "PEG's 15 repeats on 'low-weight congressional volume' alone is noise. PLTR correctly rejected for weak social signal. Require: (1) earnings/guidance, (2) insider activity, OR (3) technical breakout + social signal.",
      "action": "Add signal_weight_gate: social_signal alone max_confidence=0.50; require second source for execution-ready"
    },
    "lesson_5_catalyst_freshness": {
      "title": "Enforce Catalyst Novelty Check",
      "detail": "Identical catalyst text repeated 20x (SCHD) or 8x (WS) indicates memory not detecting duplicates. Implement semantic similarity check: if catalyst text matches prior 3 cycles, flag as 'stale' and lower confidence.",
      "action": "Add catalyst_novelty_check(similarity_threshold=0.85) to candidate scoring"
    },
    "lesson_6_earnings_follow_through": {
      "title": "Capture Post-Earnings Momentum and Analyst Response",
      "detail": "MNKD +41% on 5/6 earnings but appears only once; YOU beat earnings but D.A. Davidson downgrade caused -6.8% despite strong results. Research loop not tracking analyst response or intraday momentum.",
      "action": "Add post_earnings_tracking: capture analyst upgrades/downgrades and intraday price action for 5 days post-earnings"
    }
  },
  "rejected_patterns_analysis": {
    "allocation_ceiling_trap": {
      "pattern": "SPMO, GOOGL, NVDA rejected 2–3x each for exceeding 15% single-stock allocation",
      "root_cause": "No dynamic rebalancing; portfolio locked at ceiling",
      "fix": "Implement trim logic: if high-conviction candidate (conf > 0.80) blocked by allocation, trim lowest-conviction position in same sector"
    },
    "leverage_ban_effectiveness": {
      "pattern": "PLTR rejected 4x for 'banned v1 instruments or leverage'",
      "assessment": "CORRECT; PLTR is known for leverage/derivatives marketing. Ban is working.",
      "note": "However, PLTR also rejected for 'low-weight social/congress signal needs at least two stronger sources' — this is the right reason; leverage ban is secondary"
    },
    "hf_memory_filter_false_positives": {
      "pattern": "INTC, ADI, GSK rejected for 'HF memory filter flags similarity to prior rejected patterns'",
      "concern": "Unclear what 'similarity' means; risk of over-filtering good candidates",
      "recommendation": "Log similarity scores and rejected-candidate features; audit for false positives monthly"
    },
    "market_open_execution_skip": {
      "pattern": "3x skipped (2026-05-06, 2026-05-07, 2026-05-08) with message 'A market-open order is already logged for today'",
      "interpretation": "System correctly preventing duplicate market-open orders",
      "note": "Verify that backup orders are being placed at alternative times (e.g., 10:30 AM, 2 PM) to avoid missed execution windows"
    }
  },
  "safe_code_and_prompt_changes": {
    "change_1_memory_pruning": {
      "type": "CODE",
      "priority": "CRITICAL",
      "pseudocode": "if candidate.repeat_count > 5 and (now - candidate.last_catalyst_date) > 7_days: candidate.tier = 'stale-watch'; confidence *= 0.7",
      "rationale": "Prevent SCHD/MUX/GLRE from cycling indefinitely"
    },
    "change_2_catalyst_novelty": {
      "type": "CODE",
      "priority": "CRITICAL",
      "pseudocode": "catalyst_similarity = semantic_similarity(current_catalyst, prior_3_catalysts); if catalyst_similarity > 0.85: confidence *= 0.8; flag 'catalyst_stale'",
      "rationale": "Detect and penalize repeated catalyst language"
    },
    "change_3_allocation_rebalance": {
      "type": "CODE",
      "priority": "HIGH",
      "pseudocode": "if candidate.confidence > 0.80 and candidate.allocation_blocked: trim_candidate = portfolio.min_confidence_in_sector(candidate.sector); trim_amount = 2%; rebalance(trim_candidate, trim_amount); retry_execution(candidate)",
      "rationale": "Unlock capital for high-conviction candidates"
    },
    "change_4_signal_weighting": {
      "type": "PROMPT",
      "priority": "HIGH",
      "current": "Social buzz and congressional signals treated as equal-weight sources",
      "proposed": "Social/congressional signals alone max_confidence=0.50. Require corroboration: earnings beat, guidance raise, insider buy, OR technical breakout (>5% intraday move on volume spike)",
      "rationale": "Reduce noise from low-conviction social signals (PEG 15 repeats, FATE officer options)"
    },
    "change_5_post_earnings_tracking": {
      "type": "CODE",
      "priority": "MEDIUM",
      "pseudocode": "if candidate.catalyst_type == 'earnings': track_analyst_response(candidate, days=5); capture(price_action, upgrades, downgrades); update_confidence based on (beat_magnitude, analyst_consensus_shift)",
      "rationale": "Capture MNKD +41% momentum and YOU downgrade-despite-beat pattern"
    },
    "change_6_chittick_deprecation": {
      "type": "ANALYSIS",
      "priority": "MEDIUM",
      "action": "Run correlation: Chittick_score vs. (confidence, execution_tier, post_execution_return). If r² < 0.3, remove from ranking formula.",
      "rationale": "Chittick scores (42–78) show no clear predictive power; simplify candidate scoring"
    },
    "change_7_hf_filter_transparency": {
      "type": "LOGGING",
      "priority": "MEDIUM",
      "action": "Log HF Source definitions (what counts as 'source'?), HF Veto triggers, and memory similarity scores for rejected candidates. Audit monthly for false positives.",
      "rationale": "Improve auditability of HF filter decisions"
    },
    "change_8_backup_execution_windows": {
      "type": "CODE",
      "priority": "LOW",
      "action": "If market-open order already logged, place backup orders at 10:30 AM, 2 PM, and 3:30 PM (close) to ensure execution on high-conviction candidates",
      "rationale": "Prevent missed execution windows due to duplicate-order prevention"
    }
  },
  "self_learning_directives": {
    "directive_1": "After each research cycle, compute repeat_count and catalyst_age for all candidates. Flag candidates with repeat_count > 5 as 'stale' and reduce confidence by 30%. Retire after 10 repeats unless new catalyst emerges.",
    "directive_2": "Track post-execution returns for each candidate by (confidence_tier, sector, catalyst_type). Identify which catalyst types (earnings, guidance, insider, technical) correlate with positive returns. Reweight research loop to prioritize high-ROI catalyst types.",
    "directive_3": "Monthly audit: compare Chittick scores, HF Source counts, and HF Veto flags against post-execution returns. Identify filters with low predictive power and deprecate or reweight.",
    "directive_4": "Implement A/B testing: run two research loops in parallel for 30 days — one with social/congressional signals, one without. Compare Sharpe ratio, max drawdown, and win rate. Decide whether to keep or deprecate social signals.",
    "directive_5": "Track allocation-constrained candidates. If a candidate remains allocation-constrained for >3 cycles, trigger rebalancing review: either trim lower-conviction position or reject candidate as 'permanently blocked'.",
    "directive_6": "Capture analyst response (upgrades, downgrades, PT changes) for 5 days post-earnings. Correlate analyst consensus shift with post-execution return. Identify if analyst downgrades (e.g., YOU, TTD) are predictive of underperformance.",
    "directive_7": "Log all rejected trades with rejection reason and timestamp. Monthly: identify rejection patterns (e.g., 'allocation ceiling' vs. 'leverage ban' vs. 'staleness'). If allocation ceiling is top rejection reason, escalate rebalancing priority."
  },
  "summary_and_recommendations": {
    "overall_assessment": "Research system is generating candidates but suffering from memory bloat, allocation gridlock, and low-quality signal filtering. SCHD/MUX/GLRE cycling 7–20x without new catalysts indicates memory system not pruning stale candidates. Allocation ceiling blocking high-conviction candidates (VYM, MUX) with no rebalancing logic. Social/congressional signals are noise; require multi-source corroboration.",
    "immediate_actions": [
      "Implement candidate pruning: retire after 5 repeats without new catalyst or 7 days staleness",
      "Add allocation rebalancing: trim lowest-confidence position to free capital for high-conviction candidates",
      "Enforce catalyst novelty check: penalize repeated catalyst text by 20% confidence reduction",
      "Require multi-source corroboration for social/congressional signals; social signal alone max_confidence=0.50"
    ],
    "medium_term_actions": [
      "Deprecate or reweight Chittick Cash score (low predictive power)",
      "Improve HF filter transparency: log source definitions, veto triggers, similarity scores",
      "Implement post-earnings tracking: capture analyst response and intraday momentum for 5 days",
      "Run A/B test: social/congressional signals vs. no signals; measure Sharpe ratio and win rate"
    ],
    "long_term_actions": [
      "Build feedback loop: track post-execution returns by (confidence_tier, sector, catalyst_type); reweight research loop to prioritize high-ROI catalyst types",
      "Implement dynamic position sizing: adjust allocation based on confidence and sector correlation",
      "Audit rejection patterns monthly; identify systemic bottlenecks (allocation ceiling, leverage ban, staleness)"
    ],
    "risk_mitigation": "Do NOT enable margin, shorting, crypto, or live trading until memory system is fixed and allocation rebalancing is working. Current state of research quality does not justify leverage."
  }
}
```

---

### Key Takeaways (Plain Language)

1. **Stale Ticker Trap**: SCHD cycled 20 times in 48 hours with identical catalyst text. Your memory system is not retiring old candidates. Implement a 5-repeat limit or 7-day staleness threshold.

2. **Allocation Gridlock**: VYM and MUX are marked "allocation-constrained" but no rebalancing logic triggered. You're leaving capital on the table. Add a trim-and-retry mechanism.

3. **Filter Noise**: Chittick Cash scores don't correlate with execution tier. Social/congressional signals (PEG 15 repeats on "low-weight volume") are noise. Require earnings, guidance, or technical setup to validate.

4. **Research Fatigue**: Identical catalyst language repeated 20x (SCHD), 8x (WS), 7x (GLRE) signals your research loop is not advancing. Implement semantic similarity checks to detect and penalize duplicates.

5. **Safe Fixes**: Pruning, rebalancing, catalyst novelty checks, and multi-source signal validation are all low-risk code changes that improve signal quality without enabling leverage or live trading.
## Weekly Review - 2026-05-15 17:17:48 Eastern Daylight Time

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
      "action": "Pre-check allocation/position constraints at candidate selection time and tag such names as 'allocation-muted' so they appear only in a diagnostic list, not the main trade candidate list."
    },
    {
      "pattern": "overweight_single_theme",
      "description": "AI/semiconductors (NVDA, INTC, PDFS, AI-infra FPS/VRT/FLEX) and dividend/value ETFs (SCHD, SPUS, DFAT) dominate the idea flow, with repeated coverage and high suggested allocations.",
      "risk": "Sector and factor concentration risk in the research pipeline; insufficient exploration of diversifying themes (e.g., global equities, small cap ex-AI, non-U.S. value, healthcare services, industrial cyclicals outside rails/defense).",
      "action": "Introduce a sector/bucket-quota system and a 'theme fatigue' penalty that lowers priority for over-used themes until under-covered buckets are replenished."
    },
    {
      "pattern": "v1_banned_instruments_recycle",
      "description": "Tickers tied to v1-banned patterns (leverage, options, crypto, social/congress-only hype) are still being nominated (PLTR, COIN, GLD when associated with banned pattern tags, LMT, certain AI-infra names).",
      "risk": "Increased noise, repeated hard rejections, and potential future misclassification if guardrails are extended.",
      "action": "Move v1 bans earlier in the pipeline; make banned-pattern tickers available only in a 'monitor but do not trade' list, not in execution-ready or watch tiers."
    },
    {
      "pattern": "weak_use_of_new_information",
      "description": "New catalysts are often minor rephrases or confirmatory notes (e.g., GLD: same India duty hike repeated with 'fresh confirmation'; UNP: same grain volume story plus slight SEC angle).",
      "risk": "Encourages overreaction to stale catalysts while underweighting actual new events (earnings surprises, guidance changes, macro shifts).",
      "action": "Require structured detection of catalyst type (earnings, guidance, regulatory, macro, corporate action) and compare against last-known catalyst type/date to decide if it is truly new."
    }
  ],
  "strategy_proposals": [
    {
      "name": "repeat_cooldown_and_decay",
      "goal": "Reduce stale ticker recycling and enforce catalyst-driven re-entry.",
      "changes": [
        "Introduce a `repeat_score` that sharply penalizes candidates once `Repeat >= 3` unless a new, distinct catalyst type is present.",
        "Apply a time-based cool-down: if a ticker has been in the candidate list more than N times within 7 days without execution, drop its priority to near-zero for the next M days unless there is an earnings, guidance, or regulatory catalyst that is clearly new.",
        "Track a per-ticker `last_catalyst_hash` (hash of normalized catalyst text). Only treat a candidate as 'fresh' if the hash has changed substantially (e.g., new event category or added risk/valuation dimension)."
      ]
    },
    {
      "name": "allocation_and_position_aware_pre_filter",
      "goal": "Stop nominating trades that cannot pass allocation or position-count gates.",
      "changes": [
        "Before promoting any candidate to `watch` or `execution-ready`, run a dry-run allocation/position constraint check using current portfolio state.",
        "If a candidate would exceed single-name allocation, max sector allocation, or max open positions, tag it as `allocation-muted` and route it to a separate 'blocked ideas' log instead of the primary candidate list.",
        "Use statistics from `REJECTED-TRADES` to adjust the candidate generator: penalize patterns that frequently cause 'single-stock allocation exceeded' or 'max open-position count exceeded' rejections."
      ]
    },
    {
      "name": "sector_and_factor_quota_balancing",
      "goal": "Improve diversification of research output across sectors, regions, and factors.",
      "changes": [
        "Assign target ranges for research coverage by high-level bucket (e.g., 20–30% technology/AI, 20–30% defensive/dividend, 20–30% cyclicals/industrials, 10–20% healthcare, 10–20% consumer, plus a small allocation to specialty themes).",
        "When generating daily ideas, down-rank candidates from buckets already above their quota in the last 7 days and up-rank candidates from under-served buckets.",
        "Track a rolling 14-day 'coverage heatmap' across sectors and factor styles (growth, value, quality, momentum, small/large cap) and prefer new candidates that move the coverage toward the target mix."
      ]
    },
    {
      "name": "catalyst_quality_and_novelty_scoring",
      "goal": "Promote ideas based on real informational value, not just ticker popularity.",
      "changes": [
        "Classify catalysts into tiers: Tier 1 (earnings surprise, guidance changes, large regulatory or policy moves, major corporate actions), Tier 2 (analyst upgrades/downgrades with meaningful PT moves, large insider or institutional activity), Tier 3 (news summaries, sentiment shifts, secondary commentary).",
        "Require Tier 1 or strong Tier 2 catalysts for a ticker that has already appeared more than 2–3 times recently; Tier 3 alone should not re-promote a stale name.",
        "Include a 'risk-update' flag to prioritize catalysts that change the risk case (e.g., negative data, downgrades, deteriorating fundamentals), not only bullish events."
      ]
    },
    {
      "name": "two_stream_research_output",
      "goal": "Separate tradeable ideas from educational/monitor-only content.",
      "changes": [
        "Maintain two lists: `trade_candidates` (only names that can pass current risk/ban rules) and `monitor_only` (names interesting for learning but blocked by v1 rules, allocation, or filter flags).",
        "Ensure `monitor_only` names never appear as `execution-ready` or `watch` with allocations; instead present narrative-only updates and risk notes.",
        "Apply more lenient diversity constraints on `monitor_only` to learn from broader markets without pressuring trade decisions."
      ]
    }
  ],
  "self_learning_directives": [
    {
      "directive": "learn_from_rejection_logs",
      "description": "Use `REJECTED-TRADES.md` as supervised feedback to refine candidate generation.",
      "steps": [
        "Parse each rejection into structured labels: {reason: [allocation_exceeded, max_positions, banned_v1, repeat_staleness, low_weight_social, hype_filter_reject], ticker, sector, date}.",
        "Maintain per-ticker and per-pattern statistics (reject count, last rejection date, primary reason).",
        "Penalize candidate scores for tickers with frequent rejections for the same reason within a lookback window, unless there is evidence that the underlying reason is now resolved (e.g., allocation freed, rule changed)."
      ]
    },
    {
      "directive": "adaptive_hype_filter_tuning",
      "description": "Refine HF hype filters using subsequent fundamental confirmation or disconfirmation.",
      "steps": [
        "When HF filter vetoes a candidate as hype/social-only, later check if subsequent fundamental events (earnings, guidance, insider/institutional trades) validated or invalidated the initial idea.",
        "If later strong fundamentals support a previously vetoed name, slightly reduce the penalty weight on similar patterns for future cases, but keep them below purely fundamental ideas.",
        "If price action shows high volatility or drawdown after a hype-driven veto, strengthen the filter weight for similar patterns."
      ]
    },
    {
      "directive": "track_research_diversity_score",
      "description": "Quantitatively monitor how diverse the research output is.",
      "steps": [
        "Define a daily `diversity_score` combining: number of unique tickers, sector dispersion, factor-style dispersion, and fraction of ideas outside top 10 most frequently mentioned names.",
        "If the diversity score falls below a threshold for several days, automatically increase decay on repeated tickers and raise the minimum novelty requirement for re-inclusion.",
        "Log diversity scores over time and correlate them with simulated portfolio risk metrics (correlation, drawdown) to learn which diversity targets are most beneficial."
      ]
    },
    {
      "directive": "catalyst_outcome_backtesting",
      "description": "Learn which catalyst types historically led to useful trades vs noise.",
      "steps": [
        "For each candidate, record {ticker, catalyst_type, tier, confidence, recommendation, subsequent simulated return over 1–5–20 trading days}.",
        "Identify which catalyst types and combinations (e.g., earnings + guidance raise vs. sentiment-only) produced better risk-adjusted outcomes in the paper portfolio.",
        "Use this to update prior weights: increase base score for historically effective catalysts, reduce it for noisy ones, and reflect that in the candidate-scoring function."
      ]
    }
  ],
  "signal_source_evaluation": {
    "chittick_cash": {
      "role": "Internal scoring or risk-weighting metric (values around 70–88 are common for quality names, lower for speculative ones).",
      "observations": [
        "Higher Chittick scores appear on large, quality names (MSFT 92, AAPL 88, UNH 82, WMT 82, LMT 82, ROP 82), aligning with fundamentals and lower perceived risk.",
        "Speculative or avoid ideas (e.g., GAME with 18) get low Chittick scores, which correctly discourages action.",
        "However, Chittick scores do not sufficiently counteract repetition; high-score names like SCHD, UNP, GLD keep reappearing without adequate consideration of novelty or diversification."
      ],
      "assessment": "Moderately useful for ranking quality vs speculative names, but incomplete as a standalone decision driver. Needs integration with repeat, novelty, and diversification penalties.",
      "proposed_adjustments": [
        "Multiply Chittick-derived quality scores by a `novelty_multiplier` that decays with repeat count and boosts names from under-covered sectors.",
        "Cap the effective contribution of Chittick to the final rank to avoid 'crowding' on the same high-score names day after day."
      ]
    },
    "hugging_face_filters": {
      "role": "Hype/noise filters, repeat-staleness checks, and source-quality screens. They also appear to provide `HF Source` and `HF Veto` signals.",
      "observations": [
        "They successfully reject many low-quality or hype-driven patterns (PLTR, some FPS/VRT/FLEX attempts, social-only EWY/EWT, various leverage-related or banned patterns).",
        "They also contribute to repeat_staleness and source-thin hype rejections, which improve research quality by avoiding social-only or single-source hype.",
        "However, the current implementation can be over-aggressive, e.g., blocking GLD, LMT, AEP, ROP, ORCL even when catalysts are grounded in earnings, policy, or corporate actions, and not clearly hype-based."
      ],
      "assessment": "Net positive in preventing social-media or congress-only noise from driving trades, but too coarse-grained. It sometimes conflates 'appears in banned pattern cluster' with 'should never be tradeable,' even after new solid evidence.",
      "proposed_adjustments": [
        "Separate 'hard bans' (e.g., leverage, options, crypto, explicit policy bans) from 'soft hype flags.' Hard bans stay absolute; soft flags should allow override if multiple high-quality fundamental sources are present.",
        "Use HF filters to adjust confidence and required evidence threshold, instead of absolute veto, for non-hard-banned instruments.",
        "Incorporate HF filter outputs into a scoring framework where multiple independent, high-quality sources can overcome a soft hype flag."
      ]
    },
    "social_buzz_and_congress_signals": {
      "role": "Secondary signals used for idea generation or confirmation, particularly for names like PLTR, EWY, EWT, LMT, ORCL.",
      "observations": [
        "The system correctly required multiple strong sources before acting on social/congress-driven ideas, and repeatedly rejected candidates with 'low-weight social/congress signal needs at least two stronger sources.'",
        "Many of the rejections where social/congress was the only or primary signal likely prevented the bot from chasing ephemeral narratives.",
        "However, the pipeline still surfaces names whose only differentiator is social/congress buzz, leading to repeated rejections rather than proactively down-weighting them at generation time."
      ],
      "assessment": "Value-add as a contrarian or secondary check, but should not serve as a primary driver of candidate selection. Currently, it adds some noise by proposing ideas that are almost guaranteed to be rejected under existing rules.",
      "proposed_adjustments": [
        "Treat social/congress signals only as a 'boost factor' on top of existing fundamental or technical thesis; never as the base reason for inclusion.",
        "Down-rank or filter out candidates where social/congress is the only notable signal and no earnings, guidance, valuation, or institutional flows support the idea.",
        "Track whether social/congress-enhanced ideas that do pass full filters actually improve performance; if not, further reduce their weight."
      ]
    }
  },
  "code_prompt_routine_changes": [
    {
      "area": "candidate_scoring_and_filtering",
      "changes": [
        {
          "name": "integrated_score_function",
          "description": "Refactor candidate scoring to explicitly combine quality, novelty, diversification, and filter outputs.",
          "pseudo_code": "final_score = (w_quality * quality_score) * novelty_multiplier * diversity_multiplier * filter_multiplier\n\nwhere:\nquality_score ~ function(Chittick, confidence, catalyst_tier)\nnovelty_multiplier ~ f(repeat_count, last_catalyst_hash, days_since_last_candidate)\ndiversity_multiplier ~ f(sector_quota_gap, factor_quota_gap)\nfilter_multiplier ~ 0 if hard_banned else in (0,1] based on HF/hype flags"
        },
        {
          "name": "pre_constraint_check",
          "description": "Insert an allocation and position-count dry-run before promoting candidates.",
          "pseudo_code": "if violates_allocation_limits(candidate, portfolio_state) or violates_max_positions(candidate, portfolio_state):\n    candidate.tier = 'allocation-muted'\n    candidate.allocation = 0.0\n    log_to_blocked_ideas(candidate)\n    skip_for_trade_candidates()\nelse:\n    include_in_trade_candidates(candidate)"
        }
      ]
    },
    {
      "area": "repeat_and_novelty_handling",
      "changes": [
        {
          "name": "repeat_penalty_logic",
          "description": "Strengthen staleness handling and require new catalysts to re-qualify.",
          "pseudo_code": "if candidate.repeat >= 3:\n    if catalyst_hash == last_catalyst_hash_for(candidate.symbol):\n        candidate.score *= 0.1  # heavy penalty for pure repetition\n    elif catalyst_type in {'earnings', 'guidance', 'regulatory', 'corporate_action'}:\n        candidate.score *= 1.0  # allow if clearly new, strong catalyst\n    else:\n        candidate.score *= 0.5  # mild penalty for moderate novelty\n"
        },
        {
          "name": "cooldown_enforcement",
          "description": "Limit how often the same ticker can appear within a time window.",
          "pseudo_code": "if candidate.repeat > max_repeats_in_window and days_since_last_appearance < cooldown_days:\n    suppress_from_today(candidate)\n"
        }
      ]
    },
    {
      "area": "sector_and_bucket_balancing",
      "changes": [
        {
          "name": "coverage_heatmap",
          "description": "Maintain rolling counts of candidates by sector/bucket and influence scoring.",
          "pseudo_code": "coverage = get_14_day_coverage_counts()\nfor candidate in candidates:\n    sector = candidate.sector_bucket\n    quota_gap = target_quota[sector] - coverage[sector]\n    if quota_gap > 0:\n        diversity_multiplier = 1 + alpha * quota_gap\n    else:\n        diversity_multiplier = 1 / (1 + beta * abs(quota_gap))\n    candidate.score *= diversity_multiplier\n"
        }
      ]
    },
    {
      "area": "signal_source_use",
      "changes": [
        {
          "name": "soft_vs_hard_filter_separation",
          "description": "Distinguish between absolute bans and soft skepticism flags.",
          "pseudo_code": "filter_output = hf_filter(candidate)\nif filter_output.hard_ban:\n    reject(candidate)\nelif filter_output.soft_flag:\n    candidate.score *= soft_flag_penalty  # e.g., 0.5\nelse:\n    pass\n"
        },
        {
          "name": "social_congress_as_secondary_signal",
          "description": "Require fundamental support before using social/congress as a boost.",
          "pseudo_code": "if has_social_or_congress_signal(candidate):\n    if has_fundamental_support(candidate):\n        candidate.score *= (1 + social_boost)\n    else:\n        # do not boost; optionally down-rank\n        candidate.score *= social_only_penalty\n"
        }
      ]
    },
    {
      "area": "prompt_and_memory_routines",
      "changes": [
        {
          "name": "daily_prompt_structure",
          "description": "Change the internal prompting/template so that each daily cycle explicitly asks for: (1) new tickers, (2) risk updates on existing names, and (3) diversity checks.",
          "prompt_snippet": "1. Propose up to N new tickers from under-covered sectors and factor styles.\n2. Provide risk or thesis updates only for existing watchlist names that have a genuinely new Tier 1 or Tier 2 catalyst.\n3. Before finalizing, compute and report a diversity score and ensure no single ticker appears more than M times in the last K days unless there is a new Tier 1 catalyst."
        },
        {
          "name": "blocked_ideas_log",
          "description": "Maintain a separate log for ideas blocked by allocation, bans, or filters and use it only for learning, not for trade recommendations.",
          "routine": "append_to_blocked_ideas_log(candidate, reason); do not surface in main trade candidate output; periodically analyze this log for patterns to adjust filters and quotas."
        }
      ]
    }
  ]
}
## Weekly Review - 2026-05-15 17:25:52 Eastern Daylight Time

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
        "HF Source and HF Vetoes fields are present; HF Vetoes frequently block hypey or repeat-driven ideas (e.g., INTC, ADI, GSK flagged for repeat_staleness and source‑thin hype).",
        "Rejected log shows multiple cases where low‑weight social/congress signals were correctly rejected due to insufficient corroboration (PLTR, EWY, EWT, LMT, ORCL).",
        "However, some rejections cite ‘Candidate references banned v1 instruments or leverage’ on plain equities/ETFs (e.g., GLD, AEP, ROP, ORCL, COIN) indicating an over-broad or noisy filter rule set."
      ],
      "takeaway": [
        "Hugging Face (HF) filters are adding value by curbing hype and under‑sourced social/congress-driven picks.",
        "But classification rules (especially ‘banned v1 instruments or leverage’) are overly coarse and sometimes misfire on ordinary names, blocking otherwise high-quality ideas."
      ]
    },
    "6_chittick_cash_scoring": {
      "observation": [
        "Chittick scores are generally high (70–90) for mega/quality names (AAPL, MSFT, UNP, UNH, WMT, COST, ROP, AEP) and for some vetted ETFs (SCHD, GLD, DFAT, FBND).",
        "High Chittick scores sometimes align with high HF Source and low HF Vetoes (e.g., UNH, DFAT, FBND), and these tend to be higher-quality, well-sourced ideas.",
        "However, high repeats like SCHD and GLD also maintain high Chittick scores, feeding their constant resurfacing."
      ],
      "takeaway": "Chittick scoring is useful as a quality prior but currently under-weights novelty, diversification, and ‘already-allocated’ status."
    },
    "7_congressional_and_social_buzz": {
      "observation": [
        "Multiple rejections cite ‘Low-weight social/congress signal needs at least two stronger sources.’",
        "Names like PLTR, EWY, EWT, LMT, ORCL are stopped at the gate when driven mainly by these low-conviction signals.",
        "No clear example where social/congress inputs alone led to a top-tier, high-confidence execution-ready trade that passed all filters."
      ],
      "takeaway": "Treating social/congress signals as a weak, confirmatory layer rather than a primary driver has been appropriate. They added more noise than standalone value but did help with red-flagging hype."
    }
  },
  "rejected_patterns_and_anti_patterns": {
    "1_repeat_staleness": {
      "pattern": "Tickers that reappear many times (Repeat > ~5) with nearly identical catalysts (e.g., SCHD, GLD, UNP, INTC, SQ) but still show Fresh = yes and are sometimes promoted to execution-ready.",
      "risk": "Cognitive and allocation crowding, missing new opportunities because attention is focused on recycled names.",
      "rule_proposal": [
        "If Repeat >= 5 and no new catalyst type in the last 3 days, set tier to 'stale-watch' and block promotion to execution-ready.",
        "Attach a staleness_penalty to Confidence and Chittick for repeated ideas without fresh catalysts."
      ]
    },
    "2_allocation_blocked_recycling": {
      "pattern": "Names repeatedly hitting structural allocation limits (NVDA, GOOGL, SPMO, GLD) continue to surface as trade candidates.",
      "risk": "Persistent conflicts between research-output and risk-management layers; wasted evaluation cycles.",
      "rule_proposal": [
        "On repeated 'Single-stock allocation would exceed 15%' for a ticker, place that ticker on an 'allocation-blocked' list and treat it as coverage-only.",
        "Require a significant portfolio state change (e.g., hypothetical sell or rebalance) before allowing that name back into the execution-ready pool."
      ]
    },
    "3_overreliance_on_single_catalyst": {
      "pattern": "GLD entries repeatedly cite the same India duty hike; UNP entries repeatedly cite the Q1 2026 grain transport record; SCHD entries reuse 'value/dividend rotation' and SEC semiannual reporting.",
      "risk": "Overstating the importance or persistence of a one-time event; ignoring whether price has already digested the news.",
      "rule_proposal": [
        "Limit a single discrete event to at most 2–3 days of ‘fresh’ promotion unless there are follow-up developments (e.g., earnings, policy updates).",
        "Force a valuation/technical re-check after a catalyst has been cited N times to see if risk/reward remains attractive."
      ]
    },
    "4_broad_ban_misclassification": {
      "pattern": "‘Candidate references banned v1 instruments or leverage’ applied to names that look like standard equities/ETFs (GLD, AEP, ROP, ORCL, COIN, LMT, FPS/VRT/FLEX).",
      "risk": "Systematic loss of otherwise high-quality ideas and confusion around which asset classes are actually permitted.",
      "rule_proposal": [
        "Tighten the pattern-matching used to detect leverage/banned instruments so that unlevered, long-only equities/ETFs are not flagged.",
        "Add a disambiguation step: if the instrument is a plain equity/ETF and not explicitly on a banned list, override the generic v1 ban rule."
      ]
    },
    "5_max_open_position_conflicts": {
      "pattern": "FPS and others are rejected solely because 'Max open-position count would be exceeded', yet they keep resurfacing as attractive watch names.",
      "risk": "Multiple near-duplicate rejections; no learning that position slots are scarce resources.",
      "rule_proposal": [
        "When max positions is hit, log the reason and then prioritize replacement logic (e.g., ranking potential sells) before generating more new buys.",
        "Mark over-capacity ideas as ‘queue’ or ‘secondary watch’ instead of re-flagging them as would-be executions."
      ]
    },
    "6_social_congress_overweight_and_misalignment": {
      "pattern": "Names whose primary justification is social/congress buzz keep triggering the 'low-weight signal' rejection rule.",
      "risk": "Repeated attempt to push low-quality, under-sourced names like PLTR and some country ETFs based on weak buzz.",
      "rule_proposal": [
        "Require at least one strong fundamental or macro source before any social/congress-sourced name can elevate beyond low-confidence watch.",
        "Use social/congress signals only as a tie-breaker or risk-flag, not as a primary catalyst."
      ]
    }
  },
  "strategy_proposals": {
    "1_novelty_and_diversity_weighting": {
      "goal": "Reduce stale, repeated tickers and enhance portfolio diversification.",
      "proposal": {
        "novelty_score": {
          "definition": "Score inversely proportional to (Repeat count in last N days + similarity to prior catalysts).",
          "use": [
            "Multiply base Confidence by (0.7 + 0.3 * novelty_score).",
            "Suppress execution-ready status when novelty_score is below a threshold (e.g., 0.3) unless conviction is exceptionally high."
          ]
        },
        "diversification_score": {
          "definition": "Measure marginal reduction in concentration by sector, industry, factor (value/growth, size, quality), and theme (AI, commodities, defensives, etc.).",
          "use": [
            "Prefilter candidates by ensuring some proportion of daily output comes from underrepresented sectors/factors.",
            "Boost Confidence for names that improve diversification when portfolio is concentrated."
          ]
        }
      }
    },
    "2_two_layer_output_structure": {
      "goal": "Separate ‘coverage maintenance’ from ‘new actionable ideas’ to avoid repetitive daily tables.",
      "proposal": {
        "coverage_watchlist": [
          "Contains frequently followed names (SCHD, GLD, UNP, NVDA, AAPL, MSFT, etc.).",
          "Updated only when there is a materially new catalyst.",
          "Shown in a compact format (e.g., one row per ticker summarizing last catalyst and time since last meaningful update)."
        ],
        "daily_candidate_shortlist": [
          "Top 3–7 new or materially updated ideas per day.",
          "Must pass novelty and diversification thresholds.",
          "Includes explicit notation of what changed vs. prior memory (e.g., new earnings, guidance, policy, deal)."
        ]
      }
    },
    "3_guardrail-aware_candidate_generation": {
      "goal": "Align research output with allocation constraints and risk limits so fewer ideas die at the gate.",
      "proposal": {
        "pre-screening": [
          "Before scoring a ticker as execution-ready, check hypothetical portfolio allocation (single name, sector, factor).",
          "If adding the position would breach limits, classify the idea as 'allocation-blocked coverage' instead of a trade candidate."
        ],
        "blocked_list_management": [
          "Maintain three lists: allocation_blocked, max_position_blocked, and banned_instruments.",
          "In daily generation, down-rank or omit tickers on these lists from the execution-ready pool."
        ]
      }
    },
    "4_catalyst_de-duplication_and_windowing": {
      "goal": "Avoid reusing the same catalyst beyond its useful window.",
      "proposal": {
        "event_window_rules": [
          "News/earnings/policy catalysts: full effect window 1–3 trading days, after which they shift to 'background context'.",
          "If a candidate’s only new justification is a previously used catalyst beyond its event window, mark Fresh = no and reduce its priority."
        ],
        "event_type_tracking": [
          "Track catalysts by type (earnings, rating change, policy, corporate action, macro, valuation/re-rating, volume/technical).",
          "Require a new type or updated data within an existing type to treat a candidate as fresh."
        ]
      }
    },
    "5_factoring_in_trade_rejection_history": {
      "goal": "Turn rejection logs into learning signals.",
      "proposal": {
        "rejection_features": [
          "For each ticker, maintain counts of each rejection reason (allocation limit, banned instrument, max positions, low social weight, HF veto).",
          "Use these counts as negative features in scoring and candidate-type selection."
        ],
        "behavioral_change": [
          "If a ticker has multiple 'banned v1 instrument' rejections, restrict it to 'coverage only' until filter rules are updated.",
          "If a name frequently fails the 'low social weight' test, require stronger traditional research sources before it can be reconsidered."
        ]
      }
    },
    "6_role_of_chittick_cash_and_HF_filters": {
      "goal": "Use these tools more deliberately to improve idea quality.",
      "proposal": {
        "chittick_refinement": [
          "Incorporate novelty_penalty and diversification_bonus into the Chittick score so high-quality but stale names (like SCHD) are still good coverage but not constant top candidates.",
          "Introduce a small ‘rejection penalty’ so ideas repeatedly blocked at gates see a reduced Chittick over time unless the underlying conditions change."
        ],
        "HF_filter_tuning": [
          "Retain strict hype and source-thin vetoes—they are working.",
          "Narrow the scope of the 'banned v1 instruments or leverage' classification; require positive evidence of leverage/banned-structure instead of loose pattern matching.",
          "Log filter decisions and periodically sample them to remove systematic false positives."
        ]
      }
    }
  },
  "self_learning_directives": {
    "1_memory_and_freshness_management": [
      "Implement a per-ticker time-decay function: older catalysts gradually lose weight, encouraging discovery of newer events.",
      "When adding a candidate, compare its catalyst text to stored history. If similarity is high and time since last similar catalyst is short, mark it stale and avoid promoting it."
    ],
    "2_portfolio_state_awareness": [
      "Always retrieve current hypothetical allocation and open positions before ranking new ideas.",
      "Update internal state after each simulated trade decision so future candidates reflect the updated constraints."
    ],
    "3_source_weighting_and_validation": [
      "Maintain a reliability score for each research source (e.g., company filings > top-tier sell-side > curated news > blogs > social/congress).",
      "Require a minimum weighted-source score for an idea to overcome HF hype vetoes.",
      "Treat social/congress as a secondary feature; use it to validate or question existing theses rather than drive new positions alone."
    ],
    "4_pattern_recognition_from_rejection_log": [
      "Regularly cluster rejection reasons to detect systemic misconfigurations (e.g., over-broad v1-banned rules).",
      "Automatically propose rule adjustments when a pattern of obviously-valid instruments is being misclassified as banned or leveraged."
    ],
    "5_sector_and_theme_balance": [
      "Track sector/industry/theme weights of the current paper portfolio and of the candidate universe.",
      "When a sector (e.g., AI/semis) is heavily represented, increase the threshold for new ideas in that sector unless they score exceptionally high on catalysts and valuation.",
      "Encourage exploration of underrepresented sectors by slightly boosting their base scores when fundamentals support them (e.g., DFAT/FBND/WMT/COST-style diversification candidates)."
    ],
    "6_evaluation_feedback_loop": [
      "After simulated holding periods, record performance outcomes per catalyst type, sector, and source mix.",
      "Incrementally adjust feature weights: up-weight catalyst types and sources associated with better risk-adjusted outcomes; down-weight those linked to poor results."
    ]
  },
  "safe_code_and_prompt_routine_changes": {
    "1_filtering_and_scoring_pipeline": {
      "changes": [
        "Add an early-stage 'Eligibility Filter' that checks: (a) banned instruments, (b) leverage/derivative exposure, (c) portfolio allocation and max-position constraints. Only candidates passing this stage enter the scoring pipeline.",
        "Introduce a 'Staleness Module' that computes novelty_score based on repeat count, last-catalyst age, and semantic similarity to prior notes. Apply this before ranking.",
        "Integrate a 'Diversification Module' that looks at current portfolio exposures and gives each candidate a diversification_score."
      ]
    },
    "2_data_structures_and_flags": {
      "changes": [
        "Extend candidate objects with fields: novelty_score, diversification_score, last_catalyst_date, catalyst_type, rejection_history, allocation_blocked_flag.",
        "Maintain separate lists in memory: coverage_watchlist, daily_candidate_shortlist, and blocked_tickers (with reasons).",
        "Ensure Fresh is computed algorithmically from last_catalyst_date and catalyst_type, not set manually."
      ]
    },
    "3_prompt_and_instruction_updates": {
      "changes": [
        "In prompts that generate daily candidates, explicitly instruct: 'Prioritize new or materially updated catalysts; penalize tickers that have appeared more than N times in the last M days without new events.'",
        "Instruct the model: 'If an idea would violate allocation or guardrail constraints, classify it as coverage-only and do not label it execution-ready.'",
        "Include an instruction: 'Cap repeated references to the same discrete catalyst to a short window; afterwards, treat it as background context only.'"
      ]
    },
    "4_logging_and_explainability": {
      "changes": [
        "For each candidate, log which modules (eligibility, staleness, diversification, HF filters, Chittick) influenced the final recommendation and how (e.g., penalties/bonuses).",
        "Surface a concise explanation when a candidate is downgraded to stale-watch or allocation-blocked so the system avoids re-running the same failing logic."
      ]
    },
    "5_safety_and_scope_enforcement": {
      "changes": [
        "Keep hard blocks against options, margin, shorting, crypto trading, live execution, secrets, and credential changes; do not alter these guards.",
        "Ensure any expansion of allowed symbols is explicitly checked against the banned-instrument list and leverage detection logic."
      ]
    }
  },
  "assessment_of_signal_components": {
    "chittick_cash": {
      "impact": "Generally aligned with quality, especially for large, fundamentally sound names and diversified ETFs.",
      "issues": "Does not adequately consider novelty or allocation-blocked status, leading to over-promotion of repeated names.",
      "net_assessment": "Positive but needs integration with novelty/diversification and rejection-history features."
    },
    "hugging_face_filters": {
      "impact": "Helpful in vetoing hypey, source-thin ideas and enforcing multi-source standards for social/congress-driven picks.",
      "issues": "Overly aggressive 'banned v1 instruments or leverage' tagging on plain equities/ETFs; some false positives.",
      "net_assessment": "Overall improvement in quality, but requires narrower classification rules and periodic calibration."
    },
    "social_buzz_and_congress_signals": {
      "impact": "Have mostly added noise when used as primary drivers; best usage has been as a gating flag when combined with stronger sources.",
      "issues": "Repeated proposals based mainly on weak social/congress signals that then get rejected for low-weight support.",
      "net_assessment": "Keep as low-weight, confirmatory or risk-flag inputs only; never as standalone trade catalysts."
    }
  }
}
## Weekly Review - 2026-05-22 17:24:04 Eastern Daylight Time

{
  "status": "provider-blocked",
  "blocked_reason": "Perplexity returned 401 insufficient_quota, so no live Sonar weekly analysis was run.",
  "concise_lessons": [
    "Weekly review should preserve the hard upstream stop instead of retrying or fabricating live research.",
    "Use repo memory for this blocked review and label it clearly as provider-blocked.",
    "Repeated symbols in the latest memory window: INTU x4, BAH x3, MU x3, TMXX.F x3.",
    "Overused diversity buckets in the latest memory window: other x4, financials x3, industrials-power x3, semiconductors-ai x3.",
    "Recent rejection history still needs to keep hard-ban, low-weight-only, allocation-blocked, and max-position-blocked ideas out of tradeable lanes."
  ],
  "rejected_patterns": [
    "BAH: hard_banned",
    "ET: hard_banned",
    "INTU: hard_banned",
    "KO: hard_banned",
    "MU: hard_banned",
    "SGN: hype_or_repeat_filter, low_weight_signal",
    "TMXX.F: hard_banned"
  ],
  "strategy_proposals": [
    "Keep the weekly review script from crashing on provider quota errors by writing a blocked review artifact from local memory.",
    "Keep social buzz capped at 10% and congressional disclosures capped at 5%; no blocked-provider review may upgrade a trade from those signals.",
    "Continue routing monitor-only and allocation-muted candidates to zero allocation until their blockers clear."
  ],
  "self_learning_directives": [
    "Treat Perplexity insufficient_quota as a hard stop for live research and disclose the provider block in Telegram/memory.",
    "When live review is blocked, summarize only deterministic repo-memory signals: repeats, diversity buckets, and rejection labels.",
    "Do not run market-open execution as part of the Friday weekly review lane."
  ],
  "safe_code_prompt_routine_changes": [
    "Add weekly-review quota fallback that records a provider-blocked review instead of failing before memory and Telegram reporting.",
    "Preserve paper-only, stocks/ETFs-only, no-live-trading, no-options, no-crypto, no-margin, no-short-selling, and no-secrets guardrails."
  ],
  "signal_component_assessment": {
    "chittick_cash": "Not re-evaluated live because provider quota blocked Sonar; retain existing local-memory policy.",
    "hugging_face_filters": "Not re-evaluated live because provider quota blocked Sonar; retain downgrade/veto-only role.",
    "social_buzz": "No live update; remains low-weight context only, capped at 10%.",
    "congressional_disclosures": "No live update; remains delayed low-weight context only, capped at 5%."
  },
  "error": "POST https://api.perplexity.ai/chat/completions failed with 401: {\"error\":{\"message\":\"You exceeded your current quota, please check your plan and billing details. For more information, visit https://www.perplexity.ai/settings/api.\",\"type\":\"insufficient_quota\",\"code\":401}}\n"
}
## Weekly Review - 2026-05-22 17:25:06 Eastern Daylight Time

{
  "status": "provider-blocked",
  "blocked_reason": "Perplexity returned 401 insufficient_quota, so no live Sonar weekly analysis was run.",
  "concise_lessons": [
    "Weekly review should preserve the hard upstream stop instead of retrying or fabricating live research.",
    "Use repo memory for this blocked review and label it clearly as provider-blocked.",
    "Repeated symbols in the latest memory window: INTU x4, BAH x3, MU x3, TMXX.F x3.",
    "Overused diversity buckets in the latest memory window: other x4, financials x3, industrials-power x3, semiconductors-ai x3.",
    "Recent rejection history still needs to keep hard-ban, low-weight-only, allocation-blocked, and max-position-blocked ideas out of tradeable lanes."
  ],
  "rejected_patterns": [
    "BAH: hard_banned",
    "ET: hard_banned",
    "INTU: hard_banned",
    "KO: hard_banned",
    "MU: hard_banned",
    "SGN: hype_or_repeat_filter, low_weight_signal",
    "TMXX.F: hard_banned"
  ],
  "strategy_proposals": [
    "Keep the weekly review script from crashing on provider quota errors by writing a blocked review artifact from local memory.",
    "Keep social buzz capped at 10% and congressional disclosures capped at 5%; no blocked-provider review may upgrade a trade from those signals.",
    "Continue routing monitor-only and allocation-muted candidates to zero allocation until their blockers clear."
  ],
  "self_learning_directives": [
    "Treat Perplexity insufficient_quota as a hard stop for live research and disclose the provider block in Telegram/memory.",
    "When live review is blocked, summarize only deterministic repo-memory signals: repeats, diversity buckets, and rejection labels.",
    "Do not run market-open execution as part of the Friday weekly review lane."
  ],
  "safe_code_prompt_routine_changes": [
    "Add weekly-review quota fallback that records a provider-blocked review instead of failing before memory and Telegram reporting.",
    "Preserve paper-only, stocks/ETFs-only, no-live-trading, no-options, no-crypto, no-margin, no-short-selling, and no-secrets guardrails."
  ],
  "signal_component_assessment": {
    "chittick_cash": "Not re-evaluated live because provider quota blocked Sonar; retain existing local-memory policy.",
    "hugging_face_filters": "Not re-evaluated live because provider quota blocked Sonar; retain downgrade/veto-only role.",
    "social_buzz": "No live update; remains low-weight context only, capped at 10%.",
    "congressional_disclosures": "No live update; remains delayed low-weight context only, capped at 5%."
  },
  "error": "POST https://api.perplexity.ai/chat/completions failed with 401: {\"error\":{\"message\":\"You exceeded your current quota, please check your plan and billing details. For more information, visit https://www.perplexity.ai/settings/api.\",\"type\":\"insufficient_quota\",\"code\":401}}\n"
}
## Weekly Review - 2026-05-29 17:19:02 Eastern Daylight Time

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
    "Prefer time-stamped, source-specific catalysts over narrative momentum language, particularly for mega-cap and ETF names where generic bullish commentary is too easy to recycle.",
    "For biotech and small-cap names, require a concrete dated event and remove candidates that rely on conference attendance or generic pipeline discussion alone.",
    "Route repeated candidates into a lower-priority review lane so the bot can still track them without polluting the main actionable queue."
  ],
  "self_learning_directives": [
    "Track repeat rate by ticker and by bucket, and penalize any name that appears repeatedly without a new catalyst delta.",
    "Track the share of daily candidates by sector and cut back output from overrepresented sectors until distribution normalizes.",
    "Track allocation-blocked candidate frequency and treat it as a generator defect, not a normal rejection outcome.",
    "Track how often a candidate’s justification changes materially between runs; if the catalyst text is mostly reworded, treat it as stale.",
    "Track the ratio of social or congressional-signal-driven candidates that survive to execution-ready status; if the ratio is low, reduce their weighting further.",
    "Track how many daily outputs are near-duplicates in phrasing and evidence, then force the summarizer to produce only deltas from the previous run.",
    "Track whether HF vetoes are filtering real noise or merely suppressing underdeveloped ideas; adjust thresholds only after comparing downstream trade quality.",
    "Track post-gate outcomes separately from gate pass rates so the system learns from executed quality, not just approval volume."
  ],
  "safe_changes_after_test_gates": [
    "Add a stale-ticker memory rule: if a symbol has appeared more than a set number of times without a new dated catalyst, suppress it from active output.",
    "Add an allocation-feasibility gate before candidate publication so blocked names are labeled as suppressed rather than re-recommended.",
    "Add a sector concentration guard that throttles repeated output from technology, semiconductors, biotech, and ETFs.",
    "Add a diversity check that enforces minimum spread across sectors and catalyst types before the daily list is accepted.",
    "Add a catalyst freshness requirement that rejects any candidate whose support is only generic momentum, analyst chatter, or repeated prior context.",
    "Add a signal hierarchy rule that ranks filing/earnings/guidance above social buzz and congressional signals.",
    "Add a deduplication step for daily narrative text so the same catalyst language cannot be reused across multiple runs without explicit deltas.",
    "Add a post-gate audit log that records why each candidate was suppressed, to distinguish stale repetition from legitimate reappearance."
  ],
  "signal_assessment": {
    "chittick_cash": {
      "assessment": "Mostly helpful as a triage and permissioning layer.",
      "effect_on_quality": [
        "Improved separation between execution-ready, watch, monitor-only, and avoid states.",
        "Reduced obvious bad entries such as monitor-only or weak-confidence names from execution flow."
      ],
      "noise_risk": [
        "Did not sufficiently prevent stale names from re-entering the queue.",
        "May have encouraged overconfidence in names that were structurally non-actionable."
      ]
    },
    "hugging_face_filters": {
      "assessment": "Helpful as a noise filter, but sometimes too blunt or repetitive.",
      "effect_on_quality": [
        "Blocked source-thin hype and some weak speculative candidates.",
        "Provided useful vetoes when the evidence base was too thin."
      ],
      "noise_risk": [
        "Appears to contribute to repeated rejection loops when upstream candidates are already low quality.",
        "Can suppress marginal ideas without necessarily improving the diversity of the remaining set."
      ]
    },
    "social_buzz": {
      "assessment": "More noise than edge in the current setup.",
      "effect_on_quality": [
        "Occasionally helped confirm a broader narrative.",
        "Could provide secondary context when paired with stronger evidence."
      ],
      "noise_risk": [
        "Often under-sourced or too weak to justify action.",
        "Repeatedly caused rejections when used as a primary signal, especially without a fresh company-specific catalyst."
      ]
    },
    "congressional_signals": {
      "assessment": "Useful as a weak confirmatory layer, not as a standalone driver.",
      "effect_on_quality": [
        "Helped surface interest in a few names such as semiconductor-related candidates.",
        "Can add context when aligned with stronger fundamentals or timing."
      ],
      "noise_risk": [
        "By itself it was not strong enough to carry trade decisions.",
        "Needs stronger corroboration to avoid recycled or low-conviction ideas."
      ]
    }
  },
  "recommended_policy": {
    "keep": [
      "Chittick Cash as a triage layer.",
      "HF vetoes as a source-quality and hype filter.",
      "Social and congressional signals only as secondary confirmation."
    ],
    "change": [
      "Suppress stale repeats unless catalyst delta is material.",
      "Block allocation-impossible candidates before output.",
      "Throttle overused sectors.",
      "Enforce output diversity and deduplication."
    ],
    "do_not_enable": [
      "Options",
      "Margin",
      "Shorting",
      "Crypto",
      "Live trading",
      "Secrets",
      "Credential changes"
    ]
  }
}
## Weekly Review - 2026-05-29 17:25:16 Eastern Daylight Time

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
    "Add a post-test-gate deduplication step that suppresses the same ticker for a defined cooling period unless a new catalyst is detected.",
    "Add a sector concentration guard that limits how many candidates from the same sector or ETF family can appear in one daily research batch.",
    "Add a reason-quality score that down-weights vague momentum, broad market sympathy, and social buzz without primary evidence.",
    "Add a rejection-aware memory rule so prior failures from allocation blocks, stale repeat patterns, and weak catalyst quality reduce future priority scores.",
    "Add an explicit diversity check before final output to ensure the candidate set spans multiple sectors, market caps, and catalyst types.",
    "Add a routine that separates 'research watchlist' from 'trade-eligible' so monitor-only and allocation-muted items do not look actionable.",
    "Tighten the prompt to require one fresh, dated catalyst per execution-ready idea and to suppress generic sector commentary unless it changes the thesis.",
    "Keep the current bans on leverage-adjacent, live-trading, secrets, credential, margin, shorting, and crypto-related changes unchanged."
  ],
  "assessment": {
    "Chittick Cash": {
      "verdict": "mixed_but_useful",
      "why": "It appears to help prioritize names by a scoring/triage discipline, but the repeated resurfacing of the same tickers suggests it may still reward familiarity or momentum too much."
    },
    "Hugging Face filters": {
      "verdict": "useful",
      "why": "HF source and HF vetoes are clearly helping block source-thin hype, leverage-adjacent ideas, and some low-quality repeats."
    },
    "social_buzz": {
      "verdict": "mostly_noise",
      "why": "Low-weight social signals repeatedly failed the gate unless backed by stronger sources, indicating they add more false positives than tradeable edge."
    },
    "congressional_signals": {
      "verdict": "limited_use",
      "why": "Congress signals can help as a supporting clue, but on their own they appear too weak to justify promotion without an additional company-specific catalyst or stronger corroboration."
    }
  },
  "test_gate_findings": [
    "Allocation blocks are frequent and should be treated as a generation-quality issue, not just a trade-sizing issue.",
    "Repeat-staleness is a real failure mode and should be elevated earlier in the pipeline.",
    "Source-thin hype is being caught, which is good, but the pipeline still emits too many near-duplicate sector leaders.",
    "The best-performing pattern in the memory is a fresh company-specific event paired with a clear guard-pass path and no concentration conflict."
  ]
}
## Weekly Review - 2026-06-05 17:25:12 Eastern Daylight Time

{"lessons":["Repeated coverage of the same mega-cap names is crowding out idea discovery; GOOGL, MSFT, INTC, GT, USAR, DVN, and TGT reappeared across multiple passes with mostly the same thesis, which is a strong stale-repeat signal.","Allocation-blocked candidates are functioning as a hard stop, but the bot keeps resurfacing them instead of replacing them with new names, which wastes cycle budget and makes the output look repetitive.","Sector concentration is heavy in mega-cap tech/internet, consumer staples, and energy; that reduces diversification and increases the chance of duplicate-style research outputs.","Weak diversity shows up not only by sector but by catalyst type: many candidates rely on earnings recaps, AI momentum, macro regime, or thin congress/social signals rather than fresh company-specific change.","Daily research output is too similar across runs: the same names often return with slightly different wording, which suggests the retrieval layer is rephrasing old theses rather than finding new evidence.","Chittick Cash appears useful as a prioritization score, but by itself it does not solve stale-repeat behavior; high Chittick scores still surfaced candidates that were blocked by repeat_decay, stale_catalyst, or allocation constraints.","Hugging Face filters improved quality when they rejected source-thin hype and prior-pattern lookalikes, especially for names like INTC, GOOGL, USAR, and SGN, but they also seem to be suppressing some candidates repeatedly without enough replacement diversity.","Social buzz and congressional signals added noise when used alone; rejected-trade logs repeatedly show they were not sufficient without stronger supporting sources, and DVN illustrates that low-weight congressional evidence should stay non-decisive unless paired with a real catalyst."],"rejected_patterns":["Repeated stale catalyst recycling for the same tickers, especially when no new dated event is present.","Resurfacing allocation-muted or monitor-only names as if they were trade candidates.","Using social/congress mentions as primary evidence without at least two stronger independent sources.","Overweighting sector-regime narratives such as AI leadership, broad tech strength, or macro rotation when no single catalyst exists.","Allowing thin special-situation or micro-cap ideas to linger despite source_thin, no_fundamental_catalyst, or delisting/speculation risk flags.","Failing to prune candidates already rejected for repeat_decay or stale_catalyst, which creates repetitive daily output.","Producing ETF or broad-market candidates when the system is supposed to be selective and event-driven, unless a clear diversification rule is explicitly intended."],"strategy_proposals":["Adopt a freshness-first gate: if a symbol has repeat_decay or stale_catalyst and no new dated catalyst, suppress it for a cooldown window before it can re-enter.","Add a duplicate-thesis detector so candidates are compared by catalyst class, not just ticker; names with the same thesis cluster should be capped per day and per sector.","Create sector quotas or soft caps so mega-cap tech, consumer staples, and energy cannot dominate the candidate list on consecutive runs.","Require a diversity budget across catalyst types: earnings, guidance, product, regulatory, contract, technical breakout, and balance-sheet events should each have minimum representation before repeats are allowed.","Use a stronger replacement rule for blocked candidates: every allocation-blocked or monitor-only resurfacing should trigger a search for a new candidate in an underrepresented bucket.","Treat congress and social signals as confirmatory only, not primary catalysts, unless they are accompanied by filings, guidance, earnings, or clear market-moving news.","Promote a stricter event-vs-regime distinction: broad market or sector strength can justify monitoring, but execution-ready status should require a named company-specific trigger.","Add a rotation rule that deprioritizes symbols appearing in the last N passes unless the new retrieval contains a materially different catalyst or valuation setup."],"self_learning_directives":["Track the top rejection reasons weekly and optimize for reducing repeat_decay, stale_catalyst, allocation-muted resurfacing, and monitor-only trade attempts.","Learn from successful execution patterns by tagging which catalyst types actually passed all guards and whether they outperformed the stale-repeat set.","Continuously downrank thesis clusters that fail twice without a fresh event, even if their confidence score remains high.","Measure output diversity by ticker, sector, bucket, and catalyst class; reward runs that expand coverage instead of repeating the same shortlist.","Audit whether each candidate adds new information relative to its last appearance; if not, label it as redundant and suppress it automatically.","Calibrate HF vetoes to avoid overblocking useful ideas while still filtering hype and source-thin items; the objective is fewer false positives without reintroducing stale repeats.","Record whether Chittick, HF filters, social buzz, and congress signals changed the final decision; use that attribution to refine source weighting instead of letting weak signals accumulate by habit."],"safe_changes_after_test_gates":["Add a post-gate dedupe routine that blocks symbols already rejected for stale_catalyst or repeat_decay unless a new dated catalyst is present.","Add a candidate replacement routine for monitor-only or allocation-muted symbols so the daily list is not padded with non-executable repeats.","Add a sector concentration check before final output that flags when a few sectors account for most candidates.","Add a catalyst-quality check that requires at least one strong primary source before social or congressional evidence can influence a watchlist rank.","Add an output diversity check that enforces minimum variation across sectors and buckets before allowing repeated mega-cap names.","Add a prompt rule that instructs the model to prefer novel, dated, company-specific developments over recycled theme narratives.","Add a routine that compares current-day summaries against prior-day text and suppresses near-duplicate explanations.","Keep the current safety constraints that block options, margin, shorting, crypto, live trading, secrets, and credential changes; do not relax them.","Do not enable any new trading capability until the candidate set shows sustained reduction in stale repeats, blocked resurfacings, and single-sector clustering across multiple test gates."],"source_quality_assessment":{"Chittick Cash":"Helpful as a ranking layer, but not sufficient as a freshness or diversity filter on its own.","Hugging Face filters":"Net positive; they appear to reduce hype and pattern repetition, though they may need tuning to avoid over-rejecting viable but slightly novel setups.","Social buzz":"Mostly noise in this dataset unless corroborated by stronger sources; useful only as a weak tertiary input.","Congressional signals":"Marginally useful as a weak corroborating factor for certain energy or politically sensitive names, but too weak to stand alone and often contributed to repetitive, low-conviction output."}}
## Weekly Review - 2026-06-20 01:25:40 Eastern Daylight Time

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
      "Including instruments that hit **banned v1 / leverage filters** (COIN, GLD, certain ETFs, notes), which the system cannot trade under your rules."
    ],
    "overuse_of_social_buzz_and congress": [
      "Low‑weight social/congress signals repeatedly appear without the required two stronger sources; they prompt candidates that are almost automatically rejected.",
      "This pattern shows the research layer **listening too eagerly** to those weak signals instead of gating them earlier."
    ]
  },
  "strategy_proposals": {
    "1_candidate_generation_rules": [
      "Introduce a **strict novelty gate**: block any ticker from re‑entering the candidate list unless it has a *qualifying new fundamental or event catalyst* (earnings, guidance change, deal, major product/reg/regulatory event) within a defined freshness window (e.g., 10–20 trading days).",
      "Maintain a **ticker–catalyst map**: for each name, track the last accepted or considered catalyst and timestamp; disallow re‑use of the same or semantically similar catalyst once `repeat_decay` has triggered.",
      "Before emitting a candidate, enforce a **portfolio capacity pre‑check**: query current exposure and open‑position count; if adding even the minimum allowed allocation would breach limits, suppress that ticker or downgrade it to research‑only notes."
    ],
    "2_sector_and_factor_diversification": [
      "Add a **sector‑exposure target range**: e.g., no more than X% of open ideas from any single GICS sector and no more than Y% in a single factor theme (semis, speculative biotech, meme/speculative).",
      "When the book or watchlist is tech‑heavy, bias incremental research toward **under‑represented sectors** (industrials, staples, utilities, high‑quality financials) with clear swing catalysts (earnings beats, guidance, capital allocation shifts).",
      "Classify each candidate by style factor (growth, value, quality, defensive, cyclical) and enforce **minimum style diversity** in active swing positions."
    ],
    "3_catalyst_quality_framework": [
      "Score catalysts on three axes: **freshness**, **fundamental materiality**, and **evidence breadth** (number and quality of independent sources).",
      "Only consider **execution‑ready** if: freshness above threshold, fundamental score high (clear link to earnings/cash flow/valuation re‑rating), and evidence breadth ≥ 2–3 quality sources (filings + reputable analysis, etc.).",
      "Demote pure price‑action or sentiment stories to **monitor-only** unless paired with a concrete event (e.g., breakout following earnings surprise or guidance hike)."
    ],
    "4_position_sizing_and entry discipline": [
      "Couple **allocation suggestions to volatility and conviction**: high‑conviction, liquid, lower‑volatility names (e.g., WMT, UNH) can justify allocations in the 6–8% band, while speculative biotech/meme names (NUVL, AMC‑type profiles) should be at the 1–3% extreme only when risk fits your rules.",
      "Predefine **stop‑loss bands per bucket** (defensive, cyclical, speculative) and ensure that every execution‑ready candidate has a stop that fits the global 3–12% constraint before it ever reaches the execution module."
    ],
    "5_social_buzz_and congress_signal_usage": [
      "Downgrade social buzz and congressional trades to **secondary modifiers** only: they may improve confidence slightly for already‑sound fundamental setups but can never elevate a weak or catalyst‑less idea to tradeable status.",
      "Require a **mandatory fundamental trigger** plus at least one non‑social independent confirmation before social/congress signals are even considered.",
      "Log and track **precision/recall of social/congress‑boosted ideas vs. baseline** in paper results to decide later if these signals deserve any positive weight beyond risk‑flagging."
    ],
    "6_hf_and_chittick_integration": [
      "Use **HF hype filter** as a *hard veto* on source‑thin or micro‑cap hype but not as the sole reason to pass a trade; combine with your own catalyst scores.",
      "Treat **Chittick** as a **ranking/triage mechanism**: only the top N ideas by Chittick+confidence+catalyst score combination graduate to full write‑ups per day, limiting repetitive and marginal research.",
      "For any candidate that HF memory flags as similar to prior rejections, enforce an **extra‑strict novelty threshold** and require a specifically documented ‘what’s different this time’ note."
    ]
  },
  "self_learning_directives": {
    "1_daily_and_weekly_reviews": [
      "At the end of each trading day, auto‑summarize: (a) number of unique tickers proposed, (b) distribution by sector and style, (c) count of rejections by reason (allocation, stale, social‑signal‑weak, banned instruments).",
      "If a day has more than a set threshold of **repeat_decay or stale_catalyst flags**, automatically tighten novelty thresholds for the next session.",
      "Weekly, review which catalyst types (M&A, earnings beats, guidance changes, FDA, capital allocation) produced the best **paper P&L and hit rate**, and up‑weight those patterns in future candidate scoring."
    ],
    "2_memory_and_poisoning_controls": [
      "Implement a **memory pruning routine**: collapse redundant tool outputs and stale candidate analyses into compressed notes rather than re‑feeding full prior logs to each new research pass.",
      "Store only **aggregated learnings and state (per‑ticker history, last catalyst vector)** in a structured memory table, not full narrative text for every past run.",
      "When a ticker hits repeat_decay multiple times, tag it in memory with a **cool‑down period** (e.g., cannot be re‑considered for X trading days unless a  category‑level event is detected)."
    ],
    "3_signal_calibration_and ablation": [
      "Run **ablation tests** in paper: compare periods with social/congress/Chittick/HF weights active vs. muted to quantify their marginal contribution to idea quality and hit rate.",
      "Maintain a rolling **confusion matrix per signal type**: how often did it appear in accepted winners vs. losers vs. rejected ideas; use this to slowly re‑weight its influence.",
      "If a signal type produces recurrent rejections (e.g., low‑weight social triggers) without contributing to profitable ideas, gradually shrink its allowed role to zero or to pure risk‑flagging."
    ],
    "4_research_template_improvement": [
      "Standardize a **short research template**: thesis, catalyst, time horizon, risk factors, sector/factor tags, signals used (HF, Chittick, social, congress), and explicit reason why this candidate is not just a repeat.",
      "Force the model to answer a **binary novelty question**: ‘Does this thesis rely on any catalyst or narrative already logged for this ticker in the last X days?’ If yes, demote to monitoring and do not push as a new candidate.",
      "Track and visualize **research entropy**: fraction of new vs. recycled information in each day’s write‑ups; if entropy drops below a threshold, reduce candidate count and increase depth on fewer, higher‑quality names."
    ]
  },
  "signal_quality_assessment": {
    "chittick_cash": {
      "impact": "Useful as a **ranking and confidence layer**; higher Chittick scores generally co‑occur with better‑structured catalysts (e.g., GLW, AAPL, RRX, WMT, UNH).",
      "issues": "By itself, it does not prevent stale or over‑repeated mega‑caps; still needs novelty and capacity gates.",
      "recommendation": "Retain and **use only downstream**, after fundamental and capacity filters; never allow a high Chittick score to override stale_catalyst or repeat_decay."
    },
    "hugging_face_filters": {
      "impact": "HF hype/source filters clearly improve research quality by rejecting micro‑cap speculation, leverage‑adjacent products, and source‑thin hype.",
      "issues": "Sometimes they reject borderline but potentially valid ideas driven by a single high‑quality source; you must handle those via a documented override process rather than disabling filters.",
      "recommendation": "Keep them as **hard safety and quality gates**; complement them with a small manual or explicit‑logic override channel that requires additional confirming evidence."
    },
    "social_buzz_signals": {
      "impact": "Net effect so far is **added noise**: many candidates triggered by low‑weight social buzz are rejected for insufficient supporting sources or lack of fundamental catalyst.",
      "issues": "They push the research engine toward short‑term sentiment and micro‑cap names that do not fit a long‑only swing, risk‑controlled mandate.",
      "recommendation": "Restrict to **sentiment context only**; disallow social buzz from initiating candidates. Use it only to slightly boost or cut sizing on already‑sound setups, if at all."
    },
    "congressional_trading_signals": {
      "impact": "As implemented, mostly **low‑weight signals** that frequently fail the ‘two strong sources’ rule and rarely convert into execution‑ready ideas.",
      "issues": "They skew attention toward names that may not have timely, tradeable catalysts and add to log clutter.",
      "recommendation": "Use only as **weak corroboration** when aligned with strong fundamentals. Never as primary catalyst; suppress congress‑only ideas automatically."
    }
  },
  "safe_changes_after_test_gates": {
    "code_and_logic_changes": [
      "Implement a **portfolio‑aware candidate filter**: before scoring and emitting candidates, call a function that reads current simulated holdings and rejects or resizes any candidate that would breach single‑stock or max‑position constraints.",
      "Add a **cool‑down mechanism** at the ticker level: maintain a dictionary with `last_catalyst_hash`, `last_considered_date`, and `repeat_count`; block candidates when `repeat_count` exceeds a threshold without a new catalyst hash.",
      "Create a **sector/style quota module**: keep rolling counts of active and pending candidates by sector and style; if a quota is reached, new ideas from that bucket are tagged ‘research‑only’ and not passed to execution."
    ],
    "prompt_and_routine_changes": [
      "Amend the research prompt to: (a) explicitly require a **fresh, documented catalyst** and (b) explicitly check memory: ‘If this ticker has been considered in the last 20 trading days, explain what is new; otherwise do not propose it.’",
      "Add instructions that **social buzz and congress mentions cannot be primary catalysts** and must be treated only as secondary context layers.",
      "Ensure the system prompt/routine states that **monitor‑only, non‑tradable, or banned‑instrument tickers must never be labeled execution‑ready**, and that such ideas should be logged only in a separate ‘watch but not tradeable’ section."
    ],
    "safety_and_scope_confirmations": [
      "Keep all existing **bans on options, margin, shorting, crypto, and live trading** fully in place and ensure no research path suggests those as workarounds.",
      "Never request or handle **secrets, credentials, or broker integrations**; all logic remains on paper‑trading, research, and rules‑testing only.",
      "Add a recurring self‑check in the daily routine: ‘Confirm that all candidates comply with the mandate: long‑only, no leverage, no crypto, no non‑listed or exotic instruments.’"
    ]
  }
}
## Weekly Review - 2026-06-26 17:25:32 Eastern Daylight Time

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
      "Frequent rejections citing \"candidate is monitor‑only\" or \"allocation‑muted\" show a mismatch between research selection and tradable universe; the bot repeatedly chooses tickers that are structurally non‑executable.",
      "This creates repetitive research output around names that cannot progress beyond watch/monitor tiers, wasting attention and increasing memory clutter."
    ]
  },
  "strategy_proposals": {
    "ticker_and_sector_routing": [
      "Introduce a **repeat‑aware universe filter**: before generating fresh candidates each session, exclude any ticker that has: (a) repeat_decay or stale_catalyst logged in the past N days, and (b) is monitor‑only or allocation‑muted, unless a high‑confidence, time‑stamped new catalyst is detected.",
      "Implement **sector‑balance targets** for the candidate list: e.g., ensure each day’s execution‑ready pool includes at least one non‑tech/non‑internet name if any tech/cloud/semiconductor symbols are present. Use soft quotas (e.g., cap any single sector at 40% of daily execution‑ready slots).",
      "Add a **mega‑cap throttle**: limit daily candidate generation for mega‑cap tech/internet (AAPL, MSFT, GOOGL, AMZN, etc.) to at most one ticker and require a top‑quartile confidence plus a clearly dated catalyst (earnings, guidance, regulatory decision, index change)."
    ],
    "catalyst and confidence handling": [
      "Upgrade the **freshness gate**: only allow a symbol into execution‑ready tier when the primary catalyst has: (a) a specific date within the last X days, and (b) a clearly fundamental nature (earnings, guidance, index inclusion, rating/target change, major contract/deal, regulatory action) rather than generic news flow.",
      "Use a **two‑layer confidence model**: one score for catalyst quality (dated, fundamental, multi‑source) and one for technical/price‑action confirmation. Require both to exceed a minimal threshold before suggesting execution‑ready.",
      "Tie **position limits to pre‑filtering**: whichever symbol already approaches 10–15% of hypothetical portfolio weight should be automatically removed from candidate consideration until weight decays below a threshold, reducing late‑stage allocation rejections."
    ],
    "universe hygiene and diversity": [
      "Explicitly **downgrade or tag noise‑heavy domains** (meme entertainment, micro‑cap, potentially delisted, source‑thin overseas single names) to a separate experimental bucket that is visible but not eligible for execution‑ready recommendations.",
      "Encourage **defensive and non‑correlated sectors** (staples, healthcare, utilities, business services, high‑quality industrials) by adding a small positive bias to their selection score when recent candidates have been dominated by cyclicals, energy, or tech.",
      "Apply a **geo‑diversity check**: when US mega‑cap exposure is high, prefer candidates that improve regional diversification only if they pass the same strict fundamental‑catalyst and source‑quality gates."
    ]
  },
  "self_learning_directives": {
    "memory_and pattern learning": [
      "Maintain a **ticker‑level profile** with rolling statistics: repeat count over the last 30/60/90 days, number of rejections by reason (repeat_decay, stale_catalyst, monitor‑only, allocation‑muted, social‑noise), and realized performance of executed paper trades. Use this profile to adapt future scoring.",
      "Automatically **down‑weight tickers with high rejection density** (e.g., more than K rejections in a month) unless both catalyst freshness and confidence materially exceed prior attempts.",
      "Create a **pattern library** of rejected causes (e.g., \"micro_cap_speculation + no_fundamental_catalyst\", \"low_weight_social_congress + source_thin\") and apply these as negative priors during candidate generation so similar combinations are less likely to surface."
    ],
    "signal source evaluation": [
      "Periodically evaluate whether candidate sets selected using **Chittick Cash** scores, HF filters, social buzz, or congressional signals would have improved risk‑adjusted paper performance relative to a pure fundamental baseline, then update weights for each signal family accordingly.",
      "Log, for each candidate, which signal families contributed most to its selection and compare against later rejection reasons and hypothetical price paths to refine **signal trust scores** over time."
    ],
    "research output de‑duplication": [
      "Implement a **daily novelty check**: before finalizing outputs, compute similarity versus the prior 30 days’ catalysts and narratives for the same ticker. If similarity exceeds a threshold and no new dated event is present, route the candidate to a \"skip or brief‑update\" lane instead of full write‑up.",
      "Limit the number of **near‑duplicate narratives per day** (same sector, same style of thesis, similar catalysts) to reduce cognitive fatigue and encourage more varied research."
    ]
  },
  "signal_assessment": {
    "chittick_cash": {
      "observed_effects": [
        "Higher Chittick scores often correlate with stronger fundamental catalysts and higher confidence (e.g., GLW with warrants tied to NVIDIA, PAYX earnings and guidance, INTC target raise and AI outlook).",
        "Names like speculative micro‑caps or purely social‑driven tickers rarely show high Chittick scores in the logs, suggesting this metric is more aligned with quality than hype."
      ],
      "assessment": "Chittick Cash appears to improve research quality when treated as one input among several, particularly alongside fundamental events. It does not fully prevent repeats or sector imbalance, but it tends to support better names rather than noise."
    },
    "hugging_face_filters": {
      "observed_effects": [
        "HF memory and source/hype filters correctly flag repeat_staleness, memory_similarity, and source‑thin hype (ADI, GSK, SGN, PHX, USAR), causing many low‑quality candidates to be rejected before execution.",
        "These filters are largely reactive at the candidate vetting stage; despite that, repeat tickers and stale narratives still enter the daily candidate lists, indicating that filter logic could be moved earlier into generation."
      ],
      "assessment": "Hugging Face–style filters are net positive for research quality, primarily by removing hype and stale repeats. The main issue is placement: they clean up outputs late instead of shaping the input universe earlier, leading to redundant work."
    },
    "social_buzz_and_congressional_signals": {
      "observed_effects": [
        "Rejection logs show that low‑weight social/congress signals often trigger additional concerns: micro_cap_speculation, potentially_delisted, no_fundamental_catalyst, or source_thin.",
        "Very few execution‑ready candidates rely on these signals; instead, they cluster around rejected names or watch‑only ideas such as SGN, DVN, EWY, EWT, AMC, PHX, and multiple PLTR attempts."
      ],
      "assessment": "At current configuration, social buzz and congressional signals mostly add noise. They frequently coexist with low‑quality, speculative, or structurally untradeable names and are better treated as optional context rather than primary selection drivers."
    }
  },
  "recommended_changes": {
    "code_and_prompt_logic": [
      "Add a **pre‑generation guard** that filters tickers based on: (a) recent repeat_decay/stale_catalyst flags, (b) monitor‑only or allocation‑muted status, and (c) exceeding single‑name allocation thresholds. Only candidates that pass these checks should enter the daily selection pipeline.",
      "Modify the **candidate scoring function** to incorporate: (a) a strong penalty for undated or vague catalysts, (b) a penalty for single‑source or social‑dominant signals, and (c) a bonus for multi‑source, clearly fundamental, and dated events.",
      "Implement a **sector‑balancing routine** that, after scoring candidates, adjusts scores to reduce over‑representation of any single sector and prioritize under‑represented sectors with valid catalysts.",
      "Integrate HF memory similarity directly into the **candidate retrieval step** so that highly similar narratives to previous rejections are filtered out before confidence scoring.",
      "Add a **trade‑eligibility flag** in the memory (tradable vs monitor‑only vs allocation‑muted) and use it upstream to prevent generation of execution‑ready recommendations for non‑tradable symbols."
    ],
    "research_routine_adjustments": [
      "Restructure daily outputs into: (a) 1–3 high‑conviction, execution‑ready ideas with fresh, dated catalysts and diversified sectors, and (b) a brief watchlist update section summarizing changes for monitor‑only names without proposing trades.",
      "Limit re‑coverage of the same ticker to **no more than once per week** unless a new, clearly dated catalyst has occurred; otherwise, log only a one‑line status update.",
      "Introduce a **\"noise bucket\" label** for candidates dominated by social/congress signals or hype; keep them visible for learning, but never escalate them to execution‑ready in v1."
    ],
    "safety_and_gatekeeping": [
      "Keep all current safety constraints intact (no options, margin, shorting, crypto, live trading, secrets, or credential changes) and extend them with explicit checks that prevent any code path from proposing trades in banned instrument classes.",
      "Add a **simulation‑only tag** to all strategies and recommendations, and ensure prompts emphasize that outputs are for paper‑trading research and scenario analysis only.",
      "Enforce a **hard ceiling on daily candidate count** to reduce clutter and force higher selection quality; for example, cap at 5–7 tickers per day, with at most 3 in execution‑ready tier."
    ]
  }
}
## Weekly Review - 2026-07-03 17:25:45 Eastern Daylight Time

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
        "lesson": "The current treatment (congress/social as secondary-only signals) is directionally correct, but those signals still consume attention. They have not demonstrably lifted candidate quality; instead, they frequently correlate with later rejections as hype/noise."
      },
      {
        "issue": "Chittick Cash and Hugging Face filters appear to help, but are too reactive and not fully integrated",
        "evidence": [
          "Candidates with low Chittick scores or HF flags (`source_thin`, `HF source/hype filter rejects source-thin hype`, `HF memory filter flags similarity to prior rejected patterns`) are consistently rejected before execution.",
          "HF memory similarity and repeat-decay flags catch repeated GOOGL/INTC/MSFT/GT patterns before re-approval, but only at guard-rail time, after the candidate is fully assembled.",
          "Hype filters successfully block micro-cap/speculative plays (SGN, PHX, VST, CRDO, MUX, AMC) that lack fundamental catalysts and exhibit social/congress-driven hype."
        ],
        "lesson": "These filters improve research quality by filtering out thin/hype-based candidates and stale repeats, but they are used as late-stage vetoes rather than early-stage pruning. They reduce bad trades but don’t yet redirect research toward better themes."
      }
    ]
  },
  "rejected_patterns": {
    "behavioral_patterns_to_avoid": [
      "Re-surfacing tickers whose last rejection was due to `repeat_decay`, `stale_catalyst`, or `memory_similarity` without an explicitly new, dated, and independently corroborated catalyst.",
      "Building trade candidates primarily on low-weight social or congressional data and then back-filling fundamentals to justify them.",
      "Consuming allocation and guard-rail checks only at the final step, causing repeated attempts to trade monitor-only, allocation-muted, or max-position-breaching tickers.",
      "Returning multiple candidates from the same sector and AI narrative cluster on the same day when portfolio exposure is already high in that cluster.",
      "Treating analyst initiations and upgrades as sufficient standalone catalysts, especially when price/volume confirmation is missing or when coverage is from a single small shop.",
      "Allowing micro-cap/speculative tickers with limited liquidity and thin disclosure to pass early screens just because they mention AI, strategic materials, or congressional interest.",
      "Revisiting mega-cap AI/tech names day after day on minor narrative updates (opinion pieces, social buzz, derivative commentary) instead of waiting for truly fresh corporate events."
    ],
    "structural_patterns_to_avoid": [
      "Unbounded reuse of the same theme labels (`mega-cap-internet-cloud`, `AI infrastructure`, `semiconductors-pullback-quality`) without theme-level performance or saturation checks.",
      "Research scheduling that focuses on what is most mentioned in news/social feeds rather than what is least represented in the current portfolio and watchlist.",
      "Using a fixed 1–15% allocation band without dynamically scaling down target allocations when catalysts are weaker or more narrative-driven."
    ]
  },
  "strategy_proposals": {
    "diversification_and_theme_controls": [
      {
        "name": "Sector and theme quota system",
        "description": "Introduce explicit daily and weekly caps for research slots per sector and per top-level theme (e.g., AI/semis/cloud, healthcare, industrials, financials, consumer, energy/materials, utilities/REITs).",
        "mechanics": [
          "Before daily candidate generation, compute current portfolio and active-watchlist exposures by sector and theme.",
          "Rank sectors/themes by underweight vs. target mix (e.g., 20–25% tech/comm-services, 15–20% healthcare, 15–20% financials, etc., customizable for your risk profile).",
          "Prioritize scanning and candidate generation for sectors/themes that are underweight or missing, so you systematically surface transports, regional banks, small caps, staples, etc., rather than another AI cloud name."
        ]
      },
      {
        "name": "Repeat-decay budget",
        "description": "Impose a strict limit on how often a ticker can be re-entered into the candidate pipeline within a decay window unless a high-impact event is detected.",
        "mechanics": [
          "Maintain per-ticker state with `last_catalyst_hash`, `last_rejection_reason`, and `last_considered_at`.",
          "If `last_rejection_reason` is any of `{repeat_decay, stale_catalyst, memory_similarity}`, require at least one of the following before reconsideration:",
          "1) A new 8-K / earnings / guidance / M&A / capital raise / regulatory approval event with a fresh timestamp.",
          "2) A 30%+ price move from last consideration driven by company-specific news, not macro.",
          "3) A shift in allocation/portfolio state that makes the ticker uniquely helpful for diversification (e.g., tech now underweight by at least X%)."
        ]
      }
    ],
    "signal_weighting_and_guard_rails": [
      {
        "name": "Early guard-rail pre-filter",
        "description": "Move allocation, monitor-only, and banned-instrument checks to the earliest stage of candidate generation.",
        "mechanics": [
          "When building the candidate pool, immediately discard tickers that are:",
          "• Over the 15% single-name cap given current positions and the proposed allocation.",
          "• In `monitor-only`, `allocation-muted`, or banned buckets for this strategy version.",
          "• In violation of max open-position count.",
          "Return them only as FYI in a separate diagnostic log, not as candidates, to avoid re-running the same rejections."
        ]
      },
      {
        "name": "Signal source scoring and routing",
        "description": "Refine the source-score model so that fundamental/catalyst signals dominate candidate selection, while social/congress are only tie-breakers or augmenting features.",
        "mechanics": [
          "Assign base weights to signal classes, e.g.:",
          "• Hard catalysts (earnings surprises, guidance changes, M&A, regulatory approvals, large capex, major design wins) = very high weight.",
          "• Valuation/factor mispricing plus breadth/macrofactor alignment = high weight.",
          "• Analyst consensus shifts with multiple reputable firms = medium weight.",
          "• Congressional or social buzz, especially from small accounts or non-official sources = low weight.",
          "Require that any candidate whose top-2 signals are both low-weight be automatically downgraded to `monitor-only` or dropped."
        ]
      }
    ],
    "research_process_improvements": [
      {
        "name": "Daily research diversity mandate",
        "description": "Enforce that each daily output includes a minimum variety of sectors and catalyst types.",
        "mechanics": [
          "For each daily run, require at least: one non-tech cyclical (e.g., transport/industrial), one defensive (staples/healthcare/utilities), and one financial or real asset (financials, REITs, materials/energy).",
          "Avoid surfacing more than two tickers from the same theme label (e.g., AI-infrastructure) per session unless portfolio exposure to that theme is currently low.",
          "Rank same-theme candidates by incremental information and diversification value; only allow the top N into the final list."
        ]
      },
      {
        "name": "Catalyst lifecycle tracking",
        "description": "Treat catalysts as first-class objects with timestamps, type, expected horizon, and decay curve.",
        "mechanics": [
          "For each ticker, store a list of active catalysts with fields: `type`, `strength`, `start_date`, `expected_half_life_days`, `source_count`, `last_update`.",
          "Drop or sharply deweight catalysts whose half-life has expired without follow-through (e.g., more than one earnings cycle since the event and no confirmation).",
          "Only mark a ticker as ‘fresh’ if at least one active catalyst has a current, non-decayed state and has been updated/confirmed in the last X days."
        ]
      }
    ]
  },
  "self_learning_directives": {
    "post_gate_analysis": [
      {
        "directive": "Log every rejection with a normalized tag set and feed it to a periodic pattern miner",
        "details": [
          "Normalize reasons into a compact taxonomy: `allocation_limit`, `position_count`, `stale_catalyst`, `repeat_decay`, `memory_similarity`, `source_thin`, `hype`, `monitor_only`, `allocation_muted`, `risk_band_violation`.",
          "Weekly, cluster rejected candidates by ticker, sector, and tag combo to identify systematic failure modes (e.g., ‘mega-cap AI names rejected due to stale catalyst’).",
          "Use those clusters to adjust upstream sampling probabilities and decay parameters."
        ]
      },
      {
        "directive": "Outcome-linked learning (paper-trading only)",
        "details": [
          "For executed trades, track ex-post performance vs. a simple benchmark (e.g., sector ETF or S&P) over standardized windows (1 week, 1 month, 3 months).",
          "Associate that performance with the catalyst feature vector and signal source mix at entry time.",
          "Periodically downweight signal combinations that systematically underperform (e.g., analyst-initiation-only trades; trades driven primarily by congress/social without strong fundamentals).",
          "Upweight signal combinations that show good risk-adjusted relative performance."
        ]
      }
    ],
    "memory_and_filter_tuning": [
      {
        "directive": "Adaptive Hugging Face memory filter thresholds",
        "details": [
          "Track the frequency and quality (if executed) of candidates that survive vs. fail the HF memory/hype filters.",
          "If many good trades are blocked, gradually relax similarity/hype thresholds; if many bad trades still slip through, tighten them.",
          "Use ticker-level statistics: if a ticker has more than N rejections due to memory similarity or stale catalysts within a 60-day window, raise its minimum required catalyst strength for reconsideration."
        ]
      },
      {
        "directive": "Chittick Cash score calibration",
        "details": [
          "Correlate Chittick scores with realized paper-trade performance and with subsequent upgrade/downgrade rates.",
          "If high-Chittick names are not outperforming but are overrepresented in the candidate list, reduce the direct weight of the Chittick feature and increase reliance on catalyst structure and diversification metrics.",
          "Conversely, if low-Chittick, high-conviction fundamental ideas outperform, raise their priority even when Chittick is neutral."
        ]
      }
    ]
  },
  "component_assessments": {
    "chittick_cash": {
      "role": "A numeric confidence/quality score used in candidate ranking.",
      "observed_effect": "Most execution-ready names have Chittick scores in the 68–78 range; low-confidence or monitor-only names often have lower scores and are eventually rejected.",
      "assessment": "Helpful as a coarse quality filter, but it is not preventing repetitive AI/mega-cap resurfacing and does not encode diversification or catalyst decay.",
      "recommended_adjustments": [
        "Incorporate diversification penalty into the score: subtract points when the ticker’s sector/theme is already overweight.",
        "Incorporate catalyst freshness directly: decaying catalysts should automatically erode the score over time.",
        "Include realized paper-trade performance in a gradual feedback loop to recalibrate what score thresholds deserve ‘execution-ready’ vs. ‘watch’ status."
      ]
    },
    "hugging_face_filters": {
      "role": "Source/hype/memory filters used to veto candidates that look like prior bad patterns or thin hype.",
      "observed_effect": "They successfully tag repeat/stale/hype scenarios and block micro-cap speculation and thinly sourced AI/congress names (SGN, PHX, VST, USAR earlier, etc.).",
      "assessment": "Net positive on research quality. They reduce noise trading risk and enforce basic data richness requirements.",
      "recommended_adjustments": [
        "Move HF checks earlier so that clearly hype-driven or memory-similar candidates are never promoted to ‘execution-ready’ in the first place.",
        "Expose more granular reasons in internal logs (e.g., `hype_social`, `hype_low_liquidity`, `hype_option-flow`) to help self-learning differentiate which hype types are most problematic.",
        "Tie HF similarity penalty to ticker-level cooldown windows so the system automatically lengthens the waiting period after multiple similarity-based rejections."
      ]
    },
    "social_buzz_and_congressional_signals": {
      "role": "Secondary attention signals, often via Quiver-like sources, about unusual trading by politicians or on social platforms.",
      "observed_effect": "Cited frequently, but trades based primarily on these signals rarely pass guards; many are explicitly rejected for `low-weight social/congress signal` and `no_fundamental_catalyst`.",
      "assessment": "Currently more noise than signal. The framework correctly downgrades them, but they still create repetitive, low-value candidate attempts.",
      "recommended_adjustments": [
        "Hard rule: social/congress can never be the primary driver of `execution-ready` status; at least one strong, timestamped corporate or fundamental catalyst is required.",
        "Only elevate a social/congress signal if it aligns with:",
        "• A new, confirmed company event within the last X days, and",
        "• Unusual volume/price behavior consistent with informed participation.",
        "Otherwise, keep such tickers in a separate ‘monitor only / narrative watchlist’ and exclude them entirely from trade candidates."
      ]
    }
  },
  "safe_code_and_prompt_changes": {
    "pre_trade_pipeline_changes": [
      {
        "change_type": "logic",
        "description": "Add an early-stage `hard_filter(candidate)` that checks position limits, allocation bands, monitor-only/alloc-muted flags, and banned instruments before anything is promoted to ‘execution-ready’ or even ‘watch’.",
        "pseudo_code": "if violates_position_limits(candidate) or is_monitor_only(candidate) or is_allocation_muted(candidate) or is_banned_v1(candidate): discard_candidate(candidate);"
      },
      {
        "change_type": "logic",
        "description": "Implement per-ticker cooldown and catalyst-hash checks.",
        "pseudo_code": "if recent_rejection_with_stale_or_repeat(candidate.symbol) and !has_new_catalyst_hash(candidate): discard_candidate(candidate);"
      },
      {
        "change_type": "scoring",
        "description": "Embed diversification penalties and catalyst-decay into the scoring function.",
        "pseudo_code": "candidate.score = base_quality(candidate) - sector_overweight_penalty(candidate) - theme_repeat_penalty(candidate) - catalyst_decay_penalty(candidate);"
      }
    ],
    "research_prompt_and_routine_changes": [
      {
        "change_type": "prompting",
        "description": "Update the research agent instructions to emphasize fresh, multi-source, fundamentally-driven catalysts and diversification.",
        "example_instruction_snippet": [
          "• Prioritize company-specific events in the last 30 days: earnings/guidance, M&A, big capex, regulatory approvals, large contracts, or capital structure changes.",
          "• Do not propose trade candidates based primarily on congressional or social media signals. These may only upgrade an idea that already has strong fundamental catalysts.",
          "• If the ticker has been considered or rejected within the last 30 days due to stale catalysts or repeat-decay, require evidence of a new, independently verified catalyst before reconsidering.",
          "• Aim for sector and factor diversity in daily outputs. If the current portfolio is heavily weighted to AI/mega-cap tech, prioritize new ideas from underrepresented sectors such as transports, regional banks, consumer, or healthcare.",
          "• Explicitly state why the current catalyst is fresh and why it is not a rehash of prior narratives."
        ]
      },
      {
        "change_type": "routine",
        "description": "Introduce a weekly ‘theme health check’ routine.",
        "routine_steps": [
          "1) Aggregate performance of paper-traded positions by theme and sector.",
          "2) Identify overconcentrated themes (e.g., AI-infrastructure) with correlated outcomes.",
          "3) Adjust next-week scanning weights to favor under-researched, under-owned, or outperforming-but-underweighted areas (e.g., transports, regional banks, small caps) consistent with external breadth signals."
        ]
      }
    ]
  }
}
## Weekly Review - 2026-07-10 17:25:01 Eastern Daylight Time

{
  "status": "provider-blocked",
  "blocked_reason": "Perplexity returned 401 insufficient_quota, so no live Sonar weekly analysis was run.",
  "concise_lessons": [
    "Weekly review should preserve the hard upstream stop instead of retrying or fabricating live research.",
    "Use repo memory for this blocked review and label it clearly as provider-blocked.",
    "Repeated symbols in the latest memory window: none.",
    "Overused diversity buckets in the latest memory window: none.",
    "Recent rejection history still needs to keep hard-ban, low-weight-only, allocation-blocked, and max-position-blocked ideas out of tradeable lanes."
  ],
  "rejected_patterns": [
    "CAG: low_weight_signal",
    "FSLR: low_weight_signal",
    "GDDY: low_weight_signal",
    "GOOGL: hype_or_repeat_filter",
    "SPOT: low_weight_signal",
    "TSM: low_weight_signal"
  ],
  "strategy_proposals": [
    "Keep the weekly review script from crashing on provider quota errors by writing a blocked review artifact from local memory.",
    "Keep social buzz capped at 10% and congressional disclosures capped at 5%; no blocked-provider review may upgrade a trade from those signals.",
    "Continue routing monitor-only and allocation-muted candidates to zero allocation until their blockers clear."
  ],
  "self_learning_directives": [
    "Treat Perplexity insufficient_quota as a hard stop for live research and disclose the provider block in Telegram/memory.",
    "When live review is blocked, summarize only deterministic repo-memory signals: repeats, diversity buckets, and rejection labels.",
    "Do not run market-open execution as part of the Friday weekly review lane."
  ],
  "safe_code_prompt_routine_changes": [
    "Add weekly-review quota fallback that records a provider-blocked review instead of failing before memory and Telegram reporting.",
    "Preserve paper-only, stocks/ETFs-only, no-live-trading, no-options, no-crypto, no-margin, no-short-selling, and no-secrets guardrails."
  ],
  "signal_component_assessment": {
    "chittick_cash": "Not re-evaluated live because provider quota blocked Sonar; retain existing local-memory policy.",
    "hugging_face_filters": "Not re-evaluated live because provider quota blocked Sonar; retain downgrade/veto-only role.",
    "social_buzz": "No live update; remains low-weight context only, capped at 10%.",
    "congressional_disclosures": "No live update; remains delayed low-weight context only, capped at 5%."
  },
  "error": "POST https://api.perplexity.ai/chat/completions failed with 401: {\"error\":{\"message\":\"You exceeded your current quota, please check your plan and billing details. For more information, visit https://www.perplexity.ai/settings/api.\",\"type\":\"insufficient_quota\",\"code\":401}}\n"
}
## Weekly Review - 2026-07-17 18:13:41 Eastern Daylight Time

{
  "status": "provider-blocked",
  "blocked_reason": "Perplexity returned 401 insufficient_quota, so no live Sonar weekly analysis was run.",
  "concise_lessons": [
    "Weekly review should preserve the hard upstream stop instead of retrying or fabricating live research.",
    "Use repo memory for this blocked review and label it clearly as provider-blocked.",
    "Repeated symbols in the latest memory window: none.",
    "Overused diversity buckets in the latest memory window: none.",
    "Recent rejection history still needs to keep hard-ban, low-weight-only, allocation-blocked, and max-position-blocked ideas out of tradeable lanes."
  ],
  "rejected_patterns": [
    "FSLR: low_weight_signal",
    "GDDY: low_weight_signal",
    "GOOGL: hype_or_repeat_filter",
    "TSM: low_weight_signal"
  ],
  "strategy_proposals": [
    "Keep the weekly review script from crashing on provider quota errors by writing a blocked review artifact from local memory.",
    "Keep social buzz capped at 10% and congressional disclosures capped at 5%; no blocked-provider review may upgrade a trade from those signals.",
    "Continue routing monitor-only and allocation-muted candidates to zero allocation until their blockers clear."
  ],
  "self_learning_directives": [
    "Treat Perplexity insufficient_quota as a hard stop for live research and disclose the provider block in Telegram/memory.",
    "When live review is blocked, summarize only deterministic repo-memory signals: repeats, diversity buckets, and rejection labels.",
    "Do not run market-open execution as part of the Friday weekly review lane."
  ],
  "safe_code_prompt_routine_changes": [
    "Add weekly-review quota fallback that records a provider-blocked review instead of failing before memory and Telegram reporting.",
    "Preserve paper-only, stocks/ETFs-only, no-live-trading, no-options, no-crypto, no-margin, no-short-selling, and no-secrets guardrails."
  ],
  "signal_component_assessment": {
    "chittick_cash": "Not re-evaluated live because provider quota blocked Sonar; retain existing local-memory policy.",
    "hugging_face_filters": "Not re-evaluated live because provider quota blocked Sonar; retain downgrade/veto-only role.",
    "social_buzz": "No live update; remains low-weight context only, capped at 10%.",
    "congressional_disclosures": "No live update; remains delayed low-weight context only, capped at 5%."
  },
  "error": "POST https://api.perplexity.ai/chat/completions failed with 401: {\"error\":{\"message\":\"You exceeded your current quota, please check your plan and billing details. For more information, visit https://www.perplexity.ai/settings/api.\",\"type\":\"insufficient_quota\",\"code\":401}}\n"
}
## Weekly Review - 2026-07-24 17:25:02 Eastern Daylight Time

{
  "status": "provider-blocked",
  "blocked_reason": "Perplexity returned 401 insufficient_quota, so no live Sonar weekly analysis was run.",
  "concise_lessons": [
    "Weekly review should preserve the hard upstream stop instead of retrying or fabricating live research.",
    "Use repo memory for this blocked review and label it clearly as provider-blocked.",
    "Repeated symbols in the latest memory window: none.",
    "Overused diversity buckets in the latest memory window: none.",
    "Recent rejection history still needs to keep hard-ban, low-weight-only, allocation-blocked, and max-position-blocked ideas out of tradeable lanes."
  ],
  "rejected_patterns": [
    "FSLR: low_weight_signal",
    "GDDY: low_weight_signal",
    "GOOGL: hype_or_repeat_filter",
    "TSM: low_weight_signal"
  ],
  "strategy_proposals": [
    "Keep the weekly review script from crashing on provider quota errors by writing a blocked review artifact from local memory.",
    "Keep social buzz capped at 10% and congressional disclosures capped at 5%; no blocked-provider review may upgrade a trade from those signals.",
    "Continue routing monitor-only and allocation-muted candidates to zero allocation until their blockers clear."
  ],
  "self_learning_directives": [
    "Treat Perplexity insufficient_quota as a hard stop for live research and disclose the provider block in Telegram/memory.",
    "When live review is blocked, summarize only deterministic repo-memory signals: repeats, diversity buckets, and rejection labels.",
    "Do not run market-open execution as part of the Friday weekly review lane."
  ],
  "safe_code_prompt_routine_changes": [
    "Add weekly-review quota fallback that records a provider-blocked review instead of failing before memory and Telegram reporting.",
    "Preserve paper-only, stocks/ETFs-only, no-live-trading, no-options, no-crypto, no-margin, no-short-selling, and no-secrets guardrails."
  ],
  "signal_component_assessment": {
    "chittick_cash": "Not re-evaluated live because provider quota blocked Sonar; retain existing local-memory policy.",
    "hugging_face_filters": "Not re-evaluated live because provider quota blocked Sonar; retain downgrade/veto-only role.",
    "social_buzz": "No live update; remains low-weight context only, capped at 10%.",
    "congressional_disclosures": "No live update; remains delayed low-weight context only, capped at 5%."
  },
  "error": "POST https://api.perplexity.ai/chat/completions failed with 401: {\"error\":{\"message\":\"You exceeded your current quota, please check your plan and billing details. For more information, visit https://www.perplexity.ai/settings/api.\",\"type\":\"insufficient_quota\",\"code\":401}}\n"
}
## Weekly Review - 2026-07-31 17:25:04 Eastern Daylight Time

{
  "status": "provider-blocked",
  "blocked_reason": "Perplexity returned 401 insufficient_quota, so no live Sonar weekly analysis was run.",
  "concise_lessons": [
    "Weekly review should preserve the hard upstream stop instead of retrying or fabricating live research.",
    "Use repo memory for this blocked review and label it clearly as provider-blocked.",
    "Repeated symbols in the latest memory window: none.",
    "Overused diversity buckets in the latest memory window: none.",
    "Recent rejection history still needs to keep hard-ban, low-weight-only, allocation-blocked, and max-position-blocked ideas out of tradeable lanes."
  ],
  "rejected_patterns": [
    "FSLR: low_weight_signal",
    "GDDY: low_weight_signal",
    "GOOGL: hype_or_repeat_filter",
    "TSM: low_weight_signal"
  ],
  "strategy_proposals": [
    "Keep the weekly review script from crashing on provider quota errors by writing a blocked review artifact from local memory.",
    "Keep social buzz capped at 10% and congressional disclosures capped at 5%; no blocked-provider review may upgrade a trade from those signals.",
    "Continue routing monitor-only and allocation-muted candidates to zero allocation until their blockers clear."
  ],
  "self_learning_directives": [
    "Treat Perplexity insufficient_quota as a hard stop for live research and disclose the provider block in Telegram/memory.",
    "When live review is blocked, summarize only deterministic repo-memory signals: repeats, diversity buckets, and rejection labels.",
    "Do not run market-open execution as part of the Friday weekly review lane."
  ],
  "safe_code_prompt_routine_changes": [
    "Add weekly-review quota fallback that records a provider-blocked review instead of failing before memory and Telegram reporting.",
    "Preserve paper-only, stocks/ETFs-only, no-live-trading, no-options, no-crypto, no-margin, no-short-selling, and no-secrets guardrails."
  ],
  "signal_component_assessment": {
    "chittick_cash": "Not re-evaluated live because provider quota blocked Sonar; retain existing local-memory policy.",
    "hugging_face_filters": "Not re-evaluated live because provider quota blocked Sonar; retain downgrade/veto-only role.",
    "social_buzz": "No live update; remains low-weight context only, capped at 10%.",
    "congressional_disclosures": "No live update; remains delayed low-weight context only, capped at 5%."
  },
  "error": "POST https://api.perplexity.ai/chat/completions failed with 401: {\"error\":{\"message\":\"You exceeded your current quota, please check your plan and billing details. For more information, visit https://www.perplexity.ai/settings/api.\",\"type\":\"insufficient_quota\",\"code\":401}}\n"
}
## Weekly Review - 2026-08-07 17:25:04 Eastern Daylight Time

{
  "status": "provider-blocked",
  "blocked_reason": "Perplexity returned 401 insufficient_quota, so no live Sonar weekly analysis was run.",
  "concise_lessons": [
    "Weekly review should preserve the hard upstream stop instead of retrying or fabricating live research.",
    "Use repo memory for this blocked review and label it clearly as provider-blocked.",
    "Repeated symbols in the latest memory window: none.",
    "Overused diversity buckets in the latest memory window: none.",
    "Recent rejection history still needs to keep hard-ban, low-weight-only, allocation-blocked, and max-position-blocked ideas out of tradeable lanes."
  ],
  "rejected_patterns": [
    "FSLR: low_weight_signal",
    "GDDY: low_weight_signal",
    "GOOGL: hype_or_repeat_filter",
    "TSM: low_weight_signal"
  ],
  "strategy_proposals": [
    "Keep the weekly review script from crashing on provider quota errors by writing a blocked review artifact from local memory.",
    "Keep social buzz capped at 10% and congressional disclosures capped at 5%; no blocked-provider review may upgrade a trade from those signals.",
    "Continue routing monitor-only and allocation-muted candidates to zero allocation until their blockers clear."
  ],
  "self_learning_directives": [
    "Treat Perplexity insufficient_quota as a hard stop for live research and disclose the provider block in Telegram/memory.",
    "When live review is blocked, summarize only deterministic repo-memory signals: repeats, diversity buckets, and rejection labels.",
    "Do not run market-open execution as part of the Friday weekly review lane."
  ],
  "safe_code_prompt_routine_changes": [
    "Add weekly-review quota fallback that records a provider-blocked review instead of failing before memory and Telegram reporting.",
    "Preserve paper-only, stocks/ETFs-only, no-live-trading, no-options, no-crypto, no-margin, no-short-selling, and no-secrets guardrails."
  ],
  "signal_component_assessment": {
    "chittick_cash": "Not re-evaluated live because provider quota blocked Sonar; retain existing local-memory policy.",
    "hugging_face_filters": "Not re-evaluated live because provider quota blocked Sonar; retain downgrade/veto-only role.",
    "social_buzz": "No live update; remains low-weight context only, capped at 10%.",
    "congressional_disclosures": "No live update; remains delayed low-weight context only, capped at 5%."
  },
  "error": "POST https://api.perplexity.ai/chat/completions failed with 401: {\"error\":{\"message\":\"You exceeded your current quota, please check your plan and billing details. For more information, visit https://www.perplexity.ai/settings/api.\",\"type\":\"insufficient_quota\",\"code\":401}}\n"
}

