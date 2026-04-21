import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { aiService } from '../services/api'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const { isAuthenticated, logout, user } = useAuth()
  const navigate = useNavigate()
  const [prompt, setPrompt] = useState('')
  const [systemPrompt, setSystemPrompt] = useState('')
  const [result, setResult] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login')
    }
  }, [isAuthenticated, navigate])

  const handleGenerate = async () => {
    if (!prompt.trim()) return
    setIsLoading(true)
    try {
      const data = await aiService.generate(
        prompt,
        systemPrompt || undefined,
        1000,
        0.7
      )
      setResult(data.result)
    } catch {
      toast.error('Generation failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h2>Welcome, {user?.full_name || user?.email || 'User'}</h2>
        <button onClick={logout}>Logout</button>
      </header>
      <main className="dashboard-content">
        <div className="ai-panel">
          <h3>AI Content Generator</h3>
          <div className="form-group">
            <label>System Prompt (optional)</label>
            <textarea
              value={systemPrompt}
              onChange={(e) => setSystemPrompt(e.target.value)}
              placeholder="Set the context for AI..."
            />
          </div>
          <div className="form-group">
            <label>Prompt</label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Enter your prompt..."
            />
          </div>
          <button onClick={handleGenerate} disabled={isLoading}>
            {isLoading ? 'Generating...' : 'Generate'}
          </button>
          {result && (
            <div className="result">
              <h4>Result:</h4>
              <p>{result}</p>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
