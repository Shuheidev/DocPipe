import { useState } from 'react'
import './App.css'

function App() {
  const [form, setForm] = useState({ project_name: '', description: '' })
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const resp = await fetch(`${import.meta.env.VITE_API_URL || ''}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (!resp.ok) throw new Error('Request failed')
      const data = await resp.json()
      setResults(data)
    } catch (err) {
      setResults({ error: err.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>DocPipe</h1>
      <form onSubmit={submit}>
        <input
          name="project_name"
          placeholder="Project Name"
          value={form.project_name}
          onChange={handleChange}
          required
        />
        <textarea
          name="description"
          placeholder="Description"
          value={form.description}
          onChange={handleChange}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Docs'}
        </button>
      </form>
      {results && (
        <div className="results">
          <h2>Results</h2>
          <ul>
            {Array.isArray(results) ? (
              results.map((r) => (
                <li key={r.artefact_type}>
                  {r.artefact_type}: <a href={r.path}>{r.path}</a>
                </li>
              ))
            ) : (
              <pre>{JSON.stringify(results, null, 2)}</pre>
            )}
          </ul>
        </div>
      )}
    </div>
  )
}

export default App
