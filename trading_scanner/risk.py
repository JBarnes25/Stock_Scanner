from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskConfig:
    account_size: float = 25000.0
    risk_per_trade_pct: float = 0.01
    max_open_positions: int = 3
    max_daily_loss_pct: float = 0.02
    target_profit_pct: float = 0.25
    stop_loss_pct: float = 0.15


@dataclass
class TradePlan:
    ticker: str
    signal: str
    contract: str
    max_risk_dollars: float
    contracts: int
    entry_type: str
    take_profit_pct: float
    stop_loss_pct: float


def calc_max_risk_dollars(account_size: float, risk_per_trade_pct: float) -> float:
    return round(account_size * risk_per_trade_pct, 2)


def estimate_contract_count(max_risk_dollars: float, option_mid_price: float) -> int:
    if option_mid_price <= 0:
        return 0
    # Option contracts control 100 shares.
    per_contract_cost = option_mid_price * 100
    contracts = int(max_risk_dollars // per_contract_cost)
    return max(contracts, 0)


def build_trade_plan(ticker: str, signal: str, contract: str, option_mid_price: float, config: RiskConfig) -> TradePlan:
    max_risk = calc_max_risk_dollars(config.account_size, config.risk_per_trade_pct)
    contracts = estimate_contract_count(max_risk, option_mid_price)
    return TradePlan(
        ticker=ticker,
        signal=signal,
        contract=contract,
        max_risk_dollars=max_risk,
        contracts=contracts,
        entry_type='LIMIT',
        take_profit_pct=config.target_profit_pct,
        stop_loss_pct=config.stop_loss_pct,
    )
