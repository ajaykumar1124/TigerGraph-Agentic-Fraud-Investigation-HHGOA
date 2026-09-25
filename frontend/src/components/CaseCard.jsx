import { Link } from 'react-router-dom'
import { AlertCircle, CheckCircle2, Clock } from 'lucide-react'

export default function CaseCard({ caseData }) {
  const getRiskColor = (risk) => {
    if (risk >= 80) return 'risk-critical'
    if (risk >= 60) return 'risk-high'
    if (risk >= 40) return 'risk-medium'
    return 'risk-low'
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'CLOSED':
        return <CheckCircle2 size={16} />
      case 'INVESTIGATING':
        return <Clock size={16} />
      default:
        return <AlertCircle size={16} />
    }
  }

  const riskScore = caseData.risk_score ?? caseData.trigger?.risk_score ?? 0
  const confidence = caseData.confidence_score ?? 0

  return (
    <Link to={`/cases/${caseData.case_id}`} className="case-card">
      <div className="case-row">
        <strong>{caseData.case_id}</strong>
        <span className={`badge status-${(caseData.status || '').toLowerCase()}`}>
          {getStatusIcon(caseData.status)}
          {caseData.status || 'OPEN'}
        </span>
      </div>
      <div className="case-meta">
        <span>Customer: {caseData.customer_id}</span>
      </div>
      <div className="case-meta">
        <span>Transaction: {caseData.transaction_id || 'N/A'}</span>
      </div>
      <div className="case-stats">
        <div className={`risk-badge ${getRiskColor(riskScore)}`}>
          Risk: {Math.round(riskScore)}%
        </div>
        <div className="confidence-badge">
          Confidence: {Math.round(confidence)}%
        </div>
      </div>
    </Link>
  )
}
