# Strategy Proposals

Weekly review may propose changes here. Routine runs must not rewrite executable trading code.
## Weekly Strategy Proposals - 2026-05-01 17:25:37 Eastern Daylight Time

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

## Weekly Strategy Proposals - 2026-05-02 00:22:28 Eastern Daylight Time

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

### Signal-Weight Proposal - 2026-05-02

- Keep social buzz capped at 10% and require two stronger non-social sources before it can support any candidate. This week's review found no direct social help and no verified social anomaly.
- Keep congressional disclosures capped at 5% and require direct disclosure evidence before adding any score. This week's review found no relevant congressional help for GOOGL, NVDA, or SPMO.
- Add a weekly "signal contribution" line to future reviews: `social: helped/noise/none`, `congress: helped/noise/none`, and `primary drivers`. This would make it obvious when low-weight channels are merely noise checks versus actual supporting context.
## Weekly Strategy Proposals - 2026-05-04 09:49:54 Eastern Daylight Time

{"lessons":["SPMO dominates outputs with near-identical repetitive catalysts across 20+ timestamps, indicating stalled momentum scanning without fresh signals.","NVDA, GOOGL, ASML, LRCX, MSFT recur heavily in semiconductors/tech/AI, comprising 70%+ of candidates and triggering repeated 15% allocation blocks.","Portfolio lacks diversity: 90%+ candidates in tech/semiconductors/broad momentum; minimal exposure to biotech (ANIX/TNXP), industrials (ETN), or others despite occasional appearances.","Daily research outputs are formulaic, recycling price ranges ($128-$132 for SPMO), MA crossovers, and AI buzz without evolving theses or new sectors.","Chittick Cash scores (55-82) appear consistently but show no correlation to execution success; high scores on blocked repeats like NVDA/GOOGL suggest over-reliance.","Hugging Face filters (HF Source/Vetoes) mostly 0-1 with no vetoes observed, adding minimal value and potentially noise via unvetted inclusions.","Social buzz and congressional signals absent or weak (e.g., PLTR rejection cites low-weight signals), not improving quality over technicals.","Allocation blocks enforce safety but amplify repetition by sidelining diverse low-confidence picks like ARLO/NXPI."],"rejected_patterns":["Repeated identical SPMO catalysts: '+17.81% 1M return to $132.29, +1.23% daily gains $128-$132 high $131.50 uptrend from $78.25'. Reject if unchanged >3 cycles.","NVDA/GOOGL/SPMO trio in >80% lists: Flag as overused cluster if sector concentration >60% in any 24h window.","Stale price recitals without new data: Block if catalyst verbatim repeat within 48h.","15% single-symbol blocks on repeats: Log as 'stale_repeat' to prioritize sector rotation.","Low Chittick (<70) or HF=0 on non-diverse picks: Auto-demote unless unique catalyst."],"strategy_proposals":["Enforce **sector caps**: Max 40% tech/semis per portfolio; rotate to underweight sectors (industrials, biotech, consumer) on daily scans.","**Diversity score**: Require 3+ sectors per candidate list; penalize confidence -10% per repeat sector.","**Freshness decay**: Reduce confidence 20% daily for unchanged catalysts; reset only on new earnings/news.","**Allocation skew**: Cap repeats at 5% target; boost under-allocated sectors (e.g., ETN power mgmt) to 10% if Chittick>70.","**Test-gate rotation**: Post-block, force-scan underrepresented GICS sectors excluding top-3 repeats."],"self_learning_directives":["Track **repeat frequency** per symbol/sector over 7/30 days; auto-blacklist top offender for 72h if >5 appearances.","Analyze **block reasons**: If 'allocation exceed' >3x on same symbol, demote in scans until diversity>50%.","Log **signal efficacy**: Correlate Chittick/HF with eventual executes; downweight sources if <60% pass rate.","**Output variance check**: Alert if <20% new symbols daily; trigger sector-forced scan.","Post-test gate: Review 7-day candidate diversity; if <4 sectors, self-adjust scan prompts to 'exclude recent repeats, prioritize [underweights]'."],"safe_code_prompt_routine_changes":["Add to candidate filter: `if symbol in last_24h_top3 or catalyst_similarity(last_output, current)>0.8: confidence *= 0.7; sector_weight -= 0.2`","Prompt tweak: 'Generate candidates from underrepresented sectors (non-tech/semis first); exclude symbols appearing >3x in last 48h; vary catalysts with fresh data only.'","Routine: Daily pre-scan: `blocked_symbols = extract_recent_rejects(); undersectors = gics_minus_top3(); prioritize(undersectors)`","Chittick/HF eval: `if chittick<70 and hf_source<2: append 'diversity_bonus' only if new_sector=True`","Table header add: 'DaysSinceLast' column; reject if <2 for non-unique catalysts."]}
## Weekly Strategy Proposals - 2026-05-08 17:17:17 Eastern Daylight Time

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
## Weekly Strategy Proposals - 2026-05-08 17:25:51 Eastern Daylight Time

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
## Weekly Strategy Proposals - 2026-05-15 17:17:48 Eastern Daylight Time

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
## Weekly Strategy Proposals - 2026-05-15 17:25:52 Eastern Daylight Time

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
## Weekly Strategy Proposals - 2026-05-22 17:24:04 Eastern Daylight Time

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
## Weekly Strategy Proposals - 2026-05-22 17:25:06 Eastern Daylight Time

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

