export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export async function api(path: string, options: RequestInit = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
  const headers: Record<string, string> = { 'Content-Type': 'application/json', ...(options.headers as any || {}) }
  if (token) headers.Authorization = `Bearer ${token}`
  const res = await fetch(`${API_URL}${path}`, { ...options, headers })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}
