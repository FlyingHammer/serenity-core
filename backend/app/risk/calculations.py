from app.models.schemas import OrderEntrySheet


def pip_size(pair: str) -> float:
    return 0.01 if pair.endswith("JPY") else 0.0001


def pips_between(pair: str, p1: float, p2: float) -> float:
    return abs(p1 - p2) / pip_size(pair)


def pip_value_per_standard_lot(pair: str, price: float) -> float:
    # USD account approximation
    return 1000.0 / price if pair.endswith("JPY") else 10.0


def lot_size_for_risk(account_size: float, risk_pct: float, sl_pips: float, pip_value: float) -> float:
    risk_amount = account_size * (risk_pct / 100)
    if sl_pips <= 0 or pip_value <= 0:
        return 0.0
    return round(risk_amount / (sl_pips * pip_value), 2)


def build_order_sheet(
    pair: str,
    direction: str,
    order_type: str,
    entry: float,
    sl: float,
    tp: float,
    account_size: float,
    risk_pct: float,
    trailing: dict | None = None,
) -> OrderEntrySheet:
    sl_pips = pips_between(pair, entry, sl)
    tp_pips = pips_between(pair, entry, tp)
    pip_value = pip_value_per_standard_lot(pair, entry)
    lot = lot_size_for_risk(account_size, risk_pct, sl_pips, pip_value)
    broker_fields = {
        "order": order_type,
        "direction": direction,
        "stop_distance": round(sl_pips, 1),
        "take_profit_distance": round(tp_pips, 1),
        "initial_stop_pips": round(trailing.get("initial_stop_pips", sl_pips), 1) if trailing else round(sl_pips, 1),
        "trailing_step_pips": round(trailing.get("step_pips", 0.0), 1) if trailing else 0.0,
        "trailing_activation_pips": round(trailing.get("activation_pips", 0.0), 1) if trailing else 0.0,
        "activation_at_r": trailing.get("activation_at_r", 0.0) if trailing else 0.0,
    }
    return OrderEntrySheet(
        pair=pair,
        direction=direction,
        order_type=order_type,
        lot_size=lot,
        entry_price=entry,
        stop_price=sl,
        take_profit_price=tp,
        stop_distance_pips=round(sl_pips, 1),
        take_profit_distance_pips=round(tp_pips, 1),
        broker_fields=broker_fields,
    )
