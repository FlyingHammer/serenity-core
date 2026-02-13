from abc import ABC, abstractmethod

import pandas as pd


class CandleProvider(ABC):
    @abstractmethod
    def get_candles(self, pair: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        raise NotImplementedError
