# Stock Scanner

A Python-based stock and options scanner focused on news alerts, breakouts, breakdowns, market regime filtering, and Robinhood-ready watchlist exports.

## Features

- Daily and intraday scans for breakouts and breakdowns
- Volume, RSI, ATR, gap, and VWAP confirmation
- News headline fetching and simple sentiment scoring
- Weekly options candidate suggestions
- Market regime filter using SPY/QQQ trend and VWAP
- Discord, Telegram, and email alerts
- Robinhood-ready CSV export
- GitHub Actions workflow for scheduled runs

## Project structure

```text
trading_scanner/
  alerts.py
  market_regime.py
  options.py
  scanner.py
  utils.py
live_news_breakout_bot.py
requirements.txt
.env.example
.github/workflows/scanner.yml
```

## Install

```bash
pip install -r requirements.txt
```

## Run once

```bash
python live_news_breakout_bot.py --tickers QQQ NVDA AMD TSLA MSTR GOOGL
```

## Run every 5 minutes

```bash
python live_news_breakout_bot.py --tickers QQQ NVDA AMD TSLA MSTR GOOGL --loop --interval 5
```

## Environment variables

See `.env.example` for Discord, Telegram, and email settings.
