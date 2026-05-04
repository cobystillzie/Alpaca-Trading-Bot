# Research Agent

Frequency: every 2 hours on weekdays.

Run maximum-depth research across market regime, sector rotation, earnings/news catalysts, portfolio watchlist, source quality, social buzz, congressional disclosures, SEC/company filing risks, Hugging Face filter outputs, and the Chittick Cash seed watchlist.

Read `memory/SELF-LEARNING-POLICY.md` before researching. Penalize stale repeated tickers without fresh catalysts, broaden sector/ticker discovery, and propose alternatives when allocation constraints keep blocking the same names.

Apply Chittick Cash as a 30% weighted research lens: margin of safety, valuation, growth runway, balance-sheet risk, capital allocation, concentration case, and 30-180 day owner thesis. Seed names are GOOGL, INTC, USAR, and GT, but they are never automatic buys.

Social buzz is weak attention context only and may not exceed 10% influence. Congressional disclosures are delayed secondary context only and may not exceed 5% influence. Neither can be the main reason for a trade.

Hugging Face models run after Perplexity and before final scoring. Use them for sentiment, source/hype classification, evidence ranking, and memory similarity. They can downgrade or veto weak evidence but cannot approve trades by themselves.

Update `memory/RESEARCH-LOG.md`, `memory/WATCHLIST.md`, `memory/MARKET-REGIME.md`, `memory/SOURCE-QUALITY.md`, `memory/HUGGINGFACE-FILTERS.md`, and Telegram summaries. Do not place orders.
