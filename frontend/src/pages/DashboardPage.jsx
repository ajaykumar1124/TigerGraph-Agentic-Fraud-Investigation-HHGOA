import { Link } from 'react-router-dom'
import { 
  Activity, TrendingUp, AlertTriangle, CheckCircle, Clock, DollarSign, Eye
} from 'lucide-react'

export default function DashboardPage() {
  const stats = [
    {
      icon: Activity,
      label: 'Service Status',
      value: 'Online',
      change: 'All systems operational',
      color: '#10b981',
      bgColor: 'linear-gradient(135deg, #10b981, #059669)'
    },
    {
      icon: TrendingUp,
      label: 'Total Cases',
      value: '20',
      change: 'All hackathon cases',
      color: '#6366f1',
      bgColor: 'linear-gradient(135deg, #6366f1, #8b5cf6)'
    },
    {
      icon: AlertTriangle,
      label: 'Critical Alerts',
      value: '7',
      change: 'Requires action',
      color: '#ef4444',
      bgColor: 'linear-gradient(135deg, #ef4444, #dc2626)'
    },
    {
      icon: Clock,
      label: 'High Risk',
      value: '10',
      change: 'Under investigation',
      color: '#f59e0b',
      bgColor: 'linear-gradient(135deg, #f59e0b, #d97706)'
    },
    {
      icon: CheckCircle,
      label: 'False Positives',
      value: '3',
      change: 'Legitimate transactions',
      color: '#10b981',
      bgColor: 'linear-gradient(135deg, #10b981, #059669)'
    },
    {
      icon: DollarSign,
      label: 'Total at Risk',
      value: '₹9.8L',
      change: 'Across all cases',
      color: '#6366f1',
      bgColor: 'linear-gradient(135deg, #6366f1, #8b5cf6)'
    }
  ]

  const recentCases = [
    { id: 'HHG-001', title: 'Account Takeover - Impossible Travel', status: 'CRITICAL', confidence: 92, amount: '₹39,000', time: '2 hours ago' },
    { id: 'HHG-002', title: 'International Wire Transfer Fraud', status: 'CRITICAL', confidence: 94, amount: '₹45,000', time: '4 hours ago' },
    { id: 'HHG-003', title: 'Cryptocurrency Exchange Fraud', status: 'CRITICAL', confidence: 96, amount: '₹95,000', time: '6 hours ago' },
    { id: 'HHG-009', title: 'Business Email Compromise (BEC)', status: 'CRITICAL', confidence: 93, amount: '₹2.5L', time: '18 hours ago' },
    { id: 'HHG-018', title: 'ATM Skimming Device', status: 'CRITICAL', confidence: 94, amount: '₹67,000', time: '36 hours ago' }
  ]

  return (
    <div className="page-container">
      <div className="page-header">
        <div className="page-subtitle">Monitoring Overview</div>
        <h1 className="page-title">Fraud Operations Dashboard</h1>
      </div>

      <div className="stats-grid">
        {stats.map((stat, index) => (
          <div key={index} className="stat-card">
            <div className="stat-icon" style={{ background: stat.bgColor }}>
              <stat.icon size={24} />
            </div>
            <div className="stat-label">{stat.label}</div>
            <div className="stat-value">{stat.value}</div>
            <div className="stat-change">{stat.change}</div>
          </div>
        ))}
      </div>

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '1.5rem'
        }}>
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '0.25rem' }}>
              Recent High-Risk Cases
            </h2>
            <p style={{ color: 'var(--gray-600)', fontSize: '0.875rem' }}>
              Latest fraud detection alerts requiring attention
            </p>
          </div>
          <Link to="/cases" className="action-button secondary">
            View All Cases
          </Link>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {recentCases.map((case_) => (
            <Link
              key={case_.id}
              to={`/cases/${case_.id}`}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '1rem',
                background: 'white',
                border: '1px solid var(--gray-200)',
                borderRadius: '0.75rem',
                textDecoration: 'none',
                color: 'inherit',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = '#6366f1'
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(99, 102, 241, 0.1)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--gray-200)'
                e.currentTarget.style.boxShadow = 'none'
              }}
            >
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.875rem' }}>
                    {case_.id}
                  </span>
                  <span className="badge" style={{
                    background: case_.status === 'CRITICAL' 
                      ? 'linear-gradient(135deg, #ef4444, #dc2626)' 
                      : 'linear-gradient(135deg, #f59e0b, #d97706)',
                    color: 'white',
                    border: 'none'
                  }}>
                    {case_.status}
                  </span>
                </div>
                <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '0.5rem' }}>
                  {case_.title}
                </h3>
                <div style={{ 
                  display: 'flex', 
                  gap: '1rem',
                  fontSize: '0.875rem',
                  color: 'var(--gray-600)'
                }}>
                  <span>Confidence: <strong>{case_.confidence}%</strong></span>
                  <span>Amount: <strong>{case_.amount}</strong></span>
                  <span>{case_.time}</span>
                </div>
              </div>
              
              <button className="action-button primary" style={{ padding: '0.5rem 1rem' }}>
                <Eye size={16} />
                Investigate
              </button>
            </Link>
          ))}
        </div>
      </div>

      <div className="card">
        <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '1rem' }}>
          Quick Actions
        </h2>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '1rem'
        }}>
          <Link to="/investigations" className="action-button primary">
            New Investigation
          </Link>
          <Link to="/cases" className="action-button secondary">
            View All Cases
          </Link>
          <Link to="/reports" className="action-button secondary">
            Generate Report
          </Link>
        </div>
      </div>
    </div>
  )
}
