import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import axios from 'axios'
import AnalyticsChart from '../components/AnalyticsChart'
import './TeacherDashboard.css'

interface TopicAverage {
  topic_id: number
  topic_name: string
  average_score: number
}

function TeacherDashboard() {
  const { user, logout } = useAuth()
  const [code, setCode] = useState<string | null>(null)
  const [codeExpires, setCodeExpires] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [analytics, setAnalytics] = useState<TopicAverage[]>([])
  const [uploading, setUploading] = useState(false)
  const [uploadMessage, setUploadMessage] = useState('')

  useEffect(() => {
    fetchCurrentCode()
    fetchAnalytics()
  }, [])

  const fetchCurrentCode = async () => {
    try {
      const response = await axios.get('/api/teacher/current-code')
      if (response.data) {
        setCode(response.data.code)
        setCodeExpires(response.data.expires_at)
      }
    } catch (error) {
      console.error('Error fetching code:', error)
    }
  }

  const generateCode = async () => {
    setLoading(true)
    try {
      const response = await axios.post('/api/teacher/generate-code')
      setCode(response.data.code)
      setCodeExpires(response.data.expires_at)
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to generate code')
    } finally {
      setLoading(false)
    }
  }

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get('/api/teacher/analytics')
      setAnalytics(response.data.topic_averages)
    } catch (error) {
      console.error('Error fetching analytics:', error)
    }
  }

  const handleSyllabusUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    setUploadMessage('')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('/api/teacher/upload-syllabus', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setUploadMessage(`Syllabus uploaded successfully! Extracted ${response.data.topics.length} topics.`)
      fetchAnalytics()
    } catch (error: any) {
      setUploadMessage(`Error: ${error.response?.data?.detail || 'Upload failed'}`)
    } finally {
      setUploading(false)
      e.target.value = '' // Reset input
    }
  }

  const formatExpiry = (expiresAt: string | null) => {
    if (!expiresAt) return ''
    const date = new Date(expiresAt)
    return date.toLocaleString()
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Teacher Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {user?.username}</span>
          <button onClick={logout} className="logout-btn">Logout</button>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="dashboard-section">
          <h2>Student Login Code</h2>
          <div className="code-section">
            {code ? (
              <div className="code-display">
                <div className="code-value">{code}</div>
                <div className="code-expiry">
                  Expires: {formatExpiry(codeExpires)}
                </div>
              </div>
            ) : (
              <p className="no-code">No active code. Generate one for students to login.</p>
            )}
            <button onClick={generateCode} disabled={loading} className="generate-btn">
              {loading ? 'Generating...' : code ? 'Regenerate Code' : 'Generate Code'}
            </button>
            <p className="code-info">Code is valid for 1 hour</p>
          </div>
        </div>

        <div className="dashboard-section">
          <h2>Upload Syllabus</h2>
          <div className="upload-section">
            <label className="file-upload-label">
              <input
                type="file"
                accept=".pdf"
                onChange={handleSyllabusUpload}
                disabled={uploading}
                className="file-input"
              />
              <span className="file-upload-button">
                {uploading ? 'Uploading...' : 'Choose PDF File'}
              </span>
            </label>
            {uploadMessage && (
              <div className={`upload-message ${uploadMessage.includes('Error') ? 'error' : 'success'}`}>
                {uploadMessage}
              </div>
            )}
          </div>
        </div>

        <div className="dashboard-section">
          <h2>Class Performance Analytics</h2>
          <p className="section-description">
            Average scores per topic across all students in the class.
          </p>
          {analytics.length === 0 ? (
            <p className="no-data">No analytics data available. Upload a syllabus and wait for students to submit answers.</p>
          ) : (
            <div className="analytics-container">
              <AnalyticsChart data={analytics} />
              <div className="analytics-table">
                <h3>Topic Average Scores</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Topic</th>
                      <th>Average Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {analytics.map((topic) => (
                      <tr key={topic.topic_id}>
                        <td>{topic.topic_name}</td>
                        <td>{topic.average_score.toFixed(2)}%</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default TeacherDashboard

