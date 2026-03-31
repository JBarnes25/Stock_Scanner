import yfinance as yf
from .utils import rsi

WATCHLIST = ["QQQ", "NVDA", "AMD", "TSLA", "MSTR", "XOM", "CVX", "META", "GOOGL"]


def evaluate_swing_trade(ticker):
    intraday = yf.download(ticker, period="5d", interval="5m", progress=False)
    if intraday.empty or len(intraday) < 50:
        return None

    daily = yf.download(ticker, period="1mo", interval="1d", progress=False)
    if daily.empty or len(daily) < 15:
        return None

    last_day = daily.iloc[-1]
    rsi_val = rsi(daily['Close']).iloc[-1]

    day_high = float(last_day['High'])
    day_low = float(last_day['Low'])
    close = float(last_day['Close'])

    spread = max(day_high - day_low, 1e-6)
    position = (close - day_low) / spread
    day_return = daily['Close'].pct_change().iloc[-1]

    signal = None
    setup = None

    if position > 0.8 and rsi_val > 55:
        signal = 'CALL'
        setup = 'STRONG_CLOSE_CONTINUATION'
    elif position < 0.2 and rsi_val < 45:
        signal = 'PUT'
        setup = 'WEAK_CLOSE_BREAKDOWN'
    elif day_return < -0.08 and position > 0.3:
        signal = 'CALL'
        setup = 'OVERSOLD_BOUNCE'

    if not signal:
        return None

    return {
        'ticker': ticker,
        'signal': signal,
        'setup': setup,
        'price': round(close, 2),
        'rsi': round(float(rsi_val), 2),
        'day_return_pct': round(float(day_return) * 100, 2),
        'close_position': round(float(position), 2),
    }


def generate_daily_watchlist():
    trades = []
    for ticker in WATCHLIST:
        result = evaluate_swing_trade(ticker)
        if result:
            trades.append(result)
    return trades
