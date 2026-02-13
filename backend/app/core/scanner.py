from sqlalchemy.orm import Session

from app.backtest.runner import run_backtest
from app.data.service import SUPPORTED_PAIRS, SUPPORTED_TIMEFRAMES, DataService
from app.models.schemas import AppSettings
from app.risk.calculations import build_order_sheet
from app.storage.models import BacktestRecord, SignalRecord
from app.strategies.mr import evaluate_mr
from app.strategies.trl import evaluate_trl


def scan_all(db: Session, settings: AppSettings):
    service = DataService()
    out = []
    for pair in SUPPORTED_PAIRS:
        for tf in SUPPORTED_TIMEFRAMES:
            try:
                df = service.load(pair, tf)
            except FileNotFoundError:
                continue
            mr = evaluate_mr(pair, tf, df, settings.mr)
            trl = evaluate_trl(pair, tf, df, settings.trl)
            last_price = float(df.iloc[-1]["close"])
            for sig in [mr, trl]:
                payload = sig.model_dump()
                payload["last_price"] = last_price
                if sig.direction and sig.entry_price and sig.sl_price and sig.tp_price:
                    payload["order_sheet"] = build_order_sheet(
                        pair=pair,
                        direction=sig.direction,
                        order_type=sig.entry_type or "market",
                        entry=sig.entry_price,
                        sl=sig.sl_price,
                        tp=sig.tp_price,
                        account_size=settings.risk.account_size,
                        risk_pct=settings.risk.risk_pct,
                        trailing=sig.trailing,
                    ).model_dump()
                bt = run_backtest(df, pair, tf, sig.strategy, settings.mr if sig.strategy == "MR" else settings.trl, 300)
                payload["backtest"] = bt.model_dump()
                rec = SignalRecord(
                    pair=pair,
                    timeframe=tf,
                    strategy=sig.strategy,
                    direction=sig.direction,
                    state=sig.state,
                    entry_type=sig.entry_type,
                    entry_price=sig.entry_price,
                    payload=payload,
                )
                db.add(rec)
                db.flush()
                payload["id"] = rec.id
                rec.payload = payload
                db.add(
                    BacktestRecord(pair=pair, timeframe=tf, strategy=sig.strategy, lookback=300, metrics=bt.model_dump())
                )
                out.append(payload)
                print(f"[ALERT] {pair} {tf} {sig.strategy} -> {sig.state} {sig.direction}")
    db.commit()
    return out
