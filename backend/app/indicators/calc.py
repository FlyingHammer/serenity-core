import pandas as pd


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def bollinger_bands(close: pd.Series, period: int = 20, stdev: float = 2.0):
    ma = close.rolling(period).mean()
    sd = close.rolling(period).std(ddof=0)
    upper = ma + stdev * sd
    lower = ma - stdev * sd
    bandwidth = (upper - lower) / ma
    return ma, upper, lower, bandwidth


def atr(df: pd.DataFrame, period: int = 14):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def cci(df: pd.DataFrame, period: int = 20):
    tp = (df["high"] + df["low"] + df["close"]) / 3
    sma = tp.rolling(period).mean()
    mad = (tp - sma).abs().rolling(period).mean()
    return (tp - sma) / (0.015 * mad)


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal_p: int = 9):
    macd_line = ema(close, fast) - ema(close, slow)
    signal_line = ema(macd_line, signal_p)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist


def enrich_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ema20"] = ema(out["close"], 20)
    out["ema50"] = ema(out["close"], 50)
    out["ema100"] = ema(out["close"], 100)
    bb_mid, bb_upper, bb_lower, bb_bw = bollinger_bands(out["close"], 20, 2)
    out["bb_mid"] = bb_mid
    out["bb_upper"] = bb_upper
    out["bb_lower"] = bb_lower
    out["bb_bw"] = bb_bw
    out["atr14"] = atr(out, 14)
    out["cci20"] = cci(out, 20)
    macd_line, signal_line, hist = macd(out["close"], 12, 26, 9)
    out["macd"] = macd_line
    out["macd_signal"] = signal_line
    out["macd_hist"] = hist
    return out
