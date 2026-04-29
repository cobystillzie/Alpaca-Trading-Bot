# Idiot-Proof Setup

Follow these steps exactly.

## 1. Open PowerShell

Paste this:

```powershell
cd C:\Users\cobys\projects\alpaca-trading-bot
```

## 2. Create Your Local Secret File

Paste this:

```powershell
notepad .env.local
```

Notepad will open. Paste this whole template:

```env
ALPACA_ENV=paper
ALPACA_BASE_URL=https://paper-api.alpaca.markets
ALPACA_API_KEY=PASTE_YOUR_ALPACA_PAPER_KEY_HERE
ALPACA_SECRET_KEY=PASTE_YOUR_ALPACA_PAPER_SECRET_HERE

PERPLEXITY_API_KEY=PASTE_YOUR_PERPLEXITY_KEY_HERE

TELEGRAM_BOT_TOKEN=PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE
TELEGRAM_CHAT_ID=PASTE_YOUR_TELEGRAM_CHAT_ID_HERE

AUTO_GIT_PUSH=true
LIVE_TRADING_ENABLED=false
MANAGED_CAPITAL_USD=10000
```

Replace each `PASTE_..._HERE` value with the real value. Save Notepad.

Never commit `.env.local`. It is ignored by Git.

## 3. Get Alpaca Paper Keys

1. Log in to Alpaca.
2. Switch to paper trading.
3. Go to API keys.
4. Copy the paper API key into `ALPACA_API_KEY`.
5. Copy the paper API secret into `ALPACA_SECRET_KEY`.

Do not use live Alpaca keys for version one.

Alpaca paper accounts can show $100,000 by default. This bot self-limits sizing with
`MANAGED_CAPITAL_USD=10000`, so it behaves like it only manages $10,000.

## 4. Get Perplexity Key

1. Open your Perplexity API account.
2. Create or copy an API key.
3. Paste it into `PERPLEXITY_API_KEY`.

## 5. Create Telegram Bot

1. Open Telegram.
2. Search for `@BotFather`.
3. Send `/newbot`.
4. Follow the prompts.
5. Copy the token into `TELEGRAM_BOT_TOKEN`.
6. Send one message to your new bot from your own Telegram account.
7. Back in PowerShell, paste:

```powershell
$env:PYTHONPATH = "C:\Users\cobys\projects\alpaca-trading-bot\src"
python -m bot.cli telegram-chat-id
```

8. Copy the chat id shown in PowerShell into `TELEGRAM_CHAT_ID`.

## 6. Verify Setup

Paste:

```powershell
.\scripts\setup-check.ps1
```

If it reports missing keys, reopen `.env.local` and fix the missing values:

```powershell
notepad .env.local
```

## 7. Run Manual Paper Workflow

Paste these one at a time:

```powershell
.\scripts\run-research.ps1
.\scripts\run-premarket.ps1
.\scripts\run-market-open.ps1
```

`run-market-open.ps1` can place Alpaca paper orders if every guardrail passes.

## 8. Optional GitHub Remote Setup

This computer does not currently have the GitHub CLI installed. To connect this local repo to GitHub:

1. Create a new private GitHub repo in your browser.
2. Copy the repo URL.
3. Paste this in PowerShell, replacing the URL:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

After that, runtime auto-push will only add/commit/push markdown memory files.

## Costs

- Alpaca paper trading: $0.
- Telegram bot DM: $0.
- GitHub Free repo: $0.
- Perplexity Sonar: roughly $1-$10/month for light/medium daily use; every-2-hour weekday research may be closer to $5-$20/month depending on context size.
- Alpaca Algo Trader Plus: optional $99/month, not needed at first.
- Codex automations: use existing Codex/ChatGPT plan first.
- OpenAI API direct usage: avoid unless needed.
