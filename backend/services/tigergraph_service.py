"""
TigerGraph Service with Automatic Mock Fallback
Handles all TigerGraph database operations
Falls back to mock mode if cloud connection fails
"""

import pyTigerGraph as tg
from typing import Dict, List, Optional
import logging
from backend.config import settings

logger = logging.getLogger(__name__)


class TigerGraphService:
    """TigerGraph Service with Mock Fallback"""
    
    def __init__(self):
        self.conn = None
        self.connected = False
        self.mode = "CLOUD"
        self._mock_service = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize TigerGraph connection with fallback"""
        try:
            logger.info(f"🔗 Attempting TigerGraph Cloud connection...")
            logger.info(f"   Host: {settings.tigergraph.host}")
            logger.info(f"   Graph: {settings.tigergraph.graph_name}")
            
            self.conn = tg.TigerGraphConnection(
                host=settings.tigergraph.host,
                graphname=settings.tigergraph.graph_name,
                username=settings.tigergraph.username or "tigergraph",
                apiToken=settings.tigergraph.api_token,
                useCert=True
            )
            
            # Test connection
            version = self.conn.getVersion()
            logger.info(f"✅ Connected to TigerGraph Cloud {version}")
            self.connected = True
            self.mode = "CLOUD"
            
        except Exception as e:
            logger.warning(f"⚠️  TigerGraph Cloud connection failed: {e}")
            logger.info(f"🔧 Falling back to Mock Mode (offline development)")
            
            # Import and use mock service
            from backend.services.mock_tigergraph_service import mock_tigergraph_service
            self._mock_service = mock_tigergraph_service
            self.connected = True
            self.mode = "MOCK"
    
    def _use_mock(self):
        """Check if using mock service"""
        return self.mode == "MOCK" and self._mock_service is not None
    
    def get_connection_status(self) -> Dict:
        """Get connection status"""
        if self._use_mock():
            return self._mock_service.get_connection_status()
        
        if not self.connected or not self.conn:
            return {
                "connected": False,
                "mode": "DISCONNECTED",
                "host": settings.tigergraph.host,
                "graph": settings.tigergraph.graph_name,
                "error": "Not connected"
            }
        
        try:
            version = self.conn.getVersion()
            graphs = self.conn.getGraphs()
            
            return {
                "connected": True,
                "mode": "CLOUD",
                "host": settings.tigergraph.host,
                "graph": settings.tigergraph.graph_name,
                "version": version,
                "available_graphs": graphs
            }
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return {
                "connected": False,
                "mode": "ERROR",
                "error": str(e)
            }
    
    def get_vertex_count(self, vertex_type: str) -> int:
        """Get count of vertices by type"""
        if self._use_mock():
            return self._mock_service.get_vertex_count(vertex_type)
        
        if not self.connected:
            return 0
        
        try:
            return self.conn.getVertexCount(vertex_type)
        except Exception as e:
            logger.error(f"Error getting vertex count: {e}")
            return 0
    
    def get_transactions(self, limit: int = 100) -> List[Dict]:
        """Get recent transactions"""
        if self._use_mock():
            return self._mock_service.get_transactions(limit)
        
        if not self.connected:
            return []
        
        try:
            transactions = self.conn.getVertices(
                vertexType="Transaction",
                limit=limit
            )
            return transactions
        except Exception as e:
            logger.error(f"Error getting transactions: {e}")
            return []
    
    def get_transaction_by_id(self, transaction_id: str) -> Optional[Dict]:
        """Get specific transaction"""
        if self._use_mock():
            return self._mock_service.get_transaction_by_id(transaction_id)
        
        if not self.connected:
            return None
        
        try:
            txn = self.conn.getVerticesById(
                vertexType="Transaction",
                vertexIds=[transaction_id]
            )
            return txn[0] if txn else None
        except Exception as e:
            logger.error(f"Error getting transaction: {e}")
            return None
    
    def get_user_transactions(self, user_id: str) -> List[Dict]:
        """Get all transactions for a user"""
        if self._use_mock():
            return self._mock_service.get_user_transactions(user_id)
        
        if not self.connected:
            return []
        
        try:
            edges = self.conn.getEdges(
                sourceVertexType="User",
                sourceVertexId=user_id,
                edgeType="PERFORMED",
                targetVertexType="Transaction"
            )
            return edges
        except Exception as e:
            logger.error(f"Error getting user transactions: {e}")
            return []
    
    def upsert_transaction(self, transaction_data: Dict) -> bool:
        """Insert or update a transaction"""
        if self._use_mock():
            return self._mock_service.upsert_transaction(transaction_data)
        
        if not self.connected:
            return False
        
        try:
            transaction_id = transaction_data.get("transaction_id")
            self.conn.upsertVertex(
                vertexType="Transaction",
                vertexId=transaction_id,
                attributes=transaction_data
            )
            logger.info(f"✅ Upserted transaction: {transaction_id}")
            return True
        except Exception as e:
            logger.error(f"Error upserting transaction: {e}")
            return False
    
    def create_fraud_case(self, case_data: Dict) -> bool:
        """Create a fraud case"""
        if self._use_mock():
            return self._mock_service.create_fraud_case(case_data)
        
        if not self.connected:
            return False
        
        try:
            case_id = case_data.get("case_id")
            self.conn.upsertVertex(
                vertexType="FraudCase",
                vertexId=case_id,
                attributes=case_data
            )
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
        if self._use_mock():
            return self._mock_service.link_transaction_to_case(transaction_id, case_id)
        
        if not self.connected:
            return False
        
        try:
            self.conn.upsertEdge(
                sourceVertexType="Transaction",
                sourceVertexId=transaction_id,
                edgeType="RELATED_CASE",
                targetVertexType="FraudCase",
                targetVertexId=case_id
            )
            logger.info(f"✅ Linked {transaction_id} to case {case_id}")
            return True
        except Exception as e:
            logger.error(f"Error linking transaction to case: {e}")
            return False
    
    def get_fraud_cases(self, status: Optional[str] = None) -> List[Dict]:
        """Get fraud cases, optionally filtered by status"""
        if self._use_mock():
            return self._mock_service.get_fraud_cases(status)
        
        if not self.connected:
            return []
        
        try:
            cases = self.conn.getVertices(
                vertexType="FraudCase",
                limit=1000
            )
            
            if status:
                cases = [c for c in cases if c.get("status") == status]
            
            return cases
        except Exception as e:
            logger.error(f"Error getting fraud cases: {e}")
            return []
    
    def get_fraud_case_by_id(self, case_id: str) -> Optional[Dict]:
        """Get specific fraud case by ID"""
        if self._use_mock():
            return self._mock_service.get_fraud_case_by_id(case_id)
        
        if not self.connected:
            return None
        
        try:
            cases = self.conn.getVerticesById(
                vertexType="FraudCase",
                vertexIds=[case_id]
            )
            return cases[0] if cases else None
        except Exception as e:
            logger.error(f"Error getting fraud case: {e}")
            return None
    
    def get_case_transactions(self, case_id: str, limit: int = 100) -> List[Dict]:
        """Get all transactions related to a fraud case"""
        if self._use_mock():
            return self._mock_service.get_case_transactions(case_id, limit)
        
        if not self.connected:
            return []
        
        try:
            # Get transactions linked to this case
            edges = self.conn.getEdges(
                sourceVertexType="Transaction",
                edgeType="RELATED_CASE",
                targetVertexType="FraudCase",
                targetVertexId=case_id
            )
            
            # Get transaction details
            txn_ids = [edge.get('from_id') for edge in edges]
            if not txn_ids:
                return []
            
            transactions = self.conn.getVerticesById(
                vertexType="Transaction",
                vertexIds=txn_ids[:limit]
            )
            return transactions
        except Exception as e:
            logger.error(f"Error getting case transactions: {e}")
            return []
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        if self._use_mock():
            return self._mock_service.get_user_by_id(user_id)
        
        if not self.connected:
            return None
        
        try:
            users = self.conn.getVerticesById(
                vertexType="User",
                vertexIds=[user_id]
            )
            return users[0] if users else None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def run_fraud_detection_query(self) -> List[Dict]:
        """Run fraud detection pattern query"""
        if self._use_mock():
            return self._mock_service.run_fraud_detection_query()
        
        if not self.connected:
            return []
        
        try:
            transactions = self.get_transactions(limit=1000)
            fraud_transactions = [
                t for t in transactions 
                if t.get("risk_score", 0) > 0.7
            ]
            return fraud_transactions
        except Exception as e:
            logger.error(f"Error running fraud detection: {e}")
            return []


# Global instance
tigergraph_service = TigerGraphService()
