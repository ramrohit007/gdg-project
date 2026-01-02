import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import axios from 'axios'
import './StudentDashboard.css'

function StudentDashboard() {
  const { user, logout } = useAuth()
  const [uploading, setUploading] = useState(false)
  const [uploadMessage, setUploadMessage] = useState('')
  const [scores, setScores] = useState<Record<string, number> | null>(null)

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    setUploadMessage('')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('/api/student/upload-answer', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setUploadMessage('Answer sheet uploaded and analyzed successfully!')
      setScores(response.data.scores)
    } catch (error: any) {
      setUploadMessage(`Error: ${error.response?.data?.detail || 'Upload failed'}`)
      setScores(null)
    } finally {
      setUploading(false)
      e.target.value = '' // Reset input
    }
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Student Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {user?.username}</span>
          <button onClick={logout} className="logout-btn">Logout</button>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="dashboard-section">
          <h2>Upload Answer Sheet</h2>
          <p className="section-description">
            Upload your exam answer sheet in PDF format. The system will analyze your answers
            and evaluate your understanding of different topics.
          </p>
          
          <div className="upload-section">
            <label className="file-upload-label">
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileUpload}
                disabled={uploading}
                className="file-input"
              />
              <span className="file-upload-button">
                {uploading ? 'Uploading and Analyzing...' : 'Choose PDF File'}
              </span>
            </label>
            
            {uploadMessage && (
              <div className={`upload-message ${uploadMessage.includes('Error') ? 'error' : 'success'}`}>
                {uploadMessage}
              </div>
            )}

            {scores && (
              <div className="scores-display">
                <h3>Your Topic Scores</h3>
                <div className="scores-grid">
                  {Object.entries(scores).map(([topic, score]) => (
                    <div key={topic} className="score-card">
                      <div className="score-topic">{topic}</div>
                      <div className="score-value">{score.toFixed(1)}%</div>
                      <div className="score-bar">
                        <div 
                          className="score-bar-fill" 
                          style={{ width: `${score}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="dashboard-section">
          <h2>Instructions</h2>
          <ul className="instructions-list">
            <li>Make sure your answer sheet is in PDF format</li>
            <li>The PDF should contain clear, readable text</li>
            <li>Upload one answer sheet at a time</li>
            <li>Wait for the analysis to complete before uploading another</li>
            <li>Your scores will be displayed after successful upload</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default StudentDashboard

