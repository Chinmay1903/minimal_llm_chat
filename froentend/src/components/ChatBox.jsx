import React from 'react'

export default function ChatBox({ value, onChange, loading }) {
  return (
    <div>
      <label className="block mb-1 text-sm font-medium">Your message</label>
      <textarea
        rows={5}
        value={value}
        onChange={e => onChange(e.target.value)}
        className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Ask anything..."
        disabled={loading}
      />
    </div>
  )
}
