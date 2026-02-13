from app.data.providers.csv_provider import CSVCandleProvider
from app.indicators.calc import enrich_indicators

SUPPORTED_PAIRS = ["GBPJPY", "USDJPY", "USDCHF", "EURUSD", "EURJPY", "EURGBP"]
SUPPORTED_TIMEFRAMES = ["1H", "4H"]


class DataService:
    def __init__(self):
        self.provider = CSVCandleProvider()

    def load(self, pair: str, timeframe: str, limit: int = 500):
        df = self.provider.get_candles(pair, timeframe, limit=limit)
        return enrich_indicators(df)
