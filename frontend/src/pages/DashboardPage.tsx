import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getSignals, scan } from '../api/client'
import { SignalTable } from '../components/SignalTable'
import type { Signal } from '../types'

export function DashboardPage() {
  const [signals, setSignals] = useState<Signal[]>([])
  const nav = useNavigate()
  const load = () => getSignals().then(setSignals)
  useEffect(() => { load() }, [])

  return <div>
    <h2>Dashboard / Watchlist</h2>
    <button onClick={async () => { await scan(); await load() }}>Run Scan</button>
    <SignalTable signals={signals} onSelect={(s) => nav(`/signals/${s.id}`)} />
  </div>
}
