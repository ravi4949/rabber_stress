import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './auth/AuthContext';
import { RequireAuth } from './auth/RequireAuth';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { NewAnalysis } from './pages/NewAnalysis';
import { JobStatus } from './pages/JobStatus';
import { Results } from './pages/Results';

const NavigationBar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <nav style={{ background: '#0f172a', color: '#fff', padding: '14px 32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <Link to="/dashboard" style={{ color: '#fff', textDecoration: 'none', fontSize: '1.2rem', fontWeight: 700, letterSpacing: '-0.02em' }}>
        RubberStress <span style={{ fontSize: '0.75rem', fontWeight: 500, background: '#2563eb', padding: '2px 6px', borderRadius: '4px', marginLeft: '6px' }}>CANN</span>
      </Link>

      <div style={{ display: 'flex', alignItems: 'center', gap: '20px', fontSize: '0.9rem' }}>
        {isAuthenticated ? (
          <>
            <Link to="/dashboard" style={{ color: '#94a3b8', textDecoration: 'none', fontWeight: 500 }}>Dashboard</Link>
            <Link to="/analyses/new" style={{ color: '#94a3b8', textDecoration: 'none', fontWeight: 500 }}>+ New Analysis</Link>
            <span style={{ color: '#64748b', fontSize: '0.85rem' }}>{user?.email}</span>
            <button
              onClick={logout}
              style={{ background: 'none', border: '1px solid #334155', color: '#cbd5e1', padding: '4px 10px', borderRadius: '4px', cursor: 'pointer', fontSize: '0.85rem' }}
            >
              Sign Out
            </button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ color: '#94a3b8', textDecoration: 'none', fontWeight: 500 }}>Sign In</Link>
            <Link to="/register" style={{ color: '#fff', background: '#2563eb', textDecoration: 'none', fontWeight: 600, padding: '6px 12px', borderRadius: '4px' }}>Register</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <div style={{ minHeight: '100vh', background: '#f8fafc', fontFamily: 'system-ui, -apple-system, sans-serif', color: '#1e293b' }}>
          <NavigationBar />
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            <Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
            <Route path="/analyses/new" element={<RequireAuth><NewAnalysis /></RequireAuth>} />
            <Route path="/analyses/:runId/status" element={<RequireAuth><JobStatus /></RequireAuth>} />
            <Route path="/analyses/:runId/results" element={<RequireAuth><Results /></RequireAuth>} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;
