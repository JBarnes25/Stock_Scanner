import yfinance as yf
import pandas as pd
from .utils import rsi, atr


def scan_ticker(ticker):
    df = yf.download(ticker, period="3mo", interval="1d")
    if df.empty:
        return None

    df['rsi'] = rsi(df['Close'])
    df['atr'] = atr(df)

    last = df.iloc[-1]
    prev = df.iloc[-2]

    breakout = last['Close'] > df['High'].rolling(20).max().iloc[-2]
    breakdown = last['Close'] < df['Low'].rolling(20).min().iloc[-2]

    if breakout:
        signal = "BREAKOUT"
    elif breakdown:
        signal = "BREAKDOWN"
    else:
        return None

    return {
        "ticker": ticker,
        "signal": signal,
        "price": round(last['Close'], 2),
        "rsi": round(last['rsi'], 2),
        "atr": round(last['atr'], 2)
    }
