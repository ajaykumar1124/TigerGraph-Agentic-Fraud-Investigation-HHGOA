import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Search, Filter, Eye, AlertTriangle, TrendingUp, Clock } from 'lucide-react'

export default function CasesPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('ALL')

  // All 20 hackathon cases loaded from cases/ folder
  const cases = [
    { id: 'HHG-001', customer: 'USR_0001', title: 'Account Takeover - Impossible Travel', risk: 92, status: 'CRITICAL', amount: 39000, transactions: 4, time: '2 hours ago' },
    { id: 'HHG-002', customer: 'USR_0002', title: 'International Wire Transfer Fraud', risk: 94, status: 'CRITICAL', amount: 45000, transactions: 4, time: '4 hours ago' },
    { id: 'HHG-003', customer: 'USR_0003', title: 'Cryptocurrency Exchange Fraud', risk: 96, status: 'CRITICAL', amount: 95000, transactions: 4, time: '6 hours ago' },
    { id: 'HHG-004', customer: 'USR_0004', title: 'Early Morning ATM Withdrawal', risk: 89, status: 'HIGH', amount: 35000, transactions: 4, time: '8 hours ago' },
    { id: 'HHG-005', customer: 'USR_0005', title: 'Rapid Succession Transfers', risk: 75, status: 'HIGH', amount: 24500, transactions: 4, time: '10 hours ago' },
    { id: 'HHG-006', customer: 'USR_0006', title: 'False Positive - Legitimate Business', risk: 45, status: 'LOW', amount: 0, transactions: 4, time: '12 hours ago' },
    { id: 'HHG-007', customer: 'USR_0007', title: 'Card Present Fraud - Stolen Card', risk: 91, status: 'HIGH', amount: 8000, transactions: 4, time: '14 hours ago' },
    { id: 'HHG-008', customer: 'USR_0008', title: 'E-commerce Fraud - Account Takeover', risk: 88, status: 'HIGH', amount: 15000, transactions: 4, time: '16 hours ago' },
    { id: 'HHG-009', customer: 'USR_0009', title: 'Business Email Compromise (BEC)', risk: 93, status: 'CRITICAL', amount: 250000, transactions: 4, time: '18 hours ago' },
    { id: 'HHG-010', customer: 'USR_0010', title: 'Phishing Attack - Credential Theft', risk: 87, status: 'HIGH', amount: 12000, transactions: 4, time: '20 hours ago' },
    { id: 'HHG-011', customer: 'USR_0011', title: 'False Positive - Customer Traveling', risk: 38, status: 'LOW', amount: 0, transactions: 4, time: '22 hours ago' },
    { id: 'HHG-012', customer: 'USR_0012', title: 'Money Mule Activity', risk: 90, status: 'HIGH', amount: 75000, transactions: 4, time: '24 hours ago' },
    { id: 'HHG-013', customer: 'USR_0013', title: 'Check Fraud - Altered Check', risk: 85, status: 'HIGH', amount: 5500, transactions: 4, time: '26 hours ago' },
    { id: 'HHG-014', customer: 'USR_0014', title: 'SIM Swap Attack', risk: 92, status: 'CRITICAL', amount: 28000, transactions: 4, time: '28 hours ago' },
    { id: 'HHG-015', customer: 'USR_0015', title: 'Insider Fraud - Employee Abuse', risk: 78, status: 'HIGH', amount: 18000, transactions: 4, time: '30 hours ago' },
    { id: 'HHG-016', customer: 'USR_0016', title: 'False Positive - Large Purchase', risk: 42, status: 'LOW', amount: 0, transactions: 4, time: '32 hours ago' },
    { id: 'HHG-017', customer: 'USR_0017', title: 'Romance Scam - Social Engineering', risk: 89, status: 'HIGH', amount: 45000, transactions: 4, time: '34 hours ago' },
    { id: 'HHG-018', customer: 'USR_0018', title: 'ATM Skimming Device', risk: 94, status: 'CRITICAL', amount: 67000, transactions: 4, time: '36 hours ago' },
    { id: 'HHG-019', customer: 'USR_0019', title: 'Synthetic Identity Fraud', risk: 86, status: 'HIGH', amount: 32000, transactions: 4, time: '38 hours ago' },
    { id: 'HHG-020', customer: 'USR_0020', title: 'Ransomware Payment', risk: 91, status: 'CRITICAL', amount: 150000, transactions: 4, time: '40 hours ago' }
  ]

  const filteredCases = cases.filter(c => {
    const matchesSearch = c.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         c.customer.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         c.title.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === 'ALL' || c.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const getStatusColor = (status) => {
    const colors = {
      'CRITICAL': { bg: 'linear-gradient(135deg, #ef4444, #dc2626)', text: 'white' },
      'HIGH': { bg: 'linear-gradient(135deg, #f59e0b, #d97706)', text: 'white' },
      'MEDIUM': { bg: 'linear-gradient(135deg, #6366f1, #4f46e5)', text: 'white' },
      'LOW': { bg: 'linear-gradient(135deg, #10b981, #059669)', text: 'white' }
    }
    return colors[status] || colors['MEDIUM']
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <div className="page-subtitle">Case Management</div>
        <h1 className="page-title">Fraud Cases</h1>
        <p style={{ color: '#111827', fontSize: '0.9375rem', fontWeight: 500 }}>
          Monitor and investigate all fraud detection cases
        </p>
      </div>

      {/* Stats */}
      <div className="stats-grid" style={{ marginBottom: '1.5rem' }}>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}>
            <TrendingUp size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Total Cases</div>
          <div className="stat-value" style={{ color: '#111827' }}>20</div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>
            All hackathon cases loaded
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #ef4444, #dc2626)' }}>
            <AlertTriangle size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Critical</div>
          <div className="stat-value" style={{ color: '#ef4444' }}>7</div>
          <div className="stat-change" style={{ color: '#ef4444', fontWeight: 600 }}>
            Requires immediate action
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f59e0b, #d97706)' }}>
            <Clock size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>High Risk</div>
          <div className="stat-value" style={{ color: '#111827' }}>10</div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>
            Under investigation
          </div>
        </div>
      </div>

      {/* Search & Filters */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: '250px', position: 'relative' }}>
            <Search size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: '#6b7280' }} />
            <input
              type="text"
              placeholder="Search cases..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ paddingLeft: '2.5rem', color: '#111827', fontWeight: 500 }}
            />
          </div>
          
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            style={{ minWidth: '150px', color: '#111827', fontWeight: 600 }}
          >
            <option value="ALL">All Status</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>
          
          <button className="action-button secondary">
            <Filter size={18} />
            More Filters
          </button>
        </div>
      </div>

      {/* Cases Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))', gap: '1.5rem' }}>
        {filteredCases.map((case_) => {
          const statusStyle = getStatusColor(case_.status)
          return (
            <div key={case_.id} className="card" style={{ cursor: 'pointer', transition: 'all 0.2s' }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)'
                e.currentTarget.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.12)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)'
                e.currentTarget.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.06)'
              }}
            >
              {/* Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
                <div>
                  <div style={{ fontSize: '0.875rem', fontWeight: 700, color: '#111827', marginBottom: '0.25rem' }}>
                    {case_.id}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#6b7280', fontWeight: 600 }}>
                    Customer: {case_.customer}
                  </div>
                </div>
                <span style={{
                  padding: '0.375rem 0.75rem',
                  background: statusStyle.bg,
                  color: statusStyle.text,
                  borderRadius: '9999px',
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  textTransform: 'uppercase'
                }}>
                  {case_.status}
                </span>
              </div>

              {/* Title */}
              <h3 style={{ 
                fontSize: '1rem', 
                fontWeight: 700, 
                color: '#111827', 
                marginBottom: '1rem',
                lineHeight: 1.4
              }}>
                {case_.title}
              </h3>

              {/* Risk Score */}
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  marginBottom: '0.5rem',
                  fontSize: '0.875rem'
                }}>
                  <span style={{ color: '#111827', fontWeight: 600 }}>Risk Score</span>
                  <span style={{ color: '#ef4444', fontWeight: 700 }}>{case_.risk}%</span>
                </div>
                <div style={{ height: '8px', background: '#e5e7eb', borderRadius: '9999px', overflow: 'hidden' }}>
                  <div style={{ 
                    height: '100%', 
                    width: `${case_.risk}%`,
                    background: case_.risk >= 90 ? '#ef4444' : '#f59e0b',
                    transition: 'width 0.5s ease'
                  }} />
                </div>
              </div>

              {/* Details */}
              <div style={{ 
                display: 'grid',
                gridTemplateColumns: 'repeat(2, 1fr)',
                gap: '0.75rem',
                marginBottom: '1rem',
                padding: '0.75rem',
                background: '#f9fafb',
                borderRadius: '0.5rem'
              }}>
                <div>
                  <div style={{ fontSize: '0.75rem', color: '#6b7280', fontWeight: 600, marginBottom: '0.25rem' }}>
                    Amount
                  </div>
                  <div style={{ fontSize: '0.9375rem', fontWeight: 700, color: '#111827' }}>
                    ₹{case_.amount.toLocaleString()}
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: '0.75rem', color: '#6b7280', fontWeight: 600, marginBottom: '0.25rem' }}>
                    Transactions
                  </div>
                  <div style={{ fontSize: '0.9375rem', fontWeight: 700, color: '#111827' }}>
                    {case_.transactions}
                  </div>
                </div>
              </div>

              {/* Footer */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.875rem', color: '#6b7280', fontWeight: 600 }}>
                  {case_.time}
                </span>
                <Link to={`/cases/${case_.id}`} className="action-button primary" style={{ padding: '0.5rem 1rem' }}>
                  <Eye size={16} />
                  Investigate
                </Link>
              </div>
            </div>
          )
        })}
      </div>

      {filteredCases.length === 0 && (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ color: '#111827', fontSize: '1rem', fontWeight: 600 }}>No cases found</p>
          <p style={{ color: '#6b7280', fontSize: '0.875rem', marginTop: '0.5rem' }}>Try adjusting your search or filter</p>
        </div>
      )}

      {/* Results Count */}
      <div style={{ 
        marginTop: '1.5rem', 
        textAlign: 'center',
        color: '#111827',
        fontSize: '0.875rem',
        fontWeight: 600
      }}>
        Showing {filteredCases.length} of {cases.length} cases
      </div>
    </div>
  )
}
