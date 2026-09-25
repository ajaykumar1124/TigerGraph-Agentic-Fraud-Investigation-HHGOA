import { useState, useEffect } from 'react';
import { CheckCircle, XCircle, Clock, AlertTriangle, ThumbsUp, ThumbsDown, Eye } from 'lucide-react';

const ApprovalsPage = () => {
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('PENDING');

  const [approvals, setApprovals] = useState([
    {
      id: 'APR-2026-001',
      case_id: 'CASE-2026-002',
      type: 'BLOCK_ACCOUNT',
      title: 'Block Account - Account Takeover Suspected',
      description: 'Recommendation to block account USR_1001 due to impossible travel pattern',
      requestedBy: 'AI Agent',
      status: 'PENDING',
      priority: 'CRITICAL',
      amount: 12000,
      riskScore: 95,
      confidence: 91,
      evidence: ['Impossible travel detected', 'Multiple suspicious transactions', 'Device mismatch'],
      timestamp: '2026-09-23T10:30:00',
      details: 'Account showed withdrawals in Mumbai and Delhi within 10 minutes, indicating possible account takeover.'
    },
    {
      id: 'APR-2026-002',
      case_id: 'CASE-2026-004',
      type: 'BLOCK_TRANSACTION',
      title: 'Block International Wire Transfer',
      description: 'Recommendation to block ₹45,000 wire transfer to high-risk country',
      requestedBy: 'Fraud Detection System',
      status: 'PENDING',
      priority: 'CRITICAL',
      amount: 45000,
      riskScore: 94,
      confidence: 90,
      evidence: ['High-risk country', 'Unusual time (3:15 AM)', 'Large amount', 'Velocity check failed'],
      timestamp: '2026-09-23T03:20:00',
      details: 'Large wire transfer initiated at unusual hour to jurisdiction flagged for money laundering risk.'
    },
    {
      id: 'APR-2026-003',
      case_id: 'CASE-2026-007',
      type: 'REQUIRE_VERIFICATION',
      title: 'Require Additional Verification - Crypto Purchase',
      description: 'Request additional KYC verification for ₹95,000 cryptocurrency purchase',
      requestedBy: 'Compliance System',
      status: 'PENDING',
      priority: 'HIGH',
      amount: 95000,
      riskScore: 96,
      confidence: 93,
      evidence: ['Crypto exchange', 'KYC mismatch', 'High-risk country', 'Large amount'],
      timestamp: '2026-09-23T02:35:00',
      details: 'Cryptocurrency purchase from unverified exchange with discrepancies in customer KYC data.'
    },
    {
      id: 'APR-2026-004',
      case_id: 'CASE-2026-001',
      type: 'FLAG_ACCOUNT',
      title: 'Flag Account for Monitoring',
      description: 'Recommendation to flag account USR_1001 for enhanced monitoring',
      requestedBy: 'Risk Analysis System',
      status: 'APPROVED',
      priority: 'HIGH',
      amount: 39000,
      riskScore: 92,
      confidence: 88,
      evidence: ['Multiple ATM withdrawals', 'Unusual locations', 'Short timeframe'],
      timestamp: '2026-09-23T10:20:00',
      approvedBy: 'Senior Analyst',
      approvedAt: '2026-09-23T14:15:00',
      details: 'Pattern of suspicious ATM activity across Mumbai justifies enhanced monitoring.'
    },
    {
      id: 'APR-2026-005',
      case_id: 'CASE-2026-005',
      type: 'REQUEST_EVIDENCE',
      title: 'Request Additional Evidence',
      description: 'Request customer contact for rapid succession transfer verification',
      requestedBy: 'Investigation Team',
      status: 'PENDING',
      priority: 'MEDIUM',
      amount: 24500,
      riskScore: 68,
      confidence: 65,
      evidence: ['Rapid succession', 'Unusual amount', 'Mobile banking'],
      timestamp: '2026-09-23T12:00:00',
      details: 'Multiple transfers within minutes may be legitimate but require verification.'
    },
    {
      id: 'APR-2026-006',
      case_id: 'CASE-2026-008',
      type: 'APPROVE_TRANSACTION',
      title: 'Approve Reversal Request',
      description: 'Approve transaction reversal for confirmed card fraud case',
      requestedBy: 'Customer Service',
      status: 'APPROVED',
      priority: 'MEDIUM',
      amount: 8000,
      riskScore: 91,
      confidence: 87,
      evidence: ['Stolen card confirmed', 'Police report filed', 'Customer verified'],
      timestamp: '2026-09-23T16:30:00',
      approvedBy: 'Fraud Manager',
      approvedAt: '2026-09-23T17:00:00',
      details: 'Card present fraud confirmed with police report. Customer eligible for refund.'
    },
    {
      id: 'APR-2026-007',
      case_id: 'CASE-2026-003',
      type: 'ESCALATE',
      title: 'Escalate to Senior Investigation',
      description: 'Escalate Chennai ATM case to senior fraud analyst',
      requestedBy: 'Junior Analyst',
      status: 'REJECTED',
      priority: 'MEDIUM',
      amount: 35000,
      riskScore: 89,
      confidence: 85,
      evidence: ['Early morning withdrawal', 'Large amount', 'Location anomaly'],
      timestamp: '2026-09-23T13:00:00',
      rejectedBy: 'Team Lead',
      rejectedAt: '2026-09-23T13:30:00',
      rejectionReason: 'Within normal investigation parameters. Continue standard process.',
      details: 'Case does not meet criteria for senior escalation at this stage.'
    }
  ]);

  useEffect(() => {
    setTimeout(() => setLoading(false), 500);
  }, []);

  const filteredApprovals = approvals.filter(a => {
    if (filter === 'ALL') return true;
    return a.status === filter;
  });

  const stats = {
    total: approvals.length,
    pending: approvals.filter(a => a.status === 'PENDING').length,
    approved: approvals.filter(a => a.status === 'APPROVED').length,
    rejected: approvals.filter(a => a.status === 'REJECTED').length
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR'
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
      'PENDING': { color: '#f59e0b', icon: <Clock size={14} />, label: 'Pending' },
      'APPROVED': { color: '#10b981', icon: <CheckCircle size={14} />, label: 'Approved' },
      'REJECTED': { color: '#ef4444', icon: <XCircle size={14} />, label: 'Rejected' }
    };
    const badge = badges[status];
    return (
      <span style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '0.375rem',
        padding: '0.375rem 0.875rem',
        background: badge.color,
        borderRadius: '9999px',
        fontSize: '0.8125rem',
        fontWeight: 700,
        color: 'white'
      }}>
        {badge.icon}
        {badge.label}
      </span>
    );
  };

  const getPriorityBadge = (priority) => {
    const colors = {
      'CRITICAL': '#ef4444',
      'HIGH': '#f59e0b',
      'MEDIUM': '#6366f1',
      'LOW': '#6b7280'
    };
    return (
      <span style={{
        padding: '0.375rem 0.875rem',
        background: colors[priority],
        borderRadius: '9999px',
        fontSize: '0.8125rem',
        fontWeight: 700,
        color: 'white'
      }}>
        {priority}
      </span>
    );
  };

  const handleApprove = (id) => {
    setApprovals(approvals.map(a => 
      a.id === id ? {
        ...a,
        status: 'APPROVED',
        approvedBy: 'Current User',
        approvedAt: new Date().toISOString()
      } : a
    ));
  };

  const handleReject = (id) => {
    setApprovals(approvals.map(a => 
      a.id === id ? {
        ...a,
        status: 'REJECTED',
        rejectedBy: 'Current User',
        rejectedAt: new Date().toISOString(),
        rejectionReason: 'Rejected by user'
      } : a
    ));
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
        <div className="page-subtitle">Action Approval</div>
        <h1 className="page-title">Approval Requests</h1>
        <p style={{ color: '#111827', fontSize: '0.9375rem', fontWeight: 500 }}>
          Review and approve fraud investigation actions
        </p>
      </div>

      {/* Stats */}
      <div className="stats-grid" style={{ marginBottom: '1.5rem' }}>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}>
            <AlertTriangle size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Total Requests</div>
          <div className="stat-value" style={{ color: '#111827' }}>{stats.total}</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f59e0b, #d97706)' }}>
            <Clock size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Pending</div>
          <div className="stat-value" style={{ color: '#f59e0b' }}>{stats.pending}</div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>Awaiting review</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #10b981, #059669)' }}>
            <CheckCircle size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Approved</div>
          <div className="stat-value" style={{ color: '#10b981' }}>{stats.approved}</div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>Actions approved</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #ef4444, #dc2626)' }}>
            <XCircle size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Rejected</div>
          <div className="stat-value" style={{ color: '#ef4444' }}>{stats.rejected}</div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>Actions denied</div>
        </div>
      </div>

      {/* Filters */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          {['ALL', 'PENDING', 'APPROVED', 'REJECTED'].map(status => (
            <button
              key={status}
              className={`action-button ${filter === status ? 'primary' : 'secondary'}`}
              onClick={() => setFilter(status)}
            >
              {status} ({status === 'ALL' ? stats.total : stats[status.toLowerCase()]})
            </button>
          ))}
        </div>
      </div>

      {/* Approvals List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {filteredApprovals.map((approval) => (
          <div
            key={approval.id}
            className="card"
            style={{
              border: approval.priority === 'CRITICAL' && approval.status === 'PENDING' 
                ? '2px solid #ef4444' 
                : undefined
            }}
          >
            <div style={{ display: 'flex', gap: '1.5rem', justifyContent: 'space-between' }}>
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', marginBottom: '0.75rem', flexWrap: 'wrap' }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: 700, margin: 0, color: '#111827' }}>{approval.id}</h3>
                  {getStatusBadge(approval.status)}
                  {getPriorityBadge(approval.priority)}
                  <span style={{
                    padding: '0.375rem 0.875rem',
                    background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                    borderRadius: '9999px',
                    fontSize: '0.75rem',
                    fontWeight: 700,
                    color: 'white'
                  }}>
                    {approval.type.replace('_', ' ')}
                  </span>
                </div>

                <h4 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.5rem', color: '#111827' }}>
                  {approval.title}
                </h4>

                <p style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.75rem', fontWeight: 500 }}>
                  {approval.description}
                </p>

                <div style={{ fontSize: '0.875rem', color: '#111827', marginBottom: '0.75rem', lineHeight: 1.6, fontWeight: 500 }}>
                  {approval.details}
                </div>

                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                  gap: '1rem',
                  padding: '1rem',
                  background: '#f9fafb',
                  borderRadius: '0.5rem',
                  marginBottom: '0.75rem',
                  fontSize: '0.8125rem'
                }}>
                  <div>
                    <div style={{ color: '#6b7280', marginBottom: '0.25rem', fontWeight: 600 }}>Case ID</div>
                    <div style={{ fontWeight: 700, color: '#111827' }}>{approval.case_id}</div>
                  </div>
                  <div>
                    <div style={{ color: '#6b7280', marginBottom: '0.25rem', fontWeight: 600 }}>Amount</div>
                    <div style={{ fontWeight: 700, color: '#111827' }}>{formatCurrency(approval.amount)}</div>
                  </div>
                  <div>
                    <div style={{ color: '#6b7280', marginBottom: '0.25rem', fontWeight: 600 }}>Risk Score</div>
                    <div style={{ fontWeight: 700, color: approval.riskScore >= 80 ? '#ef4444' : '#f59e0b' }}>
                      {approval.riskScore}%
                    </div>
                  </div>
                  <div>
                    <div style={{ color: '#6b7280', marginBottom: '0.25rem', fontWeight: 600 }}>Confidence</div>
                    <div style={{ fontWeight: 700, color: '#111827' }}>{approval.confidence}%</div>
                  </div>
                  <div>
                    <div style={{ color: '#6b7280', marginBottom: '0.25rem', fontWeight: 600 }}>Requested By</div>
                    <div style={{ fontWeight: 700, color: '#111827' }}>{approval.requestedBy}</div>
                  </div>
                  <div>
                    <div style={{ color: '#6b7280', marginBottom: '0.25rem', fontWeight: 600 }}>Requested At</div>
                    <div style={{ fontWeight: 700, fontSize: '0.6875rem', color: '#111827' }}>{formatDate(approval.timestamp)}</div>
                  </div>
                </div>

                {approval.evidence && approval.evidence.length > 0 && (
                  <div style={{ marginBottom: '0.75rem' }}>
                    <div style={{ fontSize: '0.8125rem', color: '#6b7280', marginBottom: '0.5rem', fontWeight: 600 }}>
                      Evidence:
                    </div>
                    <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                      {approval.evidence.map((evidence, idx) => (
                        <span
                          key={idx}
                          style={{
                            padding: '0.25rem 0.75rem',
                            background: 'linear-gradient(135deg, #f59e0b, #d97706)',
                            borderRadius: '9999px',
                            fontSize: '0.75rem',
                            fontWeight: 700,
                            color: 'white'
                          }}
                        >
                          {evidence}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {approval.status === 'APPROVED' && approval.approvedBy && (
                  <div style={{
                    padding: '0.75rem',
                    background: '#d1fae5',
                    border: '1px solid #10b981',
                    borderRadius: '0.5rem',
                    fontSize: '0.8125rem',
                    color: '#047857',
                    fontWeight: 600
                  }}>
                    ✓ Approved by {approval.approvedBy} at {formatDate(approval.approvedAt)}
                  </div>
                )}

                {approval.status === 'REJECTED' && approval.rejectedBy && (
                  <div style={{
                    padding: '0.75rem',
                    background: '#fee2e2',
                    border: '1px solid #ef4444',
                    borderRadius: '0.5rem',
                    fontSize: '0.8125rem',
                    color: '#dc2626',
                    fontWeight: 600
                  }}>
                    ✗ Rejected by {approval.rejectedBy} at {formatDate(approval.rejectedAt)}
                    {approval.rejectionReason && (
                      <div style={{ marginTop: '0.5rem' }}>Reason: {approval.rejectionReason}</div>
                    )}
                  </div>
                )}
              </div>

              {approval.status === 'PENDING' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', minWidth: '150px' }}>
                  <button
                    className="action-button primary"
                    onClick={() => handleApprove(approval.id)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '0.5rem',
                      background: 'linear-gradient(135deg, #10b981, #059669)',
                      padding: '0.625rem 1rem'
                    }}
                  >
                    <ThumbsUp size={16} />
                    Approve
                  </button>
                  <button
                    className="action-button"
                    onClick={() => handleReject(approval.id)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '0.5rem',
                      background: 'linear-gradient(135deg, #ef4444, #dc2626)',
                      color: 'white',
                      padding: '0.625rem 1rem'
                    }}
                  >
                    <ThumbsDown size={16} />
                    Reject
                  </button>
                  <button
                    className="action-button secondary"
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '0.5rem',
                      padding: '0.625rem 1rem'
                    }}
                  >
                    <Eye size={16} />
                    Details
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {filteredApprovals.length === 0 && (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <AlertTriangle size={48} style={{ marginBottom: '1rem', color: '#9ca3af' }} />
          <p style={{ color: '#111827', fontSize: '1rem', fontWeight: 600 }}>No approval requests found</p>
        </div>
      )}

      <div style={{
        marginTop: '1.5rem',
        textAlign: 'center',
        fontSize: '0.875rem',
        color: '#111827',
        fontWeight: 600
      }}>
        Showing {filteredApprovals.length} of {approvals.length} approval requests
      </div>
    </div>
  );
};

export default ApprovalsPage;
