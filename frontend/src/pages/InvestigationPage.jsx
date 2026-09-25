import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import '../styles/InvestigationPage.css'

export default function InvestigationPage() {
  const { caseId } = useParams()
  const navigate = useNavigate()
  const [investigation, setInvestigation] = useState(null)
  const [loading, setLoading] = useState(true)
  const [additionalEvidence, setAdditionalEvidence] = useState(null)

  useEffect(() => {
    if (caseId) {
      loadInvestigation()
    }
  }, [caseId])

  const loadInvestigation = async () => {
    try {
      setLoading(true)
      const response = await fetch(`http://localhost:8000/api/v1/investigations/${caseId}`)
      const data = await response.json()
      setInvestigation(data)
    } catch (error) {
      console.error('Error loading investigation:', error)
    } finally {
      setLoading(false)
    }
  }

  const submitEvidence = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/investigations/${caseId}/additional-evidence`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            evidence_type: 'CUSTOMER_VALIDATION',
            evidence_data: { confirmed: false, message: 'Customer denied transaction' }
          })
        }
      )
      const data = await response.json()
      setAdditionalEvidence(data)
      loadInvestigation()
    } catch (error) {
      console.error('Error submitting evidence:', error)
    }
  }

  if (loading) return <div className="investigation-page"><div className="loading">Loading investigation...</div></div>
  if (!investigation) return <div className="investigation-page"><div className="error">Investigation not found</div></div>

  const riskColor = investigation.risk_score > 0.8 ? '#ef4444' : investigation.risk_score > 0.6 ? '#f97316' : '#10b981'

  return (
    <div className="investigation-page">
      <div className="page-header">
        <h1>Investigation: {investigation.case_id}</h1>
        <div className="status-badge" style={{ backgroundColor: riskColor }}>
          Risk: {(investigation.risk_score * 100).toFixed(0)}%
        </div>
      </div>

      <div className="investigation-grid">
        {/* Left Panel: Case Info & Evidence */}
        <div className="investigation-panel">
          <div className="panel-section">
            <h2>📋 Case Details</h2>
            <div className="details-grid">
              <div><strong>Customer:</strong> {investigation.customer_id}</div>
              <div><strong>Status:</strong> {investigation.status}</div>
              <div><strong>Fraud Pattern:</strong> {investigation.suspected_fraud_pattern || 'Not yet determined'}</div>
              <div><strong>Confidence:</strong> {(investigation.confidence_score * 100).toFixed(0)}%</div>
            </div>
          </div>

          <div className="panel-section">
            <h2>🔍 Evidence Collected</h2>
            <div className="evidence-list">
              {investigation.evidence.evidence_list?.map((evidence, i) => (
                <div key={i} className="evidence-item">
                  <div className="evidence-header">
                    <strong>{evidence.evidence_type}</strong>
                    <span className="confidence">
                      Confidence: {(evidence.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="evidence-desc">{evidence.description}</div>
                </div>
              )) || <div>No evidence collected yet</div>}
            </div>
          </div>
        </div>

        {/* Right Panel: Timeline & Actions */}
        <div className="investigation-panel">
          <div className="panel-section">
            <h2>📝 Investigation Timeline</h2>
            <div className="timeline">
              {investigation.investigation_log?.map((log, i) => (
                <div key={i} className="timeline-item">
                  <div className="timeline-time">{log.split('] ')[0].slice(1)}</div>
                  <div className="timeline-content">{log.split('] ')[1]}</div>
                </div>
              )) || <div>No timeline</div>}
            </div>
          </div>

          {investigation.recommended_action && (
            <div className="panel-section">
              <h2>⚡ Recommended Action</h2>
              <div className="action-card">
                <div className="action-type">{investigation.recommended_action.action_type}</div>
                <div className="action-details">
                  <p><strong>Rationale:</strong> {investigation.recommended_action.rationale}</p>
                  <p><strong>Requires Approval:</strong> {investigation.recommended_action.requires_approval ? 'Yes' : 'No'}</p>
                </div>
              </div>
            </div>
          )}

          <div className="panel-section">
            <h2>➕ Additional Evidence</h2>
            <button className="btn-primary" onClick={submitEvidence}>
              Request Customer Validation
            </button>
            {additionalEvidence && (
              <div className="evidence-response">
                <p><strong>Status:</strong> {additionalEvidence.status}</p>
                <p><strong>Updated Risk:</strong> {(additionalEvidence.risk_score * 100).toFixed(0)}%</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
