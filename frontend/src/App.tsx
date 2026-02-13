import { Link, Route, Routes } from 'react-router-dom'
import { DashboardPage } from './pages/DashboardPage'
import { SettingsPage } from './pages/SettingsPage'
import { SignalDetailPage } from './pages/SignalDetailPage'

export default function App() {
  return <div style={{fontFamily:'sans-serif', padding:16}}>
    <nav style={{display:'flex', gap:12, marginBottom:12}}>
      <Link to='/'>Dashboard</Link>
      <Link to='/settings'>Settings</Link>
    </nav>
    <Routes>
      <Route path='/' element={<DashboardPage />} />
      <Route path='/signals/:id' element={<SignalDetailPage />} />
      <Route path='/settings' element={<SettingsPage />} />
    </Routes>
  </div>
}
