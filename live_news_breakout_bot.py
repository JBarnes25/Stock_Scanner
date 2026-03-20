from trading_scanner.scanner import scan_ticker
from trading_scanner.market_regime import get_market_regime

TICKERS = ["QQQ","NVDA","AMD","TSLA","MSTR","GOOGL"]

if __name__ == "__main__":
    regime = get_market_regime()
    print(f"Market Regime: {regime}\n")

    for ticker in TICKERS:
        result = scan_ticker(ticker)
        if result:
            print(result)
