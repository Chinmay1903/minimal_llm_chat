const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost' // '' when served by FastAPI


export async function getModels() {
    console.log('API_BASE:', API_BASE);
    
const r = await fetch(`${API_BASE}/api/models`)
if (!r.ok) throw new Error(`Failed to load models (${r.status})`)
return r.json()
}


export async function sendChat(payload) {
const r = await fetch(`${API_BASE}/api/chat`, {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify(payload)
})
if (!r.ok) {
const data = await r.json().catch(() => ({}))
throw new Error(data.detail || `Chat failed (${r.status})`)
}
return r.json()
}
