import React from 'react';
import { AlertTriangle, CheckCircle, Clock } from 'lucide-react';
import { Transaction } from '../types';
import '../styles/banking.css';

interface TransactionCardProps {
  transaction: Transaction;
  onInvestigate?: (transactionId: string) => void;
  compact?: boolean;
}

const TransactionCard: React.FC<TransactionCardProps> = ({ 
  transaction, 
  onInvestigate,
  compact = false 
}) => {
  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR'
    }).format(amount);
  };

  const formatDate = (timestamp: string): string => {
    return new Date(timestamp).toLocaleString('en-IN', {
      dateStyle: 'short',
      timeStyle: 'short'
    });
  };

  const getRiskBadge = () => {
    if (transaction.status === 'fraudulent') {
      return (
        <span className="risk-badge critical">
          <AlertTriangle size={14} />
          Fraudulent
        </span>
      );
    }
    if (transaction.status === 'suspicious') {
      return (
        <span className="risk-badge high">
          <Clock size={14} />
          Suspicious
        </span>
      );
    }
    return (
      <span className="risk-badge low">
        <CheckCircle size={14} />
        Safe
      </span>
    );
  };

  const getCardClassName = (): string => {
    const baseClass = 'banking-card';
    if (transaction.status === 'fraudulent') return `${baseClass} fraud-alert`;
    if (transaction.status === 'safe') return `${baseClass} safe`;
    return baseClass;
  };

  if (compact) {
    return (
      <div className={getCardClassName()} style={{ padding: '16px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div style={{ fontSize: '14px', fontWeight: '600', marginBottom: '4px' }}>
              {transaction.id}
            </div>
            <div style={{ fontSize: '12px', opacity: 0.8 }}>
              {transaction.type.replace('_', ' ').toUpperCase()}
            </div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div className="amount-display" style={{ fontSize: '18px' }}>
              {formatCurrency(transaction.amount)}
            </div>
            {getRiskBadge()}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={getCardClassName()}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div>
          <h3 style={{ fontSize: '18px', fontWeight: '700', marginBottom: '4px' }}>
            {transaction.id}
          </h3>
          <p style={{ fontSize: '14px', opacity: 0.8, margin: 0 }}>
            User: {transaction.userId}
          </p>
        </div>
        {getRiskBadge()}
      </div>

      <div className="amount-display large">
        {formatCurrency(transaction.amount)}
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: '1fr 1fr', 
        gap: '12px',
        marginTop: '16px',
        paddingTop: '16px',
        borderTop: '1px solid rgba(255, 255, 255, 0.1)'
      }}>
        <div>
          <div style={{ fontSize: '12px', opacity: 0.6, marginBottom: '4px' }}>
            Type
          </div>
          <div style={{ fontSize: '14px', fontWeight: '500' }}>
            {transaction.type.replace('_', ' ').toUpperCase()}
          </div>
        </div>
        <div>
          <div style={{ fontSize: '12px', opacity: 0.6, marginBottom: '4px' }}>
            Location
          </div>
          <div style={{ fontSize: '14px', fontWeight: '500' }}>
            {transaction.location}
          </div>
        </div>
        <div>
          <div style={{ fontSize: '12px', opacity: 0.6, marginBottom: '4px' }}>
            Timestamp
          </div>
          <div style={{ fontSize: '14px', fontWeight: '500' }}>
            {formatDate(transaction.timestamp)}
          </div>
        </div>
        <div>
          <div style={{ fontSize: '12px', opacity: 0.6, marginBottom: '4px' }}>
            Risk Score
          </div>
          <div style={{ fontSize: '14px', fontWeight: '500' }}>
            {(transaction.riskScore * 100).toFixed(0)}%
          </div>
        </div>
      </div>

      {transaction.flags.length > 0 && (
        <div style={{ marginTop: '16px' }}>
          <div style={{ fontSize: '12px', opacity: 0.6, marginBottom: '8px' }}>
            Fraud Indicators
          </div>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {transaction.flags.map((flag, idx) => (
              <span 
                key={idx}
                style={{
                  padding: '4px 12px',
                  background: 'rgba(255, 71, 87, 0.2)',
                  border: '1px solid rgba(255, 71, 87, 0.5)',
                  borderRadius: '12px',
                  fontSize: '11px',
                  fontWeight: '500'
                }}
              >
                {flag.replace('_', ' ')}
              </span>
            ))}
          </div>
        </div>
      )}

      {onInvestigate && (
        <button 
          className="action-button primary"
          onClick={() => onInvestigate(transaction.id)}
          style={{ 
            width: '100%', 
            marginTop: '16px',
            padding: '12px'
          }}
        >
          Investigate Transaction
        </button>
      )}
    </div>
  );
};

export default TransactionCard;
