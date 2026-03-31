from trading_scanner.swing_strategy import generate_daily_watchlist
from trading_scanner.options import get_weekly_option
from trading_scanner.risk import RiskConfig, build_trade_plan

config = RiskConfig(account_size=25000)

if __name__ == "__main__":
    print("\n=== DAILY SWING TRADE PLAN V2 ===\n")

    trades = generate_daily_watchlist()

    for t in trades:
        contract = get_weekly_option(t['ticker'], t['price'], t['signal'])

        if not contract:
            continue

        option_price = 2.0

        plan = build_trade_plan(
            ticker=t['ticker'],
            signal=t['signal'],
            contract=contract,
            option_mid_price=option_price,
            config=config
        )

        print(f"{t['ticker']} | {t['setup']} | {t['signal']} | {contract}")
        print(f"RSI: {t['rsi']} | Day Move: {t['day_return_pct']}% | Close Strength: {t['close_position']}")
        print(f"Contracts: {plan.contracts} | Risk: ${plan.max_risk_dollars}")
        print(f"Entry: LAST 15 MIN")
        print(f"Exit: NEXT MORNING (20-40%)")
        print("="*50)
