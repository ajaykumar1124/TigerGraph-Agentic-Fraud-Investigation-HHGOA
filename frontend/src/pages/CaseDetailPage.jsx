import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Shield, AlertTriangle, FileText, Clock, User, Network } from 'lucide-react'

export default function CaseDetailPage() {
  const { caseId } = useParams()
  const [investigation, setInvestigation] = useState(null)
  const [loading, setLoading] = useState(true)
  const [evidence, setEvidence] = useState('')

  useEffect(() => {
    // Mock data
    setTimeout(() => {
      setInvestigation({
        case_id: caseId,
        customer_id: 'USR_1001',
        status: 'OPEN',
        fraud_pattern: 'Investigation in progress',
        risk_score: 92,
        confidence: 92,
        evidence: [
          { type: 'Risk Level', details: 'CRITICAL', severity: 'CRITICAL' },
          { type: 'Recommended Action', details: 'BLOCK' },
          { type: 'Analysis Phase', details: 'Phase 6 of 6' },
          { type: 'AI Analysis', details: 'Multiple high-value transactions from unusual locations with device mismatch detected' }
        ],
        action: 'BLOCK',
        requires_approval: false,
        policy_compliant: false
      })
      setLoading(false)
    }, 500)
  }, [caseId])

  if (loading) {
    return (
      <div className="page-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <div className="loading-spinner"></div>
      </div>
    )
  }

  if (!investigation) {
    return (
      <div className="page-container">
        <div style={{ padding: '2rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', borderRadius: '0.5rem', color: '#ef4444' }}>
          Investigation not found
        </div>
      </div>
    )
  }

  return (
    <div className="page-container">
      {/* Header */}
      <div style={{ marginBottom: '1.5rem' }}>
        <Link to="/investigations" className="action-button secondary" style={{ marginBottom: '1rem' }}>
          <ArrowLeft size={18} />
          Back to Investigations
        </Link>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div className="page-subtitle">Investigation Detail</div>
            <h1 className="page-title">{investigation.case_id}</h1>
          </div>
          <Link to={`/cases/${investigation.case_id}/network`} className="action-button secondary">
            <Network size={18} />
            Network View
          </Link>
        </div>
      </div>

      {/* 2-Column Grid */}
      <div className="case-detail-grid">
        {/* Left Column */}
        <div className="case-main-content">
          {/* Investigation Summary */}
          <div className="card">
            <h2 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <FileText size={20} />
              Investigation Summary
            </h2>
            
            <div className="info-grid">
              <div className="info-item">
                <div className="info-label">Customer</div>
                <div className="info-value">{investigation.customer_id}</div>
              </div>
              
              <div className="info-item">
                <div className="info-label">Status</div>
                <div className="info-value">
                  <span className="badge" style={{ 
                    background: 'linear-gradient(135deg, #f59e0b, #d97706)', 
                    color: 'white',
                    border: 'none'
                  }}>
                    {investigation.status}
                  </span>
                </div>
              </div>
              
              <div className="info-item">
                <div className="info-label">Fraud Pattern</div>
                <div className="info-value">{investigation.fraud_pattern}</div>
              </div>
              
              <div className="info-item">
                <div className="info-label">Evidence Items</div>
                <div className="info-value">{investigation.evidence.length}</div>
              </div>
            </div>
          </div>

          {/* Evidence Collected */}
          <div className="card">
            <h2 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Shield size={20} />
              Evidence Collected ({investigation.evidence.length})
            </h2>
            
            <div className="evidence-list">
              {investigation.evidence.map((item, index) => (
                <div key={index} className="evidence-item">
                  <div className="evidence-type">{item.type}</div>
                  <div className="evidence-details">{item.details}</div>
                  {item.severity && (
                    <span className="badge" style={{ 
                      marginTop: '0.5rem',
                      background: 'linear-gradient(135deg, #ef4444, #dc2626)', 
                      color: 'white',
                      border: 'none'
                    }}>
                      {item.severity}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Investigation Log */}
          <div className="card">
            <h2 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Clock size={20} />
              Investigation Log
            </h2>
            <p style={{ color: 'var(--gray-600)', fontStyle: 'italic', textAlign: 'center', padding: '2rem' }}>
              No log entries yet.
            </p>
          </div>

          {/* Submit Evidence */}
          <div className="card">
            <h2 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1rem' }}>
              Submit Additional Evidence
            </h2>
            
            <div style={{ marginBottom: '1rem' }}>
              <label htmlFor="evidence" className="form-label">Evidence Details</label>
              <textarea
                id="evidence"
                name="evidence"
                placeholder="Enter additional evidence..."
                value={evidence}
                onChange={(e) => setEvidence(e.target.value)}
              />
            </div>
            
            <button className="action-button primary" disabled={!evidence}>
              Submit Evidence
            </button>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="case-sidebar">
          {/* Risk Assessment */}
          <div className="card">
            <h2 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <AlertTriangle size={20} />
              Risk Assessment
            </h2>
            
            <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
              <div style={{ 
                width: '120px', 
                height: '120px', 
                margin: '0 auto 1rem',
                position: 'relative'
              }}>
                <svg width="120" height="120" style={{ transform: 'rotate(-90deg)' }}>
                  <circle cx="60" cy="60" r="50" fill="none" stroke="#e5e7eb" strokeWidth="10" />
                  <circle 
                    cx="60" 
                    cy="60" 
                    r="50" 
                    fill="none" 
                    stroke="#ef4444" 
                    strokeWidth="10"
                    strokeDasharray={`${(investigation.risk_score / 100) * 314} 314`}
                    strokeLinecap="round"
                  />
                </svg>
                <div style={{ 
                  position: 'absolute', 
                  top: '50%', 
                  left: '50%', 
                  transform: 'translate(-50%, -50%)',
                  fontSize: '2rem',
                  fontWeight: 800,
                  color: '#ef4444'
                }}>
                  {investigation.risk_score}%
                </div>
              </div>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div className="info-item">
                <div className="info-label">Risk Score</div>
                <div className="info-value" style={{ color: '#ef4444' }}>
                  {investigation.risk_score}%
                </div>
              </div>
              
              <div className="info-item">
                <div className="info-label">Confidence</div>
                <div className="info-value" style={{ color: '#6366f1' }}>
                  {investigation.confidence}%
                </div>
              </div>
              
              <div className="info-item">
                <div className="info-label">Evidence Collected</div>
                <div className="info-value">{investigation.evidence.length} items</div>
              </div>
            </div>
          </div>

          {/* Recommended Action */}
          <div className="card">
            <h2 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1rem' }}>
              Recommended Action
            </h2>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '1.5rem' }}>
              <div className="info-item">
                <div className="info-label">Action</div>
                <div className="info-value">
                  <span className="badge" style={{ 
                    background: 'linear-gradient(135deg, #ef4444, #dc2626)', 
                    color: 'white',
                    border: 'none',
                    fontSize: '0.875rem',
                    padding: '0.5rem 1rem'
                  }}>
                    {investigation.action}
                  </span>
                </div>
              </div>
              
              <div className="info-item">
                <div className="info-label">Requires Approval</div>
                <div className="info-value">{investigation.requires_approval ? 'Yes' : 'No'}</div>
              </div>
              
              <div className="info-item">
                <div className="info-label">Policy Compliant</div>
                <div className="info-value">{investigation.policy_compliant ? 'Yes' : 'No'}</div>
              </div>
            </div>
            
            <Link to="/approvals" className="action-button primary" style={{ width: '100%', justifyContent: 'center' }}>
              Review & Approve
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
