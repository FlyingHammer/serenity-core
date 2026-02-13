from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

Pair = Literal["GBPJPY", "USDJPY", "USDCHF", "EURUSD", "EURJPY", "EURGBP"]
Timeframe = Literal["1H", "4H"]


class Candle(BaseModel):
    time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float | None = None


class StrategyParams(BaseModel):
    cci_extreme: int = 100
    cci_strict_extreme: int = 150
    atr_buffer_mult: float = 0.5
    rr_min: float = 1.0
    entry_timing: Literal["close_confirm", "intrabar"] = "close_confirm"
    ema_alignment_strict: bool = True
    squeeze_bw_threshold: float = 0.015
    atr_floor_ratio: float = 0.0008
    trailing_activation_r: float = 1.0
    trailing_distance_pips: float = 20.0
    trailing_step_pips: float = 5.0


class RiskSettings(BaseModel):
    account_size: float = 100000
    risk_pct: float = 0.5


class AppSettings(BaseModel):
    risk: RiskSettings = Field(default_factory=RiskSettings)
    mr: StrategyParams = Field(default_factory=StrategyParams)
    trl: StrategyParams = Field(default_factory=StrategyParams)


class SignalBase(BaseModel):
    strategy: Literal["MR", "TRL"]
    pair: Pair
    timeframe: Timeframe
    state: Literal["NONE", "WATCH", "SETUP", "CONFIRMED", "TRIGGERED"]
    direction: Literal["LONG", "SHORT"] | None = None
    entry_type: Literal["market", "limit"] | None = None
    entry_price: float | None = None
    tp_price: float | None = None
    sl_price: float | None = None
    tp_pips: float | None = None
    sl_pips: float | None = None
    trailing: dict[str, Any] | None = None
    checklist: dict[str, bool] = Field(default_factory=dict)
    rule_values: dict[str, float | str | bool] = Field(default_factory=dict)
    confidence_score: int = 0
    notes: list[str] = Field(default_factory=list)


class MRSignal(SignalBase):
    strategy: Literal["MR"] = "MR"
    confirmation_mode: Literal["close_confirm", "intrabar"]


class TRLSignal(SignalBase):
    strategy: Literal["TRL"] = "TRL"
    trigger_mode: Literal["pullback", "breakout"] | None = None


class OrderEntrySheet(BaseModel):
    pair: Pair
    direction: Literal["LONG", "SHORT"]
    order_type: Literal["market", "limit"]
    lot_size: float
    entry_price: float
    stop_price: float
    take_profit_price: float
    stop_distance_pips: float
    take_profit_distance_pips: float
    broker_fields: dict[str, float | str]


class ScanRequest(BaseModel):
    params: StrategyParams = Field(default_factory=StrategyParams)
    risk: RiskSettings = Field(default_factory=RiskSettings)


class BacktestRequest(BaseModel):
    pair: Pair
    timeframe: Timeframe
    strategy: Literal["MR", "TRL"]
    lookback: int = 300
    params: StrategyParams = Field(default_factory=StrategyParams)


class BacktestMetrics(BaseModel):
    trades: int
    win_rate: float
    avg_r: float
    expectancy: float
    max_drawdown_r: float
    profit_factor: float
    sample_warning: str | None = None
    assumptions: str
