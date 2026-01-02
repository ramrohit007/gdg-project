import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import TeacherDashboard from './pages/TeacherDashboard'
import StudentDashboard from './pages/StudentDashboard'
import { AuthProvider, useAuth } from './context/AuthContext'

function ProtectedRoute({ children, requiredRole }: { children: React.ReactNode, requiredRole: 'teacher' | 'student' }) {
  const { user, loading } = useAuth()
  
  if (loading) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <div style={{ color: 'white', fontSize: '1.2rem' }}>Loading...</div>
    </div>
  }
  
  if (!user) {
    return <Navigate to="/login" />
  }
  
  if (user.role !== requiredRole) {
    return <Navigate to="/login" />
  }
  
  return <>{children}</>
}

function AppRoutes() {
  const { user } = useAuth()
  
  return (
    <Routes>
      <Route path="/login" element={!user ? <Login /> : <Navigate to={user.role === 'teacher' ? '/teacher' : '/student'} />} />
      <Route 
        path="/teacher" 
        element={
          <ProtectedRoute requiredRole="teacher">
            <TeacherDashboard />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/student" 
        element={
          <ProtectedRoute requiredRole="student">
            <StudentDashboard />
          </ProtectedRoute>
        } 
      />
      <Route path="/" element={<Navigate to="/login" />} />
    </Routes>
  )
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </Router>
  )
}

export default App

