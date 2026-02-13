import numpy as np
import pandas as pd

from app.models.schemas import MRSignal, StrategyParams
from app.risk.calculations import pips_between


def evaluate_mr(pair: str, timeframe: str, df: pd.DataFrame, params: StrategyParams) -> MRSignal:
    r = df.iloc[-1]
    p = df.iloc[-2]
    checklist = {
        "band_touch_upper": bool(r["high"] >= r["bb_upper"]),
        "band_touch_lower": bool(r["low"] <= r["bb_lower"]),
        "cci_turn_long": bool(p["cci20"] < -params.cci_extreme and r["cci20"] > p["cci20"]),
        "cci_turn_short": bool(p["cci20"] > params.cci_extreme and r["cci20"] < p["cci20"]),
        "macd_decelerating": bool(abs(r["macd_hist"]) < abs(p["macd_hist"])),
    }
    rule_values = {
        "close": round(float(r["close"]), 5),
        "cci_prev": round(float(p["cci20"]), 2),
        "cci_now": round(float(r["cci20"]), 2),
        "macd_hist_prev": round(float(p["macd_hist"]), 5),
        "macd_hist_now": round(float(r["macd_hist"]), 5),
        "bb_upper": round(float(r["bb_upper"]), 5),
        "bb_lower": round(float(r["bb_lower"]), 5),
        "atr14": round(float(r["atr14"]), 5),
    }
    confidence_score = int(100 * (sum(1 for v in checklist.values() if v) / max(len(checklist), 1)))
    direction = None
    if checklist["band_touch_lower"] and checklist["cci_turn_long"] and checklist["macd_decelerating"]:
        direction = "LONG"
    elif checklist["band_touch_upper"] and checklist["cci_turn_short"] and checklist["macd_decelerating"]:
        direction = "SHORT"

    state = "NONE"
    entry = sl = tp = None
    notes = [f"MR mode: {params.entry_timing}"]

    if direction:
        state = "CONFIRMED" if params.entry_timing == "close_confirm" else "TRIGGERED"
        entry = float(r["close"])
        atr = float(r["atr14"])
        if direction == "LONG":
            swing = float(df.tail(5)["low"].min())
            sl = min(swing, float(r["bb_lower"]) - params.atr_buffer_mult * atr)
            tp = float(r["ema20"])
        else:
            swing = float(df.tail(5)["high"].max())
            sl = max(swing, float(r["bb_upper"]) + params.atr_buffer_mult * atr)
            tp = float(r["ema20"])
        rr = pips_between(pair, entry, tp) / max(pips_between(pair, entry, sl), 1e-9)
        notes.append(f"R:R={rr:.2f}")
        if rr < params.rr_min:
            state = "WATCH"
            notes.append("Rejected by min R:R")
    else:
        if checklist["band_touch_lower"] or checklist["band_touch_upper"]:
            state = "SETUP"
        elif np.isnan(r["bb_upper"]):
            state = "WATCH"

    trailing = {
        "activation_at_r": params.trailing_activation_r,
        "activation_pips": round((pips_between(pair, entry, sl) if entry and sl else 0) * params.trailing_activation_r, 1),
        "initial_stop_pips": round(pips_between(pair, entry, sl), 1) if entry and sl else 0.0,
        "distance_pips": params.trailing_distance_pips,
        "step_pips": params.trailing_step_pips,
    }

    return MRSignal(
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
        confirmation_mode=params.entry_timing,
    )
