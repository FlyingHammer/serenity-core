import pandas as pd

from app.models.schemas import StrategyParams, TRLSignal
from app.risk.calculations import pips_between


def evaluate_trl(pair: str, timeframe: str, df: pd.DataFrame, params: StrategyParams) -> TRLSignal:
    r = df.iloc[-1]
    p = df.iloc[-2]
    trend_long = r["ema20"] > r["ema50"] > r["ema100"]
    trend_short = r["ema20"] < r["ema50"] < r["ema100"]

    checklist = {
        "ema_alignment_long": bool(trend_long),
        "ema_alignment_short": bool(trend_short),
        "price_position_long": bool(r["close"] > r["ema20"]),
        "price_position_short": bool(r["close"] < r["ema20"]),
        "macd_long": bool(r["macd_hist"] > 0),
        "macd_short": bool(r["macd_hist"] < 0),
        "atr_ok": bool(r["atr14"] / r["close"] > params.atr_floor_ratio),
        "squeeze_ok": bool(r["bb_bw"] > params.squeeze_bw_threshold),
    }
    rule_values = {
        "close": round(float(r["close"]), 5),
        "ema20": round(float(r["ema20"]), 5),
        "ema50": round(float(r["ema50"]), 5),
        "ema100": round(float(r["ema100"]), 5),
        "macd_hist": round(float(r["macd_hist"]), 5),
        "atr14": round(float(r["atr14"]), 5),
        "bb_bw": round(float(r["bb_bw"]), 5),
    }
    confidence_score = int(100 * (sum(1 for v in checklist.values() if v) / max(len(checklist), 1)))

    direction = trigger_mode = None
    if all([trend_long, checklist["price_position_long"], checklist["macd_long"], checklist["atr_ok"], checklist["squeeze_ok"]]):
        direction = "LONG"
    elif all([trend_short, checklist["price_position_short"], checklist["macd_short"], checklist["atr_ok"], checklist["squeeze_ok"]]):
        direction = "SHORT"

    state = "WATCH"
    entry = sl = tp = None
    notes = []
    if direction:
        pullback = (direction == "LONG" and p["low"] <= p["ema20"] and r["close"] > p["high"]) or (
            direction == "SHORT" and p["high"] >= p["ema20"] and r["close"] < p["low"]
        )
        breakout = (direction == "LONG" and r["close"] >= float(df.tail(10)["high"].max())) or (
            direction == "SHORT" and r["close"] <= float(df.tail(10)["low"].min())
        )
        if pullback:
            trigger_mode = "pullback"
            state = "TRIGGERED"
        elif breakout:
            trigger_mode = "breakout"
            state = "TRIGGERED"
        else:
            state = "CONFIRMED"

        if state in {"TRIGGERED", "CONFIRMED"}:
            entry = float(r["close"])
            atr = float(r["atr14"])
            if direction == "LONG":
                sl = float(df.tail(5)["low"].min() - params.atr_buffer_mult * atr)
                tp = entry + 1.5 * (entry - sl)
            else:
                sl = float(df.tail(5)["high"].max() + params.atr_buffer_mult * atr)
                tp = entry - 1.5 * (sl - entry)
            notes.append("TP mode: fixed 1.5R")

    trailing = {
        "activation_at_r": params.trailing_activation_r,
        "activation_pips": round((pips_between(pair, entry, sl) if entry and sl else 0) * params.trailing_activation_r, 1),
        "initial_stop_pips": round(pips_between(pair, entry, sl), 1) if entry and sl else 0.0,
        "distance_pips": params.trailing_distance_pips,
        "step_pips": params.trailing_step_pips,
    }

    return TRLSignal(
        pair=pair,
        timeframe=timeframe,
        state=state,
        direction=direction,
        entry_type="market" if direction else None,
        entry_price=entry,
        sl_price=sl,
        tp_price=tp,
        sl_pips=pips_between(pair, entry, sl) if direction else None,
        tp_pips=pips_between(pair, entry, tp) if direction else None,
        checklist=checklist,
        rule_values=rule_values,
        confidence_score=confidence_score,
        notes=notes,
        trailing=trailing if direction else None,
        trigger_mode=trigger_mode,
    )
