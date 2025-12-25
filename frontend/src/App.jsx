import React, { useState, useEffect } from 'react';
import { Activity, AlertTriangle, CheckCircle, Brain, Database, Globe } from 'lucide-react';
import './App.css';

function App() {
  const [safetyScore, setSafetyScore] = useState(95);
  const [alerts, setAlerts] = useState([]);
  const [reasoning, setReasoning] = useState([]);
  const [stats, setStats] = useState({
    documentsIndexed: 14,
    externalSourcesMonitored: 1,
    lastUpdate: new Date().toISOString()
  });

  // Simulate real-time updates (in production, this would be WebSocket)
  useEffect(() => {
    const interval = setInterval(() => {
      setStats(prev => ({
        ...prev,
        lastUpdate: new Date().toISOString()
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getScoreColor = (score) => {
    if (score >= 85) return '#10b981'; // Green
    if (score >= 70) return '#f59e0b'; // Yellow
    return '#ef4444'; // Red
  };

  const getScoreStatus = (score) => {
    if (score >= 85) return 'Healthy';
    if (score >= 70) return 'Warning';
    return 'Critical';
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <Activity size={32} />
            <h1>Bio-Watcher</h1>
          </div>
          <div className="subtitle">Agentic Clinical Intelligence</div>
        </div>
      </header>

      <div className="container">
        {/* Main Stats Grid */}
        <div className="stats-grid">
          {/* Safety Score Card */}
          <div className="card score-card">
            <h3>Safety Score</h3>
            <div className="score-display">
              <div 
                className="score-circle"
                style={{
                  background: `conic-gradient(${getScoreColor(safetyScore)} ${safetyScore * 3.6}deg, #e5e7eb 0deg)`
                }}
              >
                <div className="score-inner">
                  <div className="score-value">{safetyScore}</div>
                  <div className="score-status">{getScoreStatus(safetyScore)}</div>
                </div>
              </div>
            </div>
          </div>

          {/* Stats Cards */}
          <div className="card">
            <div className="stat-header">
              <Database size={24} />
              <h3>Documents Indexed</h3>
            </div>
            <div className="stat-value">{stats.documentsIndexed}</div>
            <div className="stat-label">Live monitoring active</div>
          </div>

          <div className="card">
            <div className="stat-header">
              <Globe size={24} />
              <h3>External Sources</h3>
            </div>
            <div className="stat-value">{stats.externalSourcesMonitored}</div>
            <div className="stat-label">WHO/FDA/CDC alerts</div>
          </div>

          <div className="card">
            <div className="stat-header">
              <Brain size={24} />
              <h3>Agent Status</h3>
            </div>
            <div className="stat-value">
              <CheckCircle size={32} color="#10b981" />
            </div>
            <div className="stat-label">Monitoring & Ready</div>
          </div>
        </div>

        {/* Alerts Section */}
        <div className="card alerts-section">
          <div className="section-header">
            <AlertTriangle size={24} />
            <h2>Active Alerts</h2>
          </div>
          
          {alerts.length === 0 ? (
            <div className="no-alerts">
              <CheckCircle size={48} color="#10b981" />
              <p>No active alerts. System monitoring normally.</p>
              <div className="demo-hint">
                💡 Run demo triggers to see real-time agent response
              </div>
            </div>
          ) : (
            <div className="alerts-list">
              {alerts.map((alert, idx) => (
                <div key={idx} className={`alert alert-${alert.severity}`}>
                  <div className="alert-header">
                    <AlertTriangle size={20} />
                    <span className="alert-title">{alert.title}</span>
                  </div>
                  <div className="alert-content">{alert.description}</div>
                  <div className="alert-time">
                    {new Date(alert.timestamp).toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Reasoning Trace */}
        <div className="card reasoning-section">
          <div className="section-header">
            <Brain size={24} />
            <h2>Agent Reasoning Trace</h2>
          </div>
          
          {reasoning.length === 0 ? (
            <div className="no-reasoning">
              <p>Waiting for agent activity...</p>
              <div className="pulse-indicator"></div>
            </div>
          ) : (
            <div className="reasoning-list">
              {reasoning.map((step, idx) => (
                <div key={idx} className="reasoning-step">
                  <div className="step-number">{idx + 1}</div>
                  <div className="step-content">{step}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* System Info */}
        <div className="card system-info">
          <h3>System Information</h3>
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">Last Update:</span>
              <span className="info-value">
                {new Date(stats.lastUpdate).toLocaleTimeString()}
              </span>
            </div>
            <div className="info-item">
              <span className="info-label">Vector Store:</span>
              <span className="info-value status-active">● Active</span>
            </div>
            <div className="info-item">
              <span className="info-label">Agent Mode:</span>
              <span className="info-value">Real-time Monitoring</span>
            </div>
            <div className="info-item">
              <span className="info-label">Demo Mode:</span>
              <span className="info-value status-active">● Enabled</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="footer">
        <p>🏥 Bio-Watcher - Eliminating the Knowledge Lag in Healthcare</p>
        <p className="footer-subtitle">
          Powered by Pathway Streaming Engine + LangGraph Agents
        </p>
      </footer>
    </div>
  );
}

export default App;
