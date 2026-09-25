import { TrendingUp, TrendingDown, Activity, DollarSign, Users, AlertTriangle } from 'lucide-react'

export default function AnalyticsPage() {
  const metrics = [
    { 
      label: 'Total Fraud Cases', 
      value: '234', 
      change: '+12%', 
      trend: 'up',
      icon: AlertTriangle,
      color: '#ef4444'
    },
    { 
      label: 'Prevention Rate', 
      value: '94.2%', 
      change: '+5.2%', 
      trend: 'up',
      icon: Activity,
      color: '#10b981'
    },
    { 
      label: 'Amount Saved', 
      value: '₹12.4M', 
      change: '+23%', 
      trend: 'up',
      icon: DollarSign,
      color: '#6366f1'
    },
    { 
      label: 'Active Users', 
      value: '1,423', 
      change: '-2%', 
      trend: 'down',
      icon: Users,
      color: '#f59e0b'
    }
  ]

  const fraudTypes = [
    { type: 'Card Fraud', cases: 89, percentage: 38, color: '#ef4444' },
    { type: 'Identity Theft', cases: 67, percentage: 29, color: '#f59e0b' },
    { type: 'Wire Transfer', cases: 45, percentage: 19, color: '#6366f1' },
    { type: 'Phishing', cases: 33, percentage: 14, color: '#ec4899' }
  ]

  const monthlyTrends = [
    { month: 'Jan', detected: 45, prevented: 42, amount: 2.1 },
    { month: 'Feb', detected: 52, prevented: 48, amount: 2.4 },
    { month: 'Mar', detected: 48, prevented: 45, amount: 2.2 },
    { month: 'Apr', detected: 61, prevented: 57, amount: 2.8 },
    { month: 'May', detected: 55, prevented: 52, amount: 2.5 },
    { month: 'Jun', detected: 58, prevented: 54, amount: 2.7 }
  ]

  const riskDistribution = [
    { level: 'Critical', count: 34, color: '#ef4444' },
    { level: 'High', count: 67, color: '#f59e0b' },
    { level: 'Medium', count: 89, color: '#6366f1' },
    { level: 'Low', count: 44, color: '#10b981' }
  ]

  return (
    <div className="page-container">
      <div className="page-header">
        <div className="page-subtitle">Data Insights</div>
        <h1 className="page-title">Fraud Analytics</h1>
        <p style={{ color: '#111827', fontSize: '0.9375rem', fontWeight: 500 }}>
          Comprehensive fraud detection analytics and trends
        </p>
      </div>

      {/* Key Metrics */}
      <div className="stats-grid">
        {metrics.map((metric, index) => (
          <div key={index} className="stat-card">
            <div className="stat-icon" style={{ background: metric.color }}>
              <metric.icon size={24} color="white" />
            </div>
            <div className="stat-label" style={{ color: '#111827' }}>{metric.label}</div>
            <div className="stat-value" style={{ color: '#111827' }}>{metric.value}</div>
            <div className="stat-change" style={{ 
              color: metric.trend === 'up' ? '#10b981' : '#ef4444',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: '0.25rem'
            }}>
              {metric.trend === 'up' ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
              {metric.change}
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>
        {/* Fraud Types Distribution */}
        <div className="card">
          <h2 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#111827', marginBottom: '1.5rem' }}>
            Fraud Types Distribution
          </h2>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {fraudTypes.map((item, index) => (
              <div key={index}>
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  marginBottom: '0.5rem',
                  color: '#111827'
                }}>
                  <span style={{ fontWeight: 600, fontSize: '0.9375rem' }}>{item.type}</span>
                  <span style={{ fontWeight: 700 }}>{item.cases} cases ({item.percentage}%)</span>
                </div>
                <div style={{ 
                  height: '8px', 
                  background: '#e5e7eb', 
                  borderRadius: '9999px',
                  overflow: 'hidden'
                }}>
                  <div style={{ 
                    height: '100%', 
                    width: `${item.percentage}%`,
                    background: item.color,
                    transition: 'width 0.5s ease'
                  }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Risk Level Distribution */}
        <div className="card">
          <h2 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#111827', marginBottom: '1.5rem' }}>
            Risk Level Distribution
          </h2>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {riskDistribution.map((item, index) => (
              <div key={index} style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '1rem',
                background: `${item.color}10`,
                border: `1px solid ${item.color}30`,
                borderRadius: '0.75rem'
              }}>
                <div>
                  <div style={{ 
                    fontSize: '0.875rem', 
                    fontWeight: 700, 
                    color: '#111827',
                    textTransform: 'uppercase',
                    marginBottom: '0.25rem'
                  }}>
                    {item.level}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#6b7280', fontWeight: 600 }}>
                    Risk Level
                  </div>
                </div>
                <div style={{ 
                  fontSize: '2rem', 
                  fontWeight: 800, 
                  color: item.color
                }}>
                  {item.count}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Monthly Trends */}
      <div className="card" style={{ marginTop: '1.5rem' }}>
        <h2 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#111827', marginBottom: '1.5rem' }}>
          Monthly Fraud Detection Trends
        </h2>
        
        <div style={{ overflowX: 'auto' }}>
          <div style={{ display: 'flex', gap: '1.5rem', minWidth: '600px', padding: '1rem 0' }}>
            {monthlyTrends.map((month, index) => {
              const maxValue = Math.max(...monthlyTrends.map(m => m.detected))
              const detectedHeight = (month.detected / maxValue) * 200
              const preventedHeight = (month.prevented / maxValue) * 200
              
              return (
                <div key={index} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <div style={{ 
                    display: 'flex', 
                    gap: '0.5rem', 
                    alignItems: 'flex-end',
                    height: '200px',
                    marginBottom: '1rem'
                  }}>
                    <div style={{
                      width: '40px',
                      height: `${detectedHeight}px`,
                      background: 'linear-gradient(180deg, #ef4444, #dc2626)',
                      borderRadius: '0.375rem',
                      transition: 'height 0.5s ease',
                      position: 'relative'
                    }}>
                      <div style={{
                        position: 'absolute',
                        top: '-1.5rem',
                        left: '50%',
                        transform: 'translateX(-50%)',
                        fontSize: '0.75rem',
                        fontWeight: 700,
                        color: '#111827',
                        whiteSpace: 'nowrap'
                      }}>
                        {month.detected}
                      </div>
                    </div>
                    <div style={{
                      width: '40px',
                      height: `${preventedHeight}px`,
                      background: 'linear-gradient(180deg, #10b981, #059669)',
                      borderRadius: '0.375rem',
                      transition: 'height 0.5s ease',
                      position: 'relative'
                    }}>
                      <div style={{
                        position: 'absolute',
                        top: '-1.5rem',
                        left: '50%',
                        transform: 'translateX(-50%)',
                        fontSize: '0.75rem',
                        fontWeight: 700,
                        color: '#111827',
                        whiteSpace: 'nowrap'
                      }}>
                        {month.prevented}
                      </div>
                    </div>
                  </div>
                  
                  <div style={{ 
                    fontSize: '0.875rem', 
                    fontWeight: 700, 
                    color: '#111827',
                    marginBottom: '0.25rem'
                  }}>
                    {month.month}
                  </div>
                  <div style={{ 
                    fontSize: '0.75rem', 
                    color: '#6b7280',
                    fontWeight: 600
                  }}>
                    ₹{month.amount}M
                  </div>
                </div>
              )
            })}
          </div>
        </div>
        
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          gap: '2rem', 
          marginTop: '1.5rem',
          paddingTop: '1rem',
          borderTop: '1px solid #e5e7eb'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ 
              width: '16px', 
              height: '16px', 
              background: 'linear-gradient(135deg, #ef4444, #dc2626)',
              borderRadius: '0.25rem'
            }} />
            <span style={{ fontSize: '0.875rem', color: '#111827', fontWeight: 600 }}>Detected</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ 
              width: '16px', 
              height: '16px', 
              background: 'linear-gradient(135deg, #10b981, #059669)',
              borderRadius: '0.25rem'
            }} />
            <span style={{ fontSize: '0.875rem', color: '#111827', fontWeight: 600 }}>Prevented</span>
          </div>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="card" style={{ marginTop: '1.5rem' }}>
        <h2 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#111827', marginBottom: '1.5rem' }}>
          Performance Summary
        </h2>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '0.75rem', color: '#6b7280', fontWeight: 600, textTransform: 'uppercase', marginBottom: '0.5rem' }}>
              Detection Rate
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: 800, color: '#111827' }}>
              96.8%
            </div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '0.75rem', color: '#6b7280', fontWeight: 600, textTransform: 'uppercase', marginBottom: '0.5rem' }}>
              Avg Response Time
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: 800, color: '#111827' }}>
              2.3s
            </div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '0.75rem', color: '#6b7280', fontWeight: 600, textTransform: 'uppercase', marginBottom: '0.5rem' }}>
              False Positive Rate
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: 800, color: '#111827' }}>
              3.2%
            </div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '0.75rem', color: '#6b7280', fontWeight: 600, textTransform: 'uppercase', marginBottom: '0.5rem' }}>
              Total Cases
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: 800, color: '#111827' }}>
              234
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
