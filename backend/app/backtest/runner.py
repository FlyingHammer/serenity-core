import math

import pandas as pd

from app.models.schemas import BacktestMetrics, StrategyParams
from app.strategies.mr import evaluate_mr
from app.strategies.trl import evaluate_trl


def _signal_for(strategy: str, pair: str, timeframe: str, frame: pd.DataFrame, params: StrategyParams):
    if strategy == "MR":
        return evaluate_mr(pair, timeframe, frame, params)
    return evaluate_trl(pair, timeframe, frame, params)


def run_backtest(df: pd.DataFrame, pair: str, timeframe: str, strategy: str, params: StrategyParams, lookback: int) -> BacktestMetrics:
    wins = losses = 0
    rs: list[float] = []
    equity = 0.0
    peak = 0.0
    max_dd = 0.0
    start = max(120, len(df) - lookback)

    for i in range(start, len(df) - 5):
        frame = df.iloc[: i + 1]
        sig = _signal_for(strategy, pair, timeframe, frame, params)
        if not sig.direction or not sig.entry_price or not sig.sl_price or not sig.tp_price:
            continue
        post = df.iloc[i + 1 : i + 6]
        risk = abs(sig.entry_price - sig.sl_price)
        if risk == 0:
            continue
        result_r = None
        for _, c in post.iterrows():
            if sig.direction == "LONG":
                if c["low"] <= sig.sl_price:
                    result_r = -1.0
                    break
                if c["high"] >= sig.tp_price:
                    result_r = abs(sig.tp_price - sig.entry_price) / risk
                    break
            else:
                if c["high"] >= sig.sl_price:
                    result_r = -1.0
                    break
                if c["low"] <= sig.tp_price:
                    result_r = abs(sig.entry_price - sig.tp_price) / risk
                    break
        if result_r is None:
            result_r = (post.iloc[-1]["close"] - sig.entry_price) / risk
            if sig.direction == "SHORT":
                result_r *= -1
        rs.append(result_r)
        if result_r > 0:
            wins += 1
        else:
            losses += 1
        equity += result_r
        peak = max(peak, equity)
        max_dd = min(max_dd, equity - peak)

    trades = wins + losses
    gross_win = sum(r for r in rs if r > 0)
    gross_loss = abs(sum(r for r in rs if r <= 0))
    return BacktestMetrics(
        trades=trades,
        win_rate=round((wins / trades) * 100, 2) if trades else 0,
        avg_r=round(sum(rs) / trades, 3) if trades else 0,
        expectancy=round(sum(rs) / trades, 3) if trades else 0,
        max_drawdown_r=round(abs(max_dd), 3),
        profit_factor=round(gross_win / gross_loss, 3) if gross_loss else math.inf,
        sample_warning="Low sample size" if trades < 20 else None,
        assumptions="Candle-based fills, 5-candle hold max, no spread/slippage.",
    )
