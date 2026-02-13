import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getSignal } from '../api/client'
import { RulesChecklist } from '../components/RulesChecklist'
import { SimResultsCard } from '../components/SimResultsCard'
import { TicketTable } from '../components/TicketTable'
import type { Signal } from '../types'

export function SignalDetailPage() {
  const { id } = useParams()
  const [signal, setSignal] = useState<Signal | null>(null)
  useEffect(() => { if (id) getSignal(Number(id)).then(setSignal) }, [id])
  if (!signal) return <p>Loading...</p>
  return <div>
    <h2>Signal Detail</h2>
    <p>{signal.pair} {signal.timeframe} {signal.strategy} {signal.direction} | State: {signal.state}</p>
    <h4>Chart panel (MVP placeholder)</h4>
    <pre>{JSON.stringify({ last_price: signal.last_price, overlays: signal.rule_values }, null, 2)}</pre>
    <h4>Rules Checklist</h4>
    <RulesChecklist checklist={signal.checklist} values={signal.rule_values} />
    <h4>Order Ticket</h4>
    <TicketTable ticket={signal.order_sheet} />
    <SimResultsCard sim={signal.backtest} />
  </div>
}
