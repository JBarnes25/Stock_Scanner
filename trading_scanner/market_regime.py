import yfinance as yf

def get_market_regime():
    spy = yf.download("SPY", period="1mo", interval="1d")
    if spy.empty:
        return "UNKNOWN"

    last = spy['Close'].iloc[-1]
    sma50 = spy['Close'].rolling(50).mean().iloc[-1]

    if last > sma50:
        return "BULL"
    elif last < sma50:
        return "BEAR"
    return "NEUTRAL"
