"""
Mock TigerGraph Service (Works Offline)
Use this when TigerGraph Cloud is not accessible
Stores data in memory for development/testing
"""

from typing import Dict, List, Optional
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class MockTigerGraphService:
    """Mock TigerGraph service for offline development"""
    
    def __init__(self):
        self.connected = True
        self.users = {}
        self.transactions = {}
        self.devices = {}
        self.fraud_cases = {}
        self.edges = []
        
        logger.info("🔧 Using Mock TigerGraph Service (Offline Mode)")
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample data into mock database"""
        # Sample users
        self.users = {
            "USR_1001": {
                "user_id": "USR_1001",
                "email": "user1@example.com",
                "phone": "+91-9876543210",
                "kyc_status": "verified",
                "risk_level": "medium",
                "total_transactions": 10,
                "total_amount": 50000.0
            },
            "USR_1002": {
                "user_id": "USR_1002",
                "email": "user2@example.com",
                "phone": "+91-9876543211",
                "kyc_status": "verified",
                "risk_level": "low",
                "total_transactions": 5,
                "total_amount": 10000.0
            },
            "USR_1003": {
                "user_id": "USR_1003",
                "email": "user3@example.com",
                "phone": "+91-9876543212",
                "kyc_status": "pending",
                "risk_level": "high",
                "total_transactions": 3,
                "total_amount": 75000.0
            }
        }
        
        # Sample transactions
        self.transactions = {
            "TXN_2026_001": {
                "transaction_id": "TXN_2026_001",
                "user_id": "USR_1001",
                "amount": 15000.0,
                "timestamp": "2026-09-23T10:15:30",
                "transaction_type": "card_payment",
                "status": "flagged",
                "risk_score": 0.92,
                "is_fraud": True,
                "location": "Mumbai",
                "device_id": "DEV_001",
                "ip_address": "192.168.1.100",
                "merchant_id": "MERCH_001"
            },
            "TXN_2026_002": {
                "transaction_id": "TXN_2026_002",
                "user_id": "USR_1002",
                "amount": 250.0,
                "timestamp": "2026-09-23T09:30:15",
                "transaction_type": "online_purchase",
                "status": "approved",
                "risk_score": 0.12,
                "is_fraud": False,
                "location": "Delhi",
                "device_id": "DEV_002",
                "ip_address": "192.168.1.101",
                "merchant_id": "MERCH_002"
            },
            "TXN_2026_003": {
                "transaction_id": "TXN_2026_003",
                "user_id": "USR_1003",
                "amount": 8500.0,
                "timestamp": "2026-09-23T11:45:20",
                "transaction_type": "transfer",
                "status": "suspicious",
                "risk_score": 0.68,
                "is_fraud": False,
                "location": "Mobile App",
                "device_id": "DEV_003",
                "ip_address": "192.168.1.102",
                "merchant_id": "MERCH_003"
            }
        }
        
        # Sample fraud cases
        self.fraud_cases = {
            "CASE_2026_001": {
                "case_id": "CASE_2026_001",
                "transaction_id": "TXN_2026_001",
                "status": "open",
                "priority": "critical",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "assigned_to": "fraud_analyst_1",
                "resolution": None,
                "notes": "Suspicious large transaction in unusual location"
            }
        }
        
        logger.info(f"✅ Loaded {len(self.users)} users, {len(self.transactions)} transactions")
    
    def get_connection_status(self) -> Dict:
        """Get mock connection status"""
        return {
            "connected": True,
            "mode": "MOCK (Offline)",
            "host": "localhost (in-memory)",
            "graph": "FraudInvestigation (Mock)",
            "version": "Mock v1.0",
            "note": "Using mock data - Configure TigerGraph Cloud for real data"
        }
    
    def get_vertex_count(self, vertex_type: str) -> int:
        """Get count of vertices by type"""
        counts = {
            "User": len(self.users),
            "Transaction": len(self.transactions),
            "FraudCase": len(self.fraud_cases),
            "Device": len(self.devices)
        }
        return counts.get(vertex_type, 0)
    
    def get_transactions(self, limit: int = 100) -> List[Dict]:
        """Get transactions"""
        txns = list(self.transactions.values())
        return txns[:limit]
    
    def get_transaction_by_id(self, transaction_id: str) -> Optional[Dict]:
        """Get specific transaction"""
        return self.transactions.get(transaction_id)
    
    def get_user_transactions(self, user_id: str) -> List[Dict]:
        """Get all transactions for a user"""
        user_txns = [
            txn for txn in self.transactions.values()
            if txn.get("user_id") == user_id
        ]
        return user_txns
    
    def upsert_transaction(self, transaction_data: Dict) -> bool:
        """Insert or update a transaction"""
        try:
            transaction_id = transaction_data.get("transaction_id")
            if not transaction_id:
                transaction_id = f"TXN_{uuid.uuid4().hex[:8].upper()}"
                transaction_data["transaction_id"] = transaction_id
            
            self.transactions[transaction_id] = transaction_data
            logger.info(f"✅ Upserted transaction: {transaction_id}")
            return True
        except Exception as e:
            logger.error(f"Error upserting transaction: {e}")
            return False
    
    def create_fraud_case(self, case_data: Dict) -> bool:
        """Create a fraud case"""
        try:
            case_id = case_data.get("case_id")
            if not case_id:
                case_id = f"CASE_{uuid.uuid4().hex[:8].upper()}"
                case_data["case_id"] = case_id
            
            case_data["created_at"] = datetime.now().isoformat()
            case_data["updated_at"] = datetime.now().isoformat()
            
            self.fraud_cases[case_id] = case_data
            logger.info(f"✅ Created fraud case: {case_id}")
            return True
        except Exception as e:
            logger.error(f"Error creating fraud case: {e}")
            return False
    
    def link_transaction_to_case(
        self,
        transaction_id: str,
        case_id: str
    ) -> bool:
        """Link a transaction to a fraud case"""
        try:
            self.edges.append({
                "type": "RELATED_CASE",
                "from": transaction_id,
                "to": case_id,
                "timestamp": datetime.now().isoformat()
            })
            logger.info(f"✅ Linked {transaction_id} to case {case_id}")
            return True
        except Exception as e:
            logger.error(f"Error linking transaction to case: {e}")
            return False
    
    def get_fraud_cases(self, status: Optional[str] = None) -> List[Dict]:
        """Get fraud cases, optionally filtered by status"""
        cases = list(self.fraud_cases.values())
        
        if status:
            cases = [c for c in cases if c.get("status") == status]
        
        return cases
    
    def run_fraud_detection_query(self) -> List[Dict]:
        """Run fraud detection pattern query"""
        fraud_transactions = [
            t for t in self.transactions.values()
            if t.get("risk_score", 0) > 0.7
        ]
        return fraud_transactions
    
    def add_user(self, user_data: Dict) -> bool:
        """Add a new user"""
        try:
            user_id = user_data.get("user_id")
            if not user_id:
                user_id = f"USR_{uuid.uuid4().hex[:8].upper()}"
                user_data["user_id"] = user_id
            
            self.users[user_id] = user_data
            logger.info(f"✅ Added user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding user: {e}")
            return False
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        return list(self.users.values())
    
    def get_fraud_case_by_id(self, case_id: str) -> Optional[Dict]:
        """Get specific fraud case by ID"""
        return self.fraud_cases.get(case_id)
    
    def get_case_transactions(self, case_id: str, limit: int = 100) -> List[Dict]:
        """Get transactions related to a fraud case"""
        # Find transactions linked to this case
        related_txns = []
        
        for edge in self.edges:
            if edge.get('edge_type') == 'RELATED_CASE' and edge.get('to_id') == case_id:
                txn_id = edge.get('from_id')
                if txn_id in self.transactions:
                    related_txns.append(self.transactions[txn_id])
        
        return related_txns[:limit]
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        return self.users.get(user_id)


# Global mock instance
mock_tigergraph_service = MockTigerGraphService()
