import pandas as pd

from app.indicators.calc import enrich_indicators


def test_indicator_columns_present():
    df = pd.DataFrame({
        "time": pd.date_range("2024-01-01", periods=150, freq="h"),
        "open": [1 + i * 0.001 for i in range(150)],
        "high": [1.002 + i * 0.001 for i in range(150)],
        "low": [0.998 + i * 0.001 for i in range(150)],
        "close": [1.001 + i * 0.001 for i in range(150)],
    })
    out = enrich_indicators(df)
    for col in ["ema20", "ema50", "ema100", "bb_upper", "atr14", "cci20", "macd_hist"]:
        assert col in out.columns
