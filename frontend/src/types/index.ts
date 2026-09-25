// Banking Transaction Types
export interface Transaction {
  id: string;
  userId: string;
  amount: number;
  timestamp: string;
  type: 'withdrawal' | 'purchase' | 'transfer' | 'wire_transfer' | 'deposit';
  location: string;
  status: 'safe' | 'suspicious' | 'fraudulent';
  riskScore: number;
  flags: string[];
  merchant?: string;
  category?: string;
  description?: string;
}

// Investigation Types
export interface Investigation {
  id: string;
  transactionId: string;
  status: 'pending' | 'in_progress' | 'completed' | 'escalated';
  createdAt: string;
  updatedAt: string;
  assignedTo?: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  findings: Finding[];
  recommendation?: Recommendation;
}

export interface Finding {
  id: string;
  type: string;
  description: string;
  severity: 'info' | 'warning' | 'critical';
  evidence: Evidence[];
  timestamp: string;
}

export interface Evidence {
  id: string;
  type: 'transaction' | 'user_behavior' | 'location' | 'device' | 'pattern';
  description: string;
  data: Record<string, any>;
  relevance: number;
}

export interface Recommendation {
  action: 'approve' | 'reject' | 'review' | 'block_account' | 'request_verification';
  confidence: number;
  reasoning: string;
  suggestedActions: string[];
}

// User Types
export interface User {
  id: string;
  name: string;
  email: string;
  accountNumber: string;
  riskProfile: 'low' | 'medium' | 'high';
  registrationDate: string;
  lastActivity: string;
  totalTransactions: number;
  flaggedTransactions: number;
}

// Analytics Types
export interface FraudMetrics {
  totalTransactions: number;
  fraudulentCount: number;
  suspiciousCount: number;
  safeCount: number;
  totalAmount: number;
  fraudAmount: number;
  preventedAmount: number;
  fraudRate: number;
}

export interface TrendData {
  date: string;
  fraudulent: number;
  suspicious: number;
  safe: number;
}

export interface VolumeData {
  hour: string;
  count: number;
  amount: number;
}

export interface FraudTypeDistribution {
  name: string;
  value: number;
  color: string;
}

export interface RiskDistribution {
  range: string;
  count: number;
  color: string;
}

// Case Types
export interface Case {
  id: string;
  title: string;
  description: string;
  status: 'open' | 'investigating' | 'resolved' | 'closed';
  priority: 'low' | 'medium' | 'high' | 'critical';
  assignedTo?: string;
  createdAt: string;
  updatedAt: string;
  investigations: Investigation[];
  relatedTransactions: Transaction[];
  totalAmount: number;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

// Filter Types
export interface TransactionFilter {
  status?: 'safe' | 'suspicious' | 'fraudulent';
  dateFrom?: string;
  dateTo?: string;
  amountMin?: number;
  amountMax?: number;
  userId?: string;
  type?: Transaction['type'];
  riskScoreMin?: number;
  riskScoreMax?: number;
}

export interface CaseFilter {
  status?: Case['status'];
  priority?: Case['priority'];
  assignedTo?: string;
  dateFrom?: string;
  dateTo?: string;
}

// Dashboard Stats
export interface DashboardStats {
  metrics: FraudMetrics;
  recentTransactions: Transaction[];
  activeCases: Case[];
  alerts: Alert[];
  trends: TrendData[];
}

export interface Alert {
  id: string;
  type: 'fraud_detected' | 'high_risk_user' | 'unusual_pattern' | 'system';
  severity: 'info' | 'warning' | 'critical';
  title: string;
  message: string;
  timestamp: string;
  read: boolean;
  actionRequired: boolean;
}

// Upload Types
export interface UploadResult {
  success: boolean;
  fileName: string;
  recordsProcessed: number;
  recordsValid: number;
  recordsInvalid: number;
  errors?: string[];
}

// Network Graph Types
export interface NetworkNode {
  id: string;
  type: 'user' | 'transaction' | 'account' | 'device' | 'location';
  label: string;
  data: Record<string, any>;
  risk?: number;
}

export interface NetworkEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  label?: string;
  weight?: number;
}

export interface NetworkGraph {
  nodes: NetworkNode[];
  edges: NetworkEdge[];
}
