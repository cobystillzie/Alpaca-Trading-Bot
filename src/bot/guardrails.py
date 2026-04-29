from __future__ import annotations

from .alpaca import as_float
from .models import GuardrailResult, TradeCandidate
from .strategy import score_candidate


MAX_NEW_POSITIONS_PER_DAY = 2
MAX_OPEN_POSITIONS = 8
MAX_SINGLE_STOCK_ALLOCATION = 15.0
MIN_CASH_RESERVE = 10.0


def evaluate_candidate_for_order(
    candidate: TradeCandidate,
    account: dict,
    positions: list[dict],
    *,
    today_order_count: int,
) -> GuardrailResult:
    reasons: list[str] = []
    warnings: list[str] = []

    score = score_candidate(candidate)
    if not score.approved:
        return GuardrailResult(False, score.rejects, score.reasons)

    if today_order_count >= MAX_NEW_POSITIONS_PER_DAY:
        reasons.append("Daily new-position limit already reached.")

    existing_symbols = {str(pos.get("symbol", "")).upper() for pos in positions}
    if candidate.symbol not in existing_symbols and len(existing_symbols) >= MAX_OPEN_POSITIONS:
        reasons.append("Max open-position count would be exceeded.")

    portfolio_value = as_float(account.get("portfolio_value"))
    buying_power = as_float(account.get("buying_power"))
    cash = as_float(account.get("cash"), buying_power)
    if portfolio_value <= 0:
        reasons.append("Portfolio value is unavailable or zero.")
        return GuardrailResult(False, reasons, warnings)

    requested_notional = portfolio_value * (candidate.target_allocation_percent / 100)
    max_notional = portfolio_value * (MAX_SINGLE_STOCK_ALLOCATION / 100)
    requested_notional = min(requested_notional, max_notional)

    current_symbol_value = 0.0
    for pos in positions:
        if str(pos.get("symbol", "")).upper() == candidate.symbol:
            current_symbol_value += as_float(pos.get("market_value"))

    post_symbol_allocation = (
        (current_symbol_value + requested_notional) / portfolio_value * 100
    )
    if post_symbol_allocation > MAX_SINGLE_STOCK_ALLOCATION:
        reasons.append("Single-stock allocation would exceed 15%.")

    min_cash_after = portfolio_value * (MIN_CASH_RESERVE / 100)
    affordable_notional = max(0.0, min(buying_power, cash - min_cash_after))
    order_notional = min(requested_notional, affordable_notional)
    if order_notional < 25:
        reasons.append("Order would violate minimum cash reserve or is too small.")

    if order_notional < requested_notional:
        warnings.append("Order notional reduced to preserve cash reserve.")

    return GuardrailResult(
        approved=not reasons,
        reasons=reasons or score.reasons,
        warnings=warnings,
        order_notional=round(order_notional, 2),
    )

