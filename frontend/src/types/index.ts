export type SignalState = 'NONE' | 'WATCH' | 'SETUP' | 'CONFIRMED' | 'TRIGGERED'

export interface Signal {
  id: number
  pair: string
  timeframe: string
  strategy: 'MR' | 'TRL'
  direction?: 'LONG' | 'SHORT'
  state: SignalState
  entry_type?: 'market' | 'limit'
  entry_price?: number
  sl_price?: number
  tp_price?: number
  sl_pips?: number
  tp_pips?: number
  confidence_score: number
  last_price: number
  checklist: Record<string, boolean>
  rule_values: Record<string, number | string | boolean>
  order_sheet?: any
  backtest?: any
  trailing?: any
}

export interface AppSettings {
  risk: { account_size: number; risk_pct: number }
  mr: Record<string, any>
  trl: Record<string, any>
}
