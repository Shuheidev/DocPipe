import { useEffect, useState } from 'react'

function Demo() {
  const [docs, setDocs] = useState({})
  const base = import.meta.env.BASE_URL || '/'

  useEffect(() => {
    const load = async (file, key) => {
      const resp = await fetch(`${base}demo/${file}`)
      const text = await resp.text()
      return [key, text]
    }
    Promise.all([
      load('BRD.md', 'brd'),
      load('Solution.md', 'solution'),
      load('epics_userstories.yaml', 'backlog'),
      load('figma.json', 'figma'),
    ]).then((items) => {
      const obj = {}
      items.forEach(([k, v]) => (obj[k] = v))
      setDocs(obj)
    })
  }, [base])

  return (
    <div className="demo">
      <h2>Salesforce UI Example</h2>
      <p>
        Below is a set of mocked artefacts produced by DocPipe for a sample
        Salesforce custom UI component. These files are also available in the
        repository under <code>docs/salesforce_demo</code>.
      </p>
      <section>
        <h3>Business Requirement Document</h3>
        <pre>{docs.brd}</pre>
      </section>
      <section>
        <h3>Solution Outline</h3>
        <pre>{docs.solution}</pre>
      </section>
      <section>
        <h3>Backlog</h3>
        <pre>{docs.backlog}</pre>
      </section>
      <section>
        <h3>Figma Links</h3>
        <pre>{docs.figma}</pre>
      </section>
    </div>
  )
}

export default Demo
