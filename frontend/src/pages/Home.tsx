import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="home">
      <header className="hero">
        <h1>AI + React + Supabase MVP</h1>
        <p>Build and deploy AI-powered applications with modern tech stack</p>
        <div className="cta-buttons">
          <Link to="/register" className="btn btn-primary">
            Get Started
          </Link>
          <Link to="/login" className="btn btn-secondary">
            Login
          </Link>
        </div>
      </header>
    </div>
  )
}
