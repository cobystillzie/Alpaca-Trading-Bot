# Alpaca Chat Transfer Checklist

Use this checklist to transfer context from a mixed Codex thread into a clean
Alpaca Trading Bot chat opened from the repo folder.

## 1. Open The Correct Folder

Open a new Codex chat from:

```powershell
C:\Users\cobys\projects\alpaca-trading-bot
```

If the new chat shows a different working directory, stop and reopen it from
the Alpaca repo folder.

## 2. Paste The Starter Prompt

Paste this into the new Alpaca-folder chat:

```text
You are now working in C:\Users\cobys\projects\alpaca-trading-bot.

First read AGENTS.md, README.md, SETUP.md, memory/SELF-LEARNING-POLICY.md, memory/TRADING-STRATEGY.md, memory/CHITTICK-CASH.md, docs/codex-control/ALPACA_CHAT_HANDOFF.md, and docs/codex-control/AUTOMATION_MAP.md.

This repo is the active Alpaca paper-trading long-term bot. Keep all guardrails: paper trading only, no live trading, no options, no crypto, no margin, no short selling, no secrets, and do not edit .env.local.

Before proposing or changing anything, summarize current repo state, active automations, latest memory lessons, and the safest next action.
```

## 3. Verify Repo State

Ask the new chat to run:

```powershell
git status --short
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Expected result:

- `git status --short` should be empty before new work.
- Local `HEAD` should match GitHub `origin/main`.

## 4. Verify Tests

Ask the new chat to run:

```powershell
python -m pytest
python -m compileall -q src
```

Both should pass before any automation or strategy change.

## 5. Verify Setup Only When Needed

To verify local keys and external services, run:

```powershell
.\scripts\setup-check.ps1
```

This can call Alpaca, Perplexity, and Telegram. Do not run it if you only need
a repo-only documentation check.

## 6. Confirm Telegram And Automation State

Before relying on unattended automation, confirm:

- Telegram receives routine summaries.
- `memory/TELEGRAM-SUMMARIES.md` is updating.
- The active automation IDs in `docs/codex-control/AUTOMATION_MAP.md` still match the Codex app.
- The Friday self-learning automation keeps `gpt-5.5`.

## 7. Keep Future Projects Separate

This handoff is for the long-term Alpaca paper-trading bot only.

Create separate handoff/control packs later for:

- options or volatility trading bot
- shortform-content-ops
- any unrelated workflow

Do not blend their strategies, schedules, or safety boundaries into this repo.
