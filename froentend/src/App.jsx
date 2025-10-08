import React, { useEffect, useState } from 'react'
import ModelSelect from './components/ModelSelect.jsx';
import ChatBox from './components/ChatBox.jsx';
import { getModels, sendChat } from './api.js';


export default function App() {
    const [models, setModels] = useState([])
    const [selected, setSelected] = useState('')
    const [message, setMessage] = useState('')
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState('')


    useEffect(() => {
        getModels().then(setModels).catch(e => setError(e.message || 'Failed to load models'))
    }, [])


    const onSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setResult(null)
        if (!selected || !message.trim()) {
            setError('Pick a model and enter a message.')
            return
        }
        setLoading(true)
        try {
            const r = await sendChat({ model_id: selected, message })
            setResult(r)
        } catch (e) {
            setError(e.message || 'Chat failed')
        } finally {
            setLoading(false)
        }
    }


    return (
        <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-2xl font-semibold mb-1">Plumloom LLM Chat</h1>
      <p className="text-sm text-gray-500 mb-4">Minimal full-stack demo (FastAPI + React)</p>

      <form onSubmit={onSubmit} className="grid gap-3">
        <ModelSelect models={models} value={selected} onChange={setSelected} />
        <ChatBox value={message} onChange={setMessage} loading={loading} />
        <button
          type="submit"
          disabled={loading}
          className="inline-flex items-center justify-center rounded-lg bg-blue-600 text-white px-4 py-2 disabled:opacity-60 hover:bg-blue-700 transition"
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>

      {error && (
        <div className="mt-4 rounded-lg border border-red-300 bg-red-50 p-3 text-red-800">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-4 rounded-lg border border-gray-200 p-4">
          <h3 className="text-lg font-medium mb-2">Response</h3>
          <p className="whitespace-pre-wrap">{result.response}</p>
          <hr className="my-3" />
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
            <div><span className="font-semibold">Input tokens:</span> {result.input_tokens}</div>
            <div><span className="font-semibold">Output tokens:</span> {result.output_tokens}</div>
            <div><span className="font-semibold">Cost (USD):</span> ${result.cost.toFixed(6)}</div>
          </div>
        </div>
      )}
    </div>
  )
}
