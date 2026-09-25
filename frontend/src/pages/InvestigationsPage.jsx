import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Filter, Plus, AlertTriangle, Clock, CheckCircle, TrendingUp, Eye } from 'lucide-react';

const InvestigationsPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [priorityFilter, setPriorityFilter] = useState('ALL');

  // Sample investigation data
  const [investigations, setInvestigations] = useState([
    {
      id: 'INV-2026-001',
      case_id: 'CASE-2026-001',
      title: 'Suspicious Card Transaction - Mumbai ATM',
      description: 'Multiple withdrawals from unusual locations within short timeframe',
      status: 'IN_PROGRESS',
      priority: 'CRITICAL',
      assignedTo: 'Fraud Analyst',
      createdAt: '2026-09-23T10:15:30',
      updatedAt: '2026-09-23T14:20:00',
      transactionCount: 3,
      totalAmount: 39000,
      riskScore: 92,
      findings: ['Impossible travel detected', 'Unusual withdrawal pattern', 'Device mismatch']
    },
    {
      id: 'INV-2026-002',
      case_id: 'CASE-2026-004',
      title: 'International Wire Transfer - Suspicious Country',
      description: 'Large wire transfer to high-risk jurisdiction at unusual hour',
      status: 'OPEN',
      priority: 'CRITICAL',
      assignedTo: null,
      createdAt: '2026-09-23T03:15:00',
      updatedAt: '2026-09-23T03:15:00',
      transactionCount: 1,
      totalAmount: 45000,
      riskScore: 94,
      findings: ['High-risk country', 'Unusual time', 'Large amount', 'Velocity check failed']
    },
    {
      id: 'INV-2026-003',
      case_id: 'CASE-2026-007',
      title: 'Cryptocurrency Exchange Transaction',
      description: 'Large crypto purchase from unverified exchange',
      status: 'IN_PROGRESS',
      priority: 'HIGH',
      assignedTo: 'Senior Analyst',
      createdAt: '2026-09-23T02:30:00',
      updatedAt: '2026-09-23T12:00:00',
      transactionCount: 1,
      totalAmount: 95000,
      riskScore: 96,
      findings: ['Crypto-related', 'KYC mismatch', 'High-risk country', 'Unusual time']
    },
    {
      id: 'INV-2026-004',
      case_id: 'CASE-2026-003',
      title: 'ATM Withdrawal - Early Morning',
      description: 'Large ATM withdrawal at unusual hour from Chennai',
      status: 'INVESTIGATING',
      priority: 'HIGH',
      assignedTo: 'Fraud Analyst',
      createdAt: '2026-09-23T08:00:00',
      updatedAt: '2026-09-23T13:30:00',
      transactionCount: 1,
      totalAmount: 35000,
      riskScore: 89,
      findings: ['Unusual time', 'Large amount', 'Location anomaly']
    },
    {
      id: 'INV-2026-005',
      case_id: 'CASE-2026-006',
      title: 'International SWIFT Transfer',
      description: 'Wire transfer to new recipient in different country',
      status: 'OPEN',
      priority: 'MEDIUM',
      assignedTo: null,
      createdAt: '2026-09-23T15:30:00',
      updatedAt: '2026-09-23T15:30:00',
      transactionCount: 1,
      totalAmount: 25000,
      riskScore: 75,
      findings: ['New recipient', 'International', 'Large amount']
    },
    {
      id: 'INV-2026-006',
      case_id: 'CASE-2026-005',
      title: 'Rapid Succession Transfers',
      description: 'Multiple transfers within minutes from mobile app',
      status: 'IN_PROGRESS',
      priority: 'MEDIUM',
      assignedTo: 'Junior Analyst',
      createdAt: '2026-09-23T11:45:20',
      updatedAt: '2026-09-23T16:00:00',
      transactionCount: 3,
      totalAmount: 24500,
      riskScore: 68,
      findings: ['Rapid succession', 'Unusual amount', 'Velocity exceeded']
    },
    {
      id: 'INV-2026-007',
      case_id: 'CASE-2026-008',
      title: 'Card Present Fraud - Jewelry Store',
      description: 'In-person card transaction with stolen card indicators',
      status: 'RESOLVED',
      priority: 'HIGH',
      assignedTo: 'Senior Analyst',
      createdAt: '2026-09-23T10:35:00',
      updatedAt: '2026-09-23T17:00:00',
      transactionCount: 1,
      totalAmount: 8000,
      riskScore: 91,
      findings: ['Stolen card', 'Multiple failed attempts', 'Card present fraud']
    }
  ]);

  useEffect(() => {
    setTimeout(() => setLoading(false), 500);
  }, []);

  const filteredInvestigations = investigations.filter(inv => {
    const matchesSearch = inv.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         inv.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         inv.case_id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'ALL' || inv.status === statusFilter;
    const matchesPriority = priorityFilter === 'ALL' || inv.priority === priorityFilter;
    
    return matchesSearch && matchesStatus && matchesPriority;
  });

  const stats = {
    total: investigations.length,
    open: investigations.filter(i => i.status === 'OPEN').length,
    inProgress: investigations.filter(i => i.status === 'IN_PROGRESS' || i.status === 'INVESTIGATING').length,
    resolved: investigations.filter(i => i.status === 'RESOLVED').length,
    critical: investigations.filter(i => i.priority === 'CRITICAL').length
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      notation: 'compact'
    }).format(amount);
  };

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString('en-IN', {
      dateStyle: 'medium',
      timeStyle: 'short'
    });
  };

  const getStatusBadge = (status) => {
    const badges = {
      'OPEN': { bg: '#f59e0b', text: 'white', label: '🔵 Open' },
      'IN_PROGRESS': { bg: '#6366f1', text: 'white', label: '🔍 In Progress' },
      'INVESTIGATING': { bg: '#6366f1', text: 'white', label: '🔎 Investigating' },
      'RESOLVED': { bg: '#10b981', text: 'white', label: '✅ Resolved' },
      'CLOSED': { bg: '#6b7280', text: 'white', label: '📁 Closed' }
    };
    const badge = badges[status] || badges['OPEN'];
    return (
      <span style={{
        padding: '0.25rem 0.75rem',
        background: badge.bg,
        borderRadius: '9999px',
        fontSize: '0.75rem',
        fontWeight: 700,
        color: badge.text
      }}>
        {badge.label}
      </span>
    );
  };

  const getPriorityBadge = (priority) => {
    const badges = {
      'CRITICAL': { color: '#ef4444', label: 'Critical' },
      'HIGH': { color: '#f59e0b', label: 'High' },
      'MEDIUM': { color: '#6366f1', label: 'Medium' },
      'LOW': { color: '#6b7280', label: 'Low' }
    };
    const badge = badges[priority] || badges['MEDIUM'];
    return (
      <span style={{
        padding: '0.25rem 0.75rem',
        background: badge.color,
        borderRadius: '9999px',
        fontSize: '0.75rem',
        fontWeight: 700,
        color: 'white'
      }}>
        {badge.label}
      </span>
    );
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <div className="loading-spinner"></div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <div className="page-subtitle">Investigation Management</div>
        <h1 className="page-title">Fraud Investigations</h1>
        <p style={{ color: '#111827', fontSize: '0.9375rem', fontWeight: 500 }}>
          Manage and track all fraud investigation cases
        </p>
      </div>

      {/* Stats */}
      <div className="stats-grid" style={{ marginBottom: '1.5rem' }}>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}>
            <TrendingUp size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Total Investigations</div>
          <div className="stat-value" style={{ color: '#111827' }}>{stats.total}</div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>All cases</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f59e0b, #d97706)' }}>
            <Clock size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Open</div>
          <div className="stat-value" style={{ color: '#f59e0b' }}>{stats.open}</div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>Awaiting assignment</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #6366f1, #4f46e5)' }}>
            <Filter size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>In Progress</div>
          <div className="stat-value" style={{ color: '#6366f1' }}>{stats.inProgress}</div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>Under investigation</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #10b981, #059669)' }}>
            <CheckCircle size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Resolved</div>
          <div className="stat-value" style={{ color: '#10b981' }}>{stats.resolved}</div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>Successfully closed</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #ef4444, #dc2626)' }}>
            <AlertTriangle size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Critical Priority</div>
          <div className="stat-value" style={{ color: '#ef4444' }}>{stats.critical}</div>
          <div className="stat-change" style={{ color: '#ef4444', fontWeight: 700 }}>
            <AlertTriangle size={16} />
            Urgent action needed
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: '250px', position: 'relative' }}>
            <Search size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: '#6b7280' }} />
            <input
              type="text"
              placeholder="Search investigations..."
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
            <option value="OPEN">Open</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="INVESTIGATING">Investigating</option>
            <option value="RESOLVED">Resolved</option>
          </select>
          
          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            style={{ minWidth: '150px', color: '#111827', fontWeight: 600 }}
          >
            <option value="ALL">All Priority</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>

          <button className="action-button primary">
            <Plus size={18} />
            New Investigation
          </button>
        </div>
      </div>

      {/* Investigations List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {filteredInvestigations.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
            <Filter size={48} style={{ marginBottom: '1rem', color: '#9ca3af' }} />
            <p style={{ color: '#111827', fontSize: '1rem', fontWeight: 600 }}>No investigations found</p>
            <p style={{ color: '#6b7280', fontSize: '0.875rem', marginTop: '0.5rem' }}>Try adjusting your search or filters</p>
          </div>
        ) : (
          filteredInvestigations.map((inv) => (
            <div
              key={inv.id}
              className="card"
              style={{
                cursor: 'pointer',
                transition: 'all 0.2s',
                border: inv.priority === 'CRITICAL' ? '2px solid #ef4444' : undefined
              }}
              onClick={() => navigate(`/cases/${inv.case_id}`)}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)'
                e.currentTarget.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.12)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)'
                e.currentTarget.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.06)'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: '1.5rem' }}>
                {/* Left Side */}
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', marginBottom: '0.5rem', flexWrap: 'wrap' }}>
                    <h3 style={{ fontSize: '1rem', fontWeight: 700, margin: 0, color: '#111827' }}>{inv.id}</h3>
                    {getStatusBadge(inv.status)}
                    {getPriorityBadge(inv.priority)}
                  </div>
                  
                  <h4 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.5rem', color: '#111827' }}>
                    {inv.title}
                  </h4>
                  
                  <p style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.75rem', fontWeight: 500 }}>
                    {inv.description}
                  </p>

                  <div style={{ display: 'flex', gap: '1.5rem', fontSize: '0.8125rem', color: '#111827', marginBottom: '0.75rem', fontWeight: 600 }}>
                    <span>Case: <strong>{inv.case_id}</strong></span>
                    <span>Transactions: <strong>{inv.transactionCount}</strong></span>
                    <span>Amount: <strong>{formatCurrency(inv.totalAmount)}</strong></span>
                    <span>Risk: <strong style={{ color: inv.riskScore >= 80 ? '#ef4444' : '#f59e0b' }}>{inv.riskScore}%</strong></span>
                  </div>

                  {inv.findings && inv.findings.length > 0 && (
                    <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '0.75rem' }}>
                      {inv.findings.slice(0, 4).map((finding, idx) => (
                        <span
                          key={idx}
                          style={{
                            padding: '0.25rem 0.75rem',
                            background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                            color: 'white',
                            borderRadius: '9999px',
                            fontSize: '0.6875rem',
                            fontWeight: 700
                          }}
                        >
                          {finding}
                        </span>
                      ))}
                      {inv.findings.length > 4 && (
                        <span style={{ fontSize: '0.6875rem', color: '#6b7280', fontWeight: 600 }}>
                          +{inv.findings.length - 4} more
                        </span>
                      )}
                    </div>
                  )}
                </div>

                {/* Right Side */}
                <div style={{ minWidth: '200px', textAlign: 'right' }}>
                  <div style={{ fontSize: '0.8125rem', color: '#111827', marginBottom: '0.5rem', fontWeight: 600 }}>
                    {inv.assignedTo ? (
                      <>
                        <div style={{ color: '#6b7280', fontSize: '0.75rem', marginBottom: '0.25rem' }}>Assigned to:</div>
                        <div style={{ color: '#111827', fontWeight: 700 }}>{inv.assignedTo}</div>
                      </>
                    ) : (
                      <div style={{ color: '#f59e0b', fontWeight: 700 }}>⚠️ Unassigned</div>
                    )}
                  </div>
                  
                  <div style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '0.75rem', fontWeight: 500 }}>
                    <div>Created: {formatDate(inv.createdAt)}</div>
                    <div>Updated: {formatDate(inv.updatedAt)}</div>
                  </div>

                  <button 
                    className="action-button primary" 
                    style={{ marginTop: '1rem', padding: '0.5rem 1rem', fontSize: '0.8125rem', width: '100%' }}
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/cases/${inv.case_id}`);
                    }}
                  >
                    <Eye size={16} />
                    View Details
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Results Count */}
      {filteredInvestigations.length > 0 && (
        <div style={{ 
          marginTop: '1.5rem', 
          textAlign: 'center',
          color: '#111827',
          fontSize: '0.875rem',
          fontWeight: 600
        }}>
          Showing {filteredInvestigations.length} of {investigations.length} investigations
        </div>
      )}
    </div>
  );
};

export default InvestigationsPage;
