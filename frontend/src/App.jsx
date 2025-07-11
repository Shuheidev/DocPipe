import { useState } from 'react'
import Demo from './Demo'
import './App.css'

function App() {
  const [form, setForm] = useState({ project_name: '', description: '' })
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [view, setView] = useState('generate')

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
      if (!resp.ok) {
        let message = 'Request failed'
        try {
          const err = await resp.json()
          message = err.error || err.detail || JSON.stringify(err)
        } catch {
          try {
            message = await resp.text()
        } catch {
          /* ignore parsing error */
        }
        }
        throw new Error(message)
      }
      const data = await resp.json()
      setResults(data)
    } catch (err) {
      setResults({ error: 'Failed to generate docs', details: err.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>DocPipe</h1>
      <nav className="tabs">
        <button onClick={() => setView('generate')} disabled={view==='generate'}>
          Generate
        </button>
        <button onClick={() => setView('demo')} disabled={view==='demo'}>
          Example
        </button>
      </nav>
      {view === 'generate' && (
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
      )}
      {view === 'generate' && results && (
        <div className="results">
          <h2>Results</h2>
          {Array.isArray(results) ? (
            <ul>
              {results.map((r) => (
                <li key={r.artefact_type}>
                  {r.artefact_type}: <a href={r.path}>{r.path}</a>
                </li>
              ))}
            </ul>
          ) : (
            <div className="error">
              <p>{results.error}</p>
              {results.details && (
                <details>
                  <summary>Details</summary>
                  <pre>{results.details}</pre>
                </details>
              )}
            </div>
          )}
        </div>
      )}
      {view === 'demo' && <Demo />}
    </div>
  )
}

export default App
