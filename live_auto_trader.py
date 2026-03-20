from trading_scanner.workflow import run_workflow
from trading_scanner.risk import RiskConfig

TICKERS = ["QQQ","NVDA","AMD","TSLA","MSTR","GOOGL"]

if __name__ == "__main__":
    config = RiskConfig(account_size=25000)

    plans = run_workflow(TICKERS, config)

    print("\n=== AUTO TRADING EXECUTION PLAN ===\n")

    for p in plans:
        tp = p['trade_plan']
        print(f"{p['ticker']} | {p['signal']} | {p['contract']}")
        print(f"Contracts: {tp.contracts} | Max Risk: ${tp.max_risk_dollars}")
        print(f"Take Profit: {tp.take_profit_pct*100}%")
        print(f"Stop Loss: {tp.stop_loss_pct*100}%")
        print("="*50)
