from __future__ import annotations

from typing import List

from .scanner import scan_ticker
from .intraday import intraday_scan
from .options import get_weekly_option
from .news import fetch_yahoo_news, headline_sentiment_score
from .market_regime import get_market_regime
from .risk import RiskConfig, build_trade_plan


def evaluate_trade(ticker: str, config: RiskConfig):
    daily = scan_ticker(ticker)
    if not daily:
        return None

    intraday_signal = intraday_scan(ticker)

    headlines = fetch_yahoo_news(ticker)
    sentiment = headline_sentiment_score(headlines)

    regime = get_market_regime()

    # Basic confluence rules
    if regime == 'BULL' and daily['signal'] == 'BREAKOUT' and sentiment >= 0:
        direction_ok = True
    elif regime == 'BEAR' and daily['signal'] == 'BREAKDOWN' and sentiment <= 0:
        direction_ok = True
    else:
        direction_ok = False

    if not direction_ok:
        return None

    contract = get_weekly_option(ticker, daily['price'], daily['signal'])
    if not contract:
        return None

    # [Unverified] Option mid price estimation placeholder; replace with live quote if available
    option_mid_price = 2.0

    plan = build_trade_plan(
        ticker=ticker,
        signal=daily['signal'],
        contract=contract,
        option_mid_price=option_mid_price,
        config=config,
    )

    return {
        'ticker': ticker,
        'signal': daily['signal'],
        'intraday': intraday_signal,
        'sentiment': sentiment,
        'regime': regime,
        'contract': contract,
        'trade_plan': plan,
    }


def run_workflow(tickers: List[str], config: RiskConfig):
    plans = []
    for t in tickers:
        result = evaluate_trade(t, config)
        if result:
            plans.append(result)
    return plans
