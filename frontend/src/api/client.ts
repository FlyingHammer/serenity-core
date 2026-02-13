import axios from 'axios'
import type { AppSettings, Signal } from '../types'

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000' })

export const getPairs = () => api.get('/pairs').then(r => r.data)
export const getSignals = (params?: { pair?: string; timeframe?: string; strategy?: string }) => api.get<Signal[]>('/signals', { params }).then(r => r.data)
export const getSignal = (id: number) => api.get<Signal>(`/signals/${id}`).then(r => r.data)
export const scan = () => api.post('/scan').then(r => r.data)
export const getSettings = () => api.get<AppSettings>('/settings').then(r => r.data)
export const saveSettings = (payload: AppSettings) => api.put('/settings', payload).then(r => r.data)
