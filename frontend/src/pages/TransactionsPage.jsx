import { useState } from 'react'
import { Search, Filter, Download, TrendingUp, AlertCircle } from 'lucide-react'

export default function TransactionsPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('ALL')

  const transactions = [
    {
      id: 'TXN-2026-001',
      user: 'USR_1001',
      amount: 15000,
      merchant: 'ATM Mumbai',
      time: '2026-09-23 10:15:30',
      status: 'FLAGGED',
      risk: 'HIGH'
    },
    {
      id: 'TXN-2026-002',
      user: 'USR_1001',
      amount: 12000,
      merchant: 'ATM Delhi',
      time: '2026-09-23 11:30:45',
      status: 'FLAGGED',
      risk: 'HIGH'
    },
    {
      id: 'TXN-2026-003',
      user: 'USR_1001',
      amount: 12000,
      merchant: 'ATM Bangalore',
      time: '2026-09-23 12:45:00',
      status: 'FLAGGED',
      risk: 'HIGH'
    },
    {
      id: 'TXN-2026-004',
      user: 'USR_1002',
      amount: 45000,
      merchant: 'International Wire',
      time: '2026-09-23 03:15:00',
      status: 'BLOCKED',
      risk: 'CRITICAL'
    },
    {
      id: 'TXN-2026-005',
      user: 'USR_1003',
      amount: 95000,
      merchant: 'Crypto Exchange',
      time: '2026-09-23 02:30:00',
      status: 'REVIEW',
      risk: 'CRITICAL'
    },
    {
      id: 'TXN-2026-006',
      user: 'USR_1001',
      amount: 35000,
      merchant: 'ATM Chennai',
      time: '2026-09-23 08:00:00',
      status: 'FLAGGED',
      risk: 'MEDIUM'
    }
  ]

  const stats = [
    { label: 'Total Transactions', value: '156', change: '+12%', color: '#6366f1' },
    { label: 'Flagged', value: '24', change: '+5%', color: '#f59e0b' },
    { label: 'Blocked', value: '8', change: '+2%', color: '#ef4444' },
    { label: 'Total Amount', value: '₹2.4M', change: '+18%', color: '#10b981' }
  ]

  const filteredTransactions = transactions.filter(txn => {
    const matchesSearch = txn.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         txn.user.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = filterStatus === 'ALL' || txn.status === filterStatus
    return matchesSearch && matchesFilter
  })

  const getStatusColor = (status) => {
    const colors = {
      'FLAGGED': { bg: 'rgba(245, 158, 11, 0.1)', text: '#f59e0b', border: '#f59e0b' },
      'BLOCKED': { bg: 'rgba(239, 68, 68, 0.1)', text: '#ef4444', border: '#ef4444' },
      'REVIEW': { bg: 'rgba(99, 102, 241, 0.1)', text: '#6366f1', border: '#6366f1' },
      'APPROVED': { bg: 'rgba(16, 185, 129, 0.1)', text: '#10b981', border: '#10b981' }
    }
    return colors[status] || colors['REVIEW']
  }

  const getRiskColor = (risk) => {
    const colors = {
      'CRITICAL': '#ef4444',
      'HIGH': '#f59e0b',
      'MEDIUM': '#6366f1',
      'LOW': '#10b981'
    }
    return colors[risk] || colors['MEDIUM']
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <div className="page-subtitle">Transaction Management</div>
        <h1 className="page-title">All Transactions</h1>
        <p style={{ color: '#111827', fontSize: '0.9375rem', fontWeight: 500 }}>
          Monitor and manage all financial transactions in real-time
        </p>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        {stats.map((stat, index) => (
          <div key={index} className="stat-card">
            <div className="stat-icon" style={{ background: stat.color }}>
              <TrendingUp size={24} color="white" />
            </div>
            <div className="stat-label" style={{ color: '#111827' }}>{stat.label}</div>
            <div className="stat-value" style={{ color: '#111827' }}>{stat.value}</div>
            <div className="stat-change" style={{ color: '#10b981', fontWeight: 600 }}>
              {stat.change} from last month
            </div>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: '250px', position: 'relative' }}>
            <Search size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: '#6b7280' }} />
            <input
              type="text"
              placeholder="Search transactions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ paddingLeft: '2.5rem', color: '#111827' }}
            />
          </div>
          
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            style={{ minWidth: '150px', color: '#111827', fontWeight: 600 }}
          >
            <option value="ALL">All Status</option>
            <option value="FLAGGED">Flagged</option>
            <option value="BLOCKED">Blocked</option>
            <option value="REVIEW">Under Review</option>
            <option value="APPROVED">Approved</option>
          </select>
          
          <button className="action-button secondary">
            <Filter size={18} />
            More Filters
          </button>
          
          <button className="action-button primary">
            <Download size={18} />
            Export
          </button>
        </div>
      </div>

      {/* Transactions Table */}
      <div className="card">
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #e5e7eb' }}>
                <th style={{ padding: '1rem', textAlign: 'left', color: '#111827', fontSize: '0.875rem', fontWeight: 700, textTransform: 'uppercase' }}>
                  Transaction ID
                </th>
                <th style={{ padding: '1rem', textAlign: 'left', color: '#111827', fontSize: '0.875rem', fontWeight: 700, textTransform: 'uppercase' }}>
                  User
                </th>
                <th style={{ padding: '1rem', textAlign: 'right', color: '#111827', fontSize: '0.875rem', fontWeight: 700, textTransform: 'uppercase' }}>
                  Amount
                </th>
                <th style={{ padding: '1rem', textAlign: 'left', color: '#111827', fontSize: '0.875rem', fontWeight: 700, textTransform: 'uppercase' }}>
                  Merchant
                </th>
                <th style={{ padding: '1rem', textAlign: 'left', color: '#111827', fontSize: '0.875rem', fontWeight: 700, textTransform: 'uppercase' }}>
                  Time
                </th>
                <th style={{ padding: '1rem', textAlign: 'center', color: '#111827', fontSize: '0.875rem', fontWeight: 700, textTransform: 'uppercase' }}>
                  Risk
                </th>
                <th style={{ padding: '1rem', textAlign: 'center', color: '#111827', fontSize: '0.875rem', fontWeight: 700, textTransform: 'uppercase' }}>
                  Status
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredTransactions.map((txn) => {
                const statusStyle = getStatusColor(txn.status)
                return (
                  <tr key={txn.id} style={{ borderBottom: '1px solid #e5e7eb', transition: 'background 0.2s' }}
                    onMouseEnter={(e) => e.currentTarget.style.background = '#f9fafb'}
                    onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                  >
                    <td style={{ padding: '1rem', color: '#111827', fontWeight: 700 }}>
                      {txn.id}
                    </td>
                    <td style={{ padding: '1rem', color: '#111827', fontWeight: 600 }}>
                      {txn.user}
                    </td>
                    <td style={{ padding: '1rem', textAlign: 'right', color: '#111827', fontWeight: 700, fontSize: '1rem' }}>
                      ₹{txn.amount.toLocaleString()}
                    </td>
                    <td style={{ padding: '1rem', color: '#111827' }}>
                      {txn.merchant}
                    </td>
                    <td style={{ padding: '1rem', color: '#111827', fontSize: '0.875rem' }}>
                      {txn.time}
                    </td>
                    <td style={{ padding: '1rem', textAlign: 'center' }}>
                      <span style={{ 
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.25rem',
                        padding: '0.25rem 0.75rem',
                        background: `${getRiskColor(txn.risk)}15`,
                        color: getRiskColor(txn.risk),
                        borderRadius: '9999px',
                        fontSize: '0.75rem',
                        fontWeight: 700,
                        textTransform: 'uppercase'
                      }}>
                        <AlertCircle size={12} />
                        {txn.risk}
                      </span>
                    </td>
                    <td style={{ padding: '1rem', textAlign: 'center' }}>
                      <span style={{ 
                        display: 'inline-block',
                        padding: '0.375rem 0.75rem',
                        background: statusStyle.bg,
                        color: statusStyle.text,
                        border: `1px solid ${statusStyle.border}`,
                        borderRadius: '9999px',
                        fontSize: '0.75rem',
                        fontWeight: 700,
                        textTransform: 'uppercase'
                      }}>
                        {txn.status}
                      </span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>

        {filteredTransactions.length === 0 && (
          <div style={{ textAlign: 'center', padding: '3rem', color: '#111827' }}>
            <p style={{ fontSize: '1rem', fontWeight: 600 }}>No transactions found</p>
            <p style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.5rem' }}>Try adjusting your search or filter</p>
          </div>
        )}

        <div style={{ 
          marginTop: '1.5rem', 
          paddingTop: '1rem', 
          borderTop: '1px solid #e5e7eb',
          textAlign: 'center',
          color: '#111827',
          fontSize: '0.875rem',
          fontWeight: 600
        }}>
          Showing {filteredTransactions.length} of {transactions.length} transactions
        </div>
      </div>
    </div>
  )
}
