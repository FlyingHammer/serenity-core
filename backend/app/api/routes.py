from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.scanner import scan_all
from app.core.settings_store import get_settings, save_settings
from app.data.service import SUPPORTED_PAIRS, SUPPORTED_TIMEFRAMES
from app.models.schemas import AppSettings
from app.storage.database import get_db
from app.storage.models import SignalRecord

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/pairs")
def pairs():
    return {"pairs": SUPPORTED_PAIRS, "timeframes": SUPPORTED_TIMEFRAMES}


@router.get("/settings")
def read_settings(db: Session = Depends(get_db)):
    return get_settings(db)


@router.put("/settings")
def update_settings(payload: AppSettings, db: Session = Depends(get_db)):
    return save_settings(db, payload)


@router.post("/scan")
def scan(db: Session = Depends(get_db)):
    settings = get_settings(db)
    return scan_all(db, settings)


@router.get("/signals")
def signals(
    pair: str | None = Query(default=None), timeframe: str | None = Query(default=None), strategy: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(SignalRecord).order_by(SignalRecord.created_at.desc())
    if pair:
        stmt = stmt.where(SignalRecord.pair == pair)
    if timeframe:
        stmt = stmt.where(SignalRecord.timeframe == timeframe)
    if strategy:
        stmt = stmt.where(SignalRecord.strategy == strategy)
    return [r.payload for r in db.execute(stmt.limit(200)).scalars().all()]


@router.get("/signals/{signal_id}")
def signal_detail(signal_id: int, db: Session = Depends(get_db)):
    row = db.execute(select(SignalRecord).where(SignalRecord.id == signal_id)).scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Signal not found")
    return row.payload
