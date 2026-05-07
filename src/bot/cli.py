from __future__ import annotations

import argparse

from .config import load_settings
from .runner import (
    run_close,
    run_hf_eval,
    run_hf_setup,
    run_market_open,
    run_midday,
    run_performance_report,
    run_premarket,
    run_research,
    run_self_learning_finalize,
    run_weekly_review,
    setup_check,
)
from .telegram import get_updates


def telegram_chat_id() -> int:
    settings = load_settings()
    updates = get_updates(settings)
    if not updates:
        print("No Telegram updates found. Message your bot once, then run this again.")
        return 1
    seen: set[str] = set()
    for update in updates:
        message = update.get("message") or update.get("channel_post") or {}
        chat = message.get("chat") or {}
        chat_id = str(chat.get("id", "")).strip()
        if chat_id and chat_id not in seen:
            seen.add(chat_id)
            print(f"TELEGRAM_CHAT_ID={chat_id}  title={chat.get('title') or chat.get('username') or chat.get('first_name') or 'private'}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="alpaca-trading-bot")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in [
        "setup-check",
        "research",
        "premarket",
        "market-open",
        "midday",
        "close",
        "performance-report",
        "weekly-review",
        "telegram-chat-id",
        "hf-setup",
        "hf-eval",
        "self-learning-finalize",
    ]:
        parser_for_command = sub.add_parser(command)
        if command == "hf-setup":
            parser_for_command.add_argument("--download", action="store_true")
            parser_for_command.add_argument("--include-large", action="store_true")
    args = parser.parse_args()
    if args.command == "setup-check":
        return setup_check()
    if args.command == "research":
        return run_research()
    if args.command == "premarket":
        return run_premarket()
    if args.command == "market-open":
        return run_market_open()
    if args.command == "midday":
        return run_midday()
    if args.command == "close":
        return run_close()
    if args.command == "performance-report":
        return run_performance_report()
    if args.command == "weekly-review":
        return run_weekly_review()
    if args.command == "telegram-chat-id":
        return telegram_chat_id()
    if args.command == "hf-setup":
        return run_hf_setup(download=args.download, include_large=args.include_large)
    if args.command == "hf-eval":
        return run_hf_eval()
    if args.command == "self-learning-finalize":
        return run_self_learning_finalize()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
