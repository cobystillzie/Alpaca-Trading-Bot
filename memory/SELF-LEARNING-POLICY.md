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
- Current candidate diversity buckets: mega-cap-internet-cloud, semiconductors, software-internet-services, solar-renewables.
- Overused recent diversity buckets: none.
- Weekly review must disclose any code or prompt edits through Telegram before commit/push.

## Latest Review Input

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
