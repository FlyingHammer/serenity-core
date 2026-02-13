import { useEffect, useState } from 'react'
import { getSettings, saveSettings } from '../api/client'
import type { AppSettings } from '../types'

export function SettingsPage() {
  const [settings, setSettings] = useState<AppSettings | null>(null)
  useEffect(() => { getSettings().then(setSettings) }, [])
  if (!settings) return <p>Loading...</p>

  return <div>
    <h2>Settings</h2>
    <label>Account Size <input type='number' value={settings.risk.account_size} onChange={e => setSettings({...settings, risk:{...settings.risk, account_size:+e.target.value}})} /></label>
    <label>Risk % <input type='number' min={0.1} max={2} step={0.1} value={settings.risk.risk_pct} onChange={e => setSettings({...settings, risk:{...settings.risk, risk_pct:+e.target.value}})} /></label>
    <h4>MR params</h4>
    <label>CCI Extreme <input type='number' value={settings.mr.cci_extreme} onChange={e => setSettings({...settings, mr:{...settings.mr, cci_extreme:+e.target.value}})} /></label>
    <label>Entry timing <select value={settings.mr.entry_timing} onChange={e => setSettings({...settings, mr:{...settings.mr, entry_timing:e.target.value}})}><option value='close_confirm'>Option A</option><option value='intrabar'>Option B</option></select></label>
    <h4>TRL params</h4>
    <label>Squeeze threshold <input type='number' step={0.001} value={settings.trl.squeeze_bw_threshold} onChange={e => setSettings({...settings, trl:{...settings.trl, squeeze_bw_threshold:+e.target.value}})} /></label>
    <h4>Trailing defaults</h4>
    <label>Activation R <input type='number' step={0.1} value={settings.trl.trailing_activation_r} onChange={e => setSettings({...settings, trl:{...settings.trl, trailing_activation_r:+e.target.value}, mr:{...settings.mr, trailing_activation_r:+e.target.value}})} /></label>
    <label>Distance pips <input type='number' step={1} value={settings.trl.trailing_distance_pips} onChange={e => setSettings({...settings, trl:{...settings.trl, trailing_distance_pips:+e.target.value}, mr:{...settings.mr, trailing_distance_pips:+e.target.value}})} /></label>
    <label>Step pips <input type='number' step={1} value={settings.trl.trailing_step_pips} onChange={e => setSettings({...settings, trl:{...settings.trl, trailing_step_pips:+e.target.value}, mr:{...settings.mr, trailing_step_pips:+e.target.value}})} /></label>
    <div><button onClick={async()=>{ await saveSettings(settings); alert('Saved'); }}>Save</button></div>
  </div>
}
