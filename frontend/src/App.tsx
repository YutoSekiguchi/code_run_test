import { useState } from 'react'
import './App.css'

const LANGUAGES = {
  python: 'Python',
  javascript: 'JavaScript',
  ruby: 'Ruby',
  php: 'PHP',
  perl: 'Perl',
  c: 'C',
  cpp: 'C++',
  java: 'Java'
} as const

type Language = keyof typeof LANGUAGES

function App() {
  const [language, setLanguage] = useState<Language>('python')
  const [code, setCode] = useState('')
  const [output, setOutput] = useState('')
  const [isRunning, setIsRunning] = useState(false)

  const runCode = async () => {
    setIsRunning(true)
    setOutput('')
    
    try {
      const response = await fetch('http://localhost:8000/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          language,
          code,
          deps: ''
        })
      })
      
      const result = await response.text()
      setOutput(result)
    } catch (error) {
      setOutput(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setIsRunning(false)
    }
  }

  return (
    <div className="app">
      <h1>Code Runner</h1>
      
      <div className="controls">
        <label>
          Language:
          <select 
            value={language} 
            onChange={(e) => setLanguage(e.target.value as Language)}
          >
            {Object.entries(LANGUAGES).map(([key, name]) => (
              <option key={key} value={key}>{name}</option>
            ))}
          </select>
        </label>
      </div>

      <div className="editor">
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Enter your code here..."
          rows={15}
          cols={80}
        />
      </div>

      <div className="run-section">
        <button 
          onClick={runCode} 
          disabled={isRunning || !code.trim()}
          className="run-button"
        >
          {isRunning ? 'Running...' : 'Run Code'}
        </button>
      </div>

      <div className="output">
        <h3>Output:</h3>
        <pre className="output-content">{output}</pre>
      </div>
    </div>
  )
}

export default App
