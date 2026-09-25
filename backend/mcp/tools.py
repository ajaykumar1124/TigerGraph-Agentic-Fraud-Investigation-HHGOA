"""
TigerGraph MCP Tools - Query and analysis functions exposed to LLM
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from backend.tigergraph.client import get_client
from backend.graphrag.retriever import GraphRAGRetriever

logger = logging.getLogger(__name__)


class TigerGraphTools:
    """MCP tools for TigerGraph graph operations"""

    def __init__(self, client=None, retriever=None):
        """Initialize tools"""
        self.client = client or get_client()
        self.retriever = retriever or GraphRAGRetriever()

    def query_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Query user profile and risk indicators
        
        Tool: query_user_profile
        Args: user_id (string)
        Returns: User profile with risk score and transaction history
        """
        try:
            user = self.client.get_vertex("User", str(user_id))
            
            # Get transaction history
            neighbors = self.client.get_neighbors("User", str(user_id), edge_type="HAS_TRANSACTION", max_depth=1)
            
            return {
                "success": True,
                "user_id": user_id,
                "profile": user,
                "transaction_count": len(neighbors.get("Transaction", [])) if neighbors else 0,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to query user: {str(e)}")
            return {"success": False, "error": str(e)}

    def query_transaction_details(self, transaction_id: str) -> Dict[str, Any]:
        """
        Query transaction details and relationships
        
        Tool: query_transaction_details
        Args: transaction_id (string)
        Returns: Transaction with user, card, device, merchant, IP info
        """
        try:
            txn = self.client.get_vertex("Transaction", transaction_id)
            neighbors = self.client.get_neighbors("Transaction", transaction_id, max_depth=1)
            
            return {
                "success": True,
                "transaction_id": transaction_id,
                "transaction": txn,
                "related_entities": neighbors,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to query transaction: {str(e)}")
            return {"success": False, "error": str(e)}

    def query_card_details(self, card_id: str) -> Dict[str, Any]:
        """
        Query card profile and transaction history
        
        Tool: query_card_details
        Args: card_id (string)
        Returns: Card information with transaction history
        """
        try:
            card = self.client.get_vertex("Card", str(card_id))
            
            # Get transactions
            neighbors = self.client.get_neighbors("Card", str(card_id), edge_type="USED_IN_TRANSACTION", max_depth=1)
            
            return {
                "success": True,
                "card_id": card_id,
                "card": card,
                "transaction_count": len(neighbors.get("Transaction", [])) if neighbors else 0,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to query card: {str(e)}")
            return {"success": False, "error": str(e)}

    def query_device_details(self, device_id: str) -> Dict[str, Any]:
        """
        Query device profile and usage history
        
        Tool: query_device_details
        Args: device_id (string)
        Returns: Device information with connected users and IPs
        """
        try:
            device = self.client.get_vertex("Device", device_id)
            neighbors = self.client.get_neighbors("Device", device_id, max_depth=2)
            
            return {
                "success": True,
                "device_id": device_id,
                "device": device,
                "connected_entities": neighbors,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to query device: {str(e)}")
            return {"success": False, "error": str(e)}

    def query_merchant_profile(self, merchant_id: str) -> Dict[str, Any]:
        """
        Query merchant profile and risk category
        
        Tool: query_merchant_profile
        Args: merchant_id (string)
        Returns: Merchant information with risk level
        """
        try:
            merchant = self.client.get_vertex("Merchant", str(merchant_id))
            neighbors = self.client.get_neighbors("Merchant", str(merchant_id), max_depth=1)
            
            return {
                "success": True,
                "merchant_id": merchant_id,
                "merchant": merchant,
                "transaction_count": len(neighbors.get("Transaction", [])) if neighbors else 0,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to query merchant: {str(e)}")
            return {"success": False, "error": str(e)}

    def query_ip_address_risk(self, ip_address: str) -> Dict[str, Any]:
        """
        Query IP address risk assessment
        
        Tool: query_ip_address_risk
        Args: ip_address (string, e.g., "192.168.1.1")
        Returns: IP risk level, VPN/proxy status, geolocation
        """
        try:
            ip = self.client.get_vertex("IPAddress", ip_address)
            neighbors = self.client.get_neighbors("IPAddress", ip_address, max_depth=1)
            
            return {
                "success": True,
                "ip_address": ip_address,
                "ip_info": ip,
                "connected_devices": len(neighbors.get("Device", [])) if neighbors else 0,
                "risk_assessment": {
                    "is_vpn": ip.get("is_vpn", False),
                    "is_proxy": ip.get("is_proxy", False),
                    "is_datacenter": ip.get("is_datacenter", False),
                    "risk_level": ip.get("risk_level", "UNKNOWN"),
                },
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to query IP: {str(e)}")
            return {"success": False, "error": str(e)}

    def search_fraud_patterns(self, pattern_name: str) -> Dict[str, Any]:
        """
        Search for fraud pattern information
        
        Tool: search_fraud_patterns
        Args: pattern_name (string, e.g., "velocity_attack")
        Returns: Pattern definition and risk level
        """
        try:
            # Get all patterns and filter
            patterns = self.client.query_vertices_by_type("FraudPattern", limit=100)
            
            matching = [p for p in patterns if pattern_name.lower() in p.get("pattern_name", "").lower()]
            
            return {
                "success": True,
                "search_term": pattern_name,
                "matches": matching,
                "total_patterns": len(patterns),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to search patterns: {str(e)}")
            return {"success": False, "error": str(e)}

    def retrieve_evidence(self, case_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve evidence for a fraud case using GraphRAG
        
        Tool: retrieve_evidence
        Args: case_context (dict with user_id, indicators, etc.)
        Returns: Relevant policies, patterns, and historical cases
        """
        try:
            evidence = self.retriever.retrieve_evidence(
                case_id="case_query",
                investigation_context=case_context,
                top_k=5
            )
            
            return {
                "success": True,
                "evidence": evidence,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to retrieve evidence: {str(e)}")
            return {"success": False, "error": str(e)}

    def check_policies(self, case_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check which fraud policies are violated
        
        Tool: check_policies
        Args: case_context (dict with indicators)
        Returns: Triggered and passed policies
        """
        try:
            policy_results = self.retriever.get_policy_check_results(case_context)
            
            return {
                "success": True,
                "policies": policy_results,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to check policies: {str(e)}")
            return {"success": False, "error": str(e)}

    def query_case_history(self, case_id: str) -> Dict[str, Any]:
        """
        Query case history and related information
        
        Tool: query_case_history
        Args: case_id (string)
        Returns: Case details, evidence, and findings
        """
        try:
            case = self.client.get_vertex("FraudCase", case_id)
            neighbors = self.client.get_neighbors("FraudCase", case_id, max_depth=2)
            
            return {
                "success": True,
                "case_id": case_id,
                "case": case,
                "related_entities": neighbors,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to query case: {str(e)}")
            return {"success": False, "error": str(e)}

    def create_fraud_case(
        self,
        initiator: str,
        user_id: str,
        transaction_id: str,
        risk_level: str,
        indicators: List[str],
    ) -> Dict[str, Any]:
        """
        Create a new fraud case in the graph
        
        Tool: create_fraud_case
        Args: initiator, user_id, transaction_id, risk_level, indicators (list)
        Returns: New case ID and confirmation
        """
        try:
            case_id = f"case_{datetime.now().timestamp():.0f}"
            
            # Create FraudCase vertex
            self.client.upsert_vertex(
                "FraudCase",
                case_id,
                {
                    "initiator": initiator,
                    "case_status": "OPEN",
                    "risk_level": risk_level,
                    "confidence_score": 0.0,
                    "investigation_depth": 0,
                    "created_at": int(datetime.now().timestamp()),
                    "updated_at": int(datetime.now().timestamp()),
                },
            )
            
            # Link to User
            if user_id:
                self.client.upsert_edge(
                    "INVESTIGATES_USER",
                    "FraudCase",
                    case_id,
                    "User",
                    str(user_id),
                    {"investigation_date": int(datetime.now().timestamp())},
                )
            
            # Link to Transaction
            if transaction_id:
                self.client.upsert_edge(
                    "INVESTIGATES_TRANSACTION",
                    "FraudCase",
                    case_id,
                    "Transaction",
                    transaction_id,
                    {"investigation_date": int(datetime.now().timestamp()), "risk_score": 0.5},
                )
            
            return {
                "success": True,
                "case_id": case_id,
                "initiator": initiator,
                "status": "OPEN",
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to create case: {str(e)}")
            return {"success": False, "error": str(e)}

    def update_case_status(
        self, case_id: str, status: str, next_action: str = None, findings: str = None
    ) -> Dict[str, Any]:
        """
        Update case status and findings
        
        Tool: update_case_status
        Args: case_id, status (OPEN, INVESTIGATING, RESOLVED), next_action, findings
        Returns: Updated case
        """
        try:
            # Get current case
            case = self.client.get_vertex("FraudCase", case_id)
            
            # Update attributes
            case.update({
                "case_status": status,
                "next_action": next_action or "PENDING",
                "updated_at": int(datetime.now().timestamp()),
            })
            
            # If resolved, set resolution date
            if status == "RESOLVED":
                case["resolved_at"] = int(datetime.now().timestamp())
            
            # Upsert updated case
            self.client.upsert_vertex("FraudCase", case_id, case)
            
            return {
                "success": True,
                "case_id": case_id,
                "status": status,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to update case: {str(e)}")
            return {"success": False, "error": str(e)}

    def add_case_evidence(self, case_id: str, evidence_text: str, evidence_type: str = "general") -> Dict[str, Any]:
        """
        Add evidence to a case
        
        Tool: add_case_evidence
        Args: case_id, evidence_text, evidence_type
        Returns: Evidence ID and confirmation
        """
        try:
            evidence_id = f"evidence_{case_id}_{evidence_type}_{int(datetime.now().timestamp())}"
            
            # Create Evidence vertex
            self.client.upsert_vertex(
                "Evidence",
                evidence_id,
                {
                    "evidence_type": evidence_type,
                    "description": evidence_text,
                    "weight_score": 0.5,
                    "data_value": evidence_text,
                    "collected_at": int(datetime.now().timestamp()),
                },
            )
            
            # Link to Case
            self.client.upsert_edge(
                "COLLECTS_EVIDENCE",
                "FraudCase",
                case_id,
                "Evidence",
                evidence_id,
                {"collected_at": int(datetime.now().timestamp()), "evidence_order": 1},
            )
            
            return {
                "success": True,
                "evidence_id": evidence_id,
                "case_id": case_id,
                "type": evidence_type,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to add evidence: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_graph_stats(self) -> Dict[str, Any]:
        """
        Get overall graph statistics
        
        Tool: get_graph_stats
        Args: (none)
        Returns: Vertex and edge counts
        """
        try:
            stats = self.client.get_graph_stats()
            return {
                "success": True,
                "stats": stats,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {str(e)}")
            return {"success": False, "error": str(e)}
