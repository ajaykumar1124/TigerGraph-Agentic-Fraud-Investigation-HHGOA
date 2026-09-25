import { useState } from 'react';
import { FileText, Download, Calendar, TrendingUp, PieChart, BarChart3, Filter } from 'lucide-react';

const ReportsPage = () => {
  const [selectedReport, setSelectedReport] = useState('fraud-summary');
  const [dateRange, setDateRange] = useState('7d');

  const reports = [
    {
      id: 'fraud-summary',
      name: 'Fraud Summary Report',
      description: 'Overview of all fraud cases and investigation outcomes',
      icon: <FileText size={24} />,
      generated: '2026-09-23T18:00:00',
      size: '2.4 MB'
    },
    {
      id: 'transaction-analysis',
      name: 'Transaction Analysis Report',
      description: 'Detailed analysis of transaction patterns and anomalies',
      icon: <TrendingUp size={24} />,
      generated: '2026-09-23T17:30:00',
      size: '3.1 MB'
    },
    {
      id: 'risk-assessment',
      name: 'Risk Assessment Report',
      description: 'Risk scores and fraud patterns by category',
      icon: <PieChart size={24} />,
      generated: '2026-09-23T16:00:00',
      size: '1.8 MB'
    },
    {
      id: 'performance-metrics',
      name: 'Performance Metrics Report',
      description: 'Investigation performance and resolution times',
      icon: <BarChart3 size={24} />,
      generated: '2026-09-23T15:00:00',
      size: '1.2 MB'
    },
    {
      id: 'compliance',
      name: 'Compliance Report',
      description: 'Regulatory compliance and audit trail',
      icon: <FileText size={24} />,
      generated: '2026-09-23T14:00:00',
      size: '4.5 MB'
    },
    {
      id: 'user-activity',
      name: 'User Activity Report',
      description: 'High-risk user accounts and activity patterns',
      icon: <TrendingUp size={24} />,
      generated: '2026-09-23T13:00:00',
      size: '2.8 MB'
    }
  ];

  const summaryData = {
    totalCases: 127,
    fraudDetected: 38,
    falsePositives: 12,
    avgResolutionTime: '4.2 hours',
    amountSaved: 4850000,
    avgRiskScore: 67
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

  return (
    <div className="page-container">
      <div className="page-header">
        <div className="page-subtitle">Business Intelligence</div>
        <h1 className="page-title">Reports & Analytics</h1>
        <p style={{ color: '#111827', fontSize: '0.9375rem', fontWeight: 500 }}>
          Generate and download fraud investigation reports
        </p>
      </div>

      {/* Controls */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
            <span style={{ fontSize: '0.875rem', fontWeight: 600, color: '#111827' }}>Date Range:</span>
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              style={{ minWidth: '150px', color: '#111827', fontWeight: 600 }}
            >
              <option value="24h">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="90d">Last 90 Days</option>
            </select>
          </div>
          <button className="action-button primary">
            <Download size={18} />
            Generate Report
          </button>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="stats-grid" style={{ marginBottom: '1.5rem' }}>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}>
            <TrendingUp size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Total Cases</div>
          <div className="stat-value" style={{ color: '#111827' }}>{summaryData.totalCases}</div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>
            Last {dateRange === '24h' ? '24 hours' : dateRange}
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #ef4444, #dc2626)' }}>
            <TrendingUp size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Fraud Detected</div>
          <div className="stat-value" style={{ color: '#ef4444' }}>{summaryData.fraudDetected}</div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>
            {((summaryData.fraudDetected / summaryData.totalCases) * 100).toFixed(1)}% detection rate
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f59e0b, #d97706)' }}>
            <TrendingUp size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>False Positives</div>
          <div className="stat-value" style={{ color: '#f59e0b' }}>{summaryData.falsePositives}</div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>
            {((summaryData.falsePositives / summaryData.totalCases) * 100).toFixed(1)}% rate
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #10b981, #059669)' }}>
            <TrendingUp size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Amount Saved</div>
          <div className="stat-value" style={{ fontSize: '1.5rem', color: '#10b981' }}>
            {formatCurrency(summaryData.amountSaved)}
          </div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>
            Fraud prevented
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #6366f1, #4f46e5)' }}>
            <TrendingUp size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Avg Resolution Time</div>
          <div className="stat-value" style={{ fontSize: '1.75rem', color: '#111827' }}>{summaryData.avgResolutionTime}</div>
          <div className="stat-change" style={{ color: '#10b981', fontWeight: 600 }}>
            15% faster than last period
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f59e0b, #d97706)' }}>
            <TrendingUp size={24} color="white" />
          </div>
          <div className="stat-label" style={{ color: '#111827' }}>Avg Risk Score</div>
          <div className="stat-value" style={{ color: '#f59e0b' }}>{summaryData.avgRiskScore}%</div>
          <div className="stat-change" style={{ color: '#111827', fontWeight: 600 }}>
            Across all cases
          </div>
        </div>
      </div>

      {/* Reports Grid */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '1.25rem', color: '#111827' }}>
          Available Reports
        </h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '1.25rem' }}>
          {reports.map((report) => (
            <div
              key={report.id}
              className="card"
              style={{
                cursor: 'pointer',
                border: selectedReport === report.id ? '2px solid #6366f1' : undefined,
                transition: 'all 0.2s'
              }}
              onClick={() => setSelectedReport(report.id)}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)'
                e.currentTarget.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.12)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)'
                e.currentTarget.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.06)'
              }}
            >
              <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
                <div style={{
                  width: '48px',
                  height: '48px',
                  borderRadius: '0.75rem',
                  background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white'
                }}>
                  {report.icon}
                </div>
                <div style={{ flex: 1 }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.25rem', color: '#111827' }}>
                    {report.name}
                  </h3>
                  <p style={{ fontSize: '0.8125rem', color: '#6b7280', margin: 0, fontWeight: 600 }}>
                    {report.size}
                  </p>
                </div>
              </div>

              <p style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '1rem', fontWeight: 500 }}>
                {report.description}
              </p>

              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                paddingTop: '0.75rem',
                borderTop: '1px solid #e5e7eb',
                fontSize: '0.75rem',
                color: '#6b7280',
                fontWeight: 600
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                  <Calendar size={14} />
                  <span>{formatDate(report.generated)}</span>
                </div>
                <button
                  className="action-button primary"
                  style={{ padding: '0.375rem 0.75rem', fontSize: '0.75rem' }}
                  onClick={(e) => {
                    e.stopPropagation();
                    alert(`Downloading ${report.name}...`);
                  }}
                >
                  <Download size={14} />
                  Download
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Report Preview */}
      <div className="card">
        <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '1.25rem', color: '#111827' }}>
          Report Preview - {reports.find(r => r.id === selectedReport)?.name}
        </h2>

        <div style={{
          background: '#f9fafb',
          padding: '1.5rem',
          borderRadius: '0.5rem',
          border: '1px solid #e5e7eb',
          minHeight: '300px'
        }}>
          <div style={{ marginBottom: '1.5rem' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.75rem', color: '#6366f1' }}>
              Executive Summary
            </h3>
            <p style={{ fontSize: '0.875rem', color: '#111827', lineHeight: 1.6, fontWeight: 500 }}>
              During the reporting period, the fraud detection system processed {summaryData.totalCases} cases,
              identifying {summaryData.fraudDetected} instances of fraudulent activity. The system maintained
              a {((summaryData.falsePositives / summaryData.totalCases) * 100).toFixed(1)}% false positive rate
              while successfully preventing {formatCurrency(summaryData.amountSaved)} in fraudulent transactions.
            </p>
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.75rem', color: '#6366f1' }}>
              Key Findings
            </h3>
            <ul style={{ fontSize: '0.875rem', color: '#111827', lineHeight: 1.8, paddingLeft: '1.25rem', fontWeight: 500 }}>
              <li>Average resolution time decreased to {summaryData.avgResolutionTime}, a 15% improvement</li>
              <li>Card fraud remains the most common fraud type at 35% of total cases</li>
              <li>International wire transfers show the highest average risk score at 82%</li>
              <li>Impossible travel detection identified 12 account takeover attempts</li>
              <li>Cryptocurrency-related fraud increased by 23% compared to previous period</li>
            </ul>
          </div>

          <div>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.75rem', color: '#6366f1' }}>
              Recommendations
            </h3>
            <ul style={{ fontSize: '0.875rem', color: '#111827', lineHeight: 1.8, paddingLeft: '1.25rem', fontWeight: 500 }}>
              <li>Enhance monitoring for cryptocurrency exchange transactions</li>
              <li>Implement stricter verification for early morning ATM withdrawals</li>
              <li>Add additional checks for first-time international wire transfers</li>
              <li>Review and update device fingerprinting algorithms</li>
              <li>Increase training for junior analysts on rapid succession patterns</li>
            </ul>
          </div>
        </div>

        <div style={{ marginTop: '1.5rem', display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
          <button className="action-button secondary">
            <Filter size={16} />
            Customize
          </button>
          <button className="action-button primary">
            <Download size={16} />
            Download Full Report
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReportsPage;
