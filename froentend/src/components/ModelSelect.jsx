import React from 'react'


export default function ModelSelect({ models, value, onChange }) {
  return (
    <div>
      <label className="block mb-1 text-sm font-medium">Model</label>
      <select
        value={value}
        onChange={e => onChange(e.target.value)}
        className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">-- choose a model --</option>
        {models.map(m => (
          <option key={m.id} value={m.id}>
            {m.display_name} ({m.provider})
          </option>
        ))}
      </select>
    </div>
  )
}
