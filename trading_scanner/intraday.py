import yfinance as yf


def intraday_scan(ticker):
    df = yf.download(ticker, period="1d", interval="5m")
    if df.empty:
        return None

    high = df['High'].max()
    low = df['Low'].min()
    last = df['Close'].iloc[-1]

    if last >= high * 0.995:
        return "NEAR_BREAKOUT"
    elif last <= low * 1.005:
        return "NEAR_BREAKDOWN"
    return None
