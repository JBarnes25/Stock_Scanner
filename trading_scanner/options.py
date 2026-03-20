import yfinance as yf


def get_weekly_option(ticker_symbol, price, signal):
    try:
        ticker = yf.Ticker(ticker_symbol)
        expirations = ticker.options
        if not expirations:
            return None

        exp = expirations[0]
        chain = ticker.option_chain(exp)

        if signal == "BREAKOUT":
            side = "CALL"
            strikes = chain.calls['strike']
        elif signal == "BREAKDOWN":
            side = "PUT"
            strikes = chain.puts['strike']
        else:
            return None

        strike = min(strikes, key=lambda x: abs(x - price))
        return f"{ticker_symbol} {exp} {strike} {side}"

    except Exception:
        return None
