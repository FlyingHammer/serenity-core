import { useMemo, useState } from 'react'
import type { Signal } from '../types'

export function SignalTable({ signals, onSelect }: { signals: Signal[]; onSelect: (s: Signal) => void }) {
  const [sortKey, setSortKey] = useState<keyof Signal>('confidence_score')
  const sorted = useMemo(
    () => [...signals].sort((a, b) => Number((b as any)[sortKey] ?? 0) - Number((a as any)[sortKey] ?? 0)),
    [signals, sortKey]
  )
  return (
    <table border={1} cellPadding={6}>
      <thead>
        <tr>
          {['pair', 'timeframe', 'last_price', 'strategy', 'direction', 'state', 'confidence_score'].map((k) => (
            <th key={k} onClick={() => setSortKey(k as keyof Signal)} style={{ cursor: 'pointer' }}>{k}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {sorted.map((s) => (
          <tr key={s.id} onClick={() => onSelect(s)} style={{ cursor: 'pointer' }}>
            <td>{s.pair}</td><td>{s.timeframe}</td><td>{s.last_price?.toFixed(5)}</td><td>{s.strategy}</td>
            <td>{s.direction ?? '-'}</td><td>{s.state}</td><td>{s.confidence_score}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
