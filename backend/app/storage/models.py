from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String

from app.storage.database import Base


class SignalRecord(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String, index=True)
    timeframe = Column(String, index=True)
    strategy = Column(String, index=True)
    direction = Column(String)
    state = Column(String)
    entry_type = Column(String)
    entry_price = Column(Float)
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class BacktestRecord(Base):
    __tablename__ = "backtests"

    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String, index=True)
    timeframe = Column(String, index=True)
    strategy = Column(String, index=True)
    lookback = Column(Integer)
    metrics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class SettingsRecord(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    payload = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
