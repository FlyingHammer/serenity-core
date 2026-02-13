# FX Scanner MVP

## Run
```bash
docker-compose up --build
```
- Backend: http://localhost:8000/docs
- Frontend: http://localhost:5173

## UI Pages
- Dashboard/Watchlist: sortable signal table (pair, timeframe, price, strategy, direction, state, confidence score)
- Signal Detail: rules checklist with underlying values, order ticket, and quick sim metrics
- Settings: account/risk, MR/TRL thresholds, and trailing defaults

## API Endpoints
- `GET /pairs`
- `GET /signals?pair=&timeframe=&strategy=`
- `GET /signals/{id}`
- `POST /scan`
- `GET /settings`
- `PUT /settings`

## Add a data provider
1. Implement `CandleProvider.get_candles(pair, timeframe, limit)`.
2. Return DataFrame columns: `time, open, high, low, close, volume(optional)`.
3. Wire provider in `backend/app/data/service.py`.

## Add pair/timeframe
1. Update constants in `backend/app/data/service.py`.
2. Add CSV files in `backend/data/{PAIR}_{TF}.csv` for MVP mode.

## Backtest assumptions
- Candle-level fills only.
- 5-candle max hold in quick sim.
- No spread/slippage.

## Known limitations
- CSV provider only by default.
- Pip value approximated for USD account.
- No real broker execution (alerts + order sheet only).
