from pathlib import Path

import pandas as pd

from app.core.config import settings
from app.data.providers.base import CandleProvider


class CSVCandleProvider(CandleProvider):
    def __init__(self, data_dir: str | None = None):
        self.data_dir = Path(data_dir or settings.data_dir)

    def get_candles(self, pair: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        path = self.data_dir / f"{pair}_{timeframe}.csv"
        if not path.exists():
            raise FileNotFoundError(f"Missing candle file: {path}")
        df = pd.read_csv(path)
        df["time"] = pd.to_datetime(df["time"], utc=True)
        return df.tail(limit).reset_index(drop=True)
