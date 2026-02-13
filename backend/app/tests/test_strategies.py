import pandas as pd

from app.indicators.calc import enrich_indicators
from app.models.schemas import StrategyParams
from app.strategies.mr import evaluate_mr
from app.strategies.trl import evaluate_trl


def _mk_df(trend=0.001):
    base = []
    c = 1.0
    for i in range(200):
        c += trend
        base.append({"time": pd.Timestamp("2024-01-01") + pd.Timedelta(hours=i), "open": c - 0.0005, "high": c + 0.001, "low": c - 0.001, "close": c})
    return enrich_indicators(pd.DataFrame(base))


def test_trl_returns_signal_object():
    sig = evaluate_trl("EURUSD", "1H", _mk_df(), StrategyParams())
    assert sig.strategy == "TRL"


def test_mr_returns_signal_object():
    sig = evaluate_mr("EURUSD", "1H", _mk_df(trend=0.0), StrategyParams())
    assert sig.strategy == "MR"
