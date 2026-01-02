import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Login.css'

function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [code, setCode] = useState('')
  const [role, setRole] = useState<'teacher' | 'student'>('teacher')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await login(username, password, role === 'student' ? code : undefined)
      navigate(role === 'teacher' ? '/teacher' : '/student')
    } catch (err: any) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Student Performance Analyzer</h1>
        <h2>Login</h2>
        
        <div className="role-selector">
          <button
            className={role === 'teacher' ? 'active' : ''}
            onClick={() => setRole('teacher')}
          >
            Teacher
          </button>
          <button
            className={role === 'student' ? 'active' : ''}
            onClick={() => setRole('student')}
          >
            Student
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              placeholder={role === 'teacher' ? 'teacher' : 'student1/student2/student3'}
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter password"
            />
          </div>

          {role === 'student' && (
            <div className="form-group">
              <label>Login Code (from teacher)</label>
              <input
                type="text"
                value={code}
                onChange={(e) => setCode(e.target.value.toUpperCase())}
                required
                placeholder="Enter code"
                maxLength={8}
              />
            </div>
          )}

          {error && <div className="error-message">{error}</div>}

          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="demo-info">
          <p><strong>Demo Accounts:</strong></p>
          <p>Teacher: username: <code>teacher</code>, password: <code>teacher123</code></p>
          <p>Students: username: <code>student1/student2/student3</code>, password: <code>student123</code></p>
        </div>
      </div>
    </div>
  )
}

export default Login

