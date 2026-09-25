"""
GraphRAG Retriever - Evidence retrieval and semantic search
Integrates with TigerGraph for graph-aware evidence collection
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from backend.graphrag.indexer import get_indexer
from backend.tigergraph.client import get_client

logger = logging.getLogger(__name__)


class GraphRAGRetriever:
    """
    Retrieve evidence for fraud investigations using semantic search
    Combines FAISS vector search with TigerGraph graph queries
    """

    def __init__(self, indexer=None, client=None):
        """Initialize retriever"""
        self.indexer = indexer or get_indexer()
        self.client = client or get_client()

    def retrieve_evidence(
        self, case_id: str, investigation_context: Dict[str, Any], top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Retrieve evidence for a fraud case
        
        Args:
            case_id: Fraud case ID
            investigation_context: Context about the case (user, transaction, etc.)
            top_k: Number of results to return
        
        Returns:
            Dictionary with retrieved evidence
        """
        try:
            logger.info(f"Retrieving evidence for case {case_id}")

            evidence = {
                "case_id": case_id,
                "timestamp": datetime.now().isoformat(),
                "policies": [],
                "patterns": [],
                "related_cases": [],
                "graph_neighbors": [],
            }

            # Extract investigation context
            user_id = investigation_context.get("user_id")
            card_id = investigation_context.get("card_id")
            transaction_id = investigation_context.get("transaction_id")
            risk_indicators = investigation_context.get("indicators", [])

            # 1. Retrieve relevant policies
            evidence["policies"] = self._retrieve_policies(risk_indicators, top_k)

            # 2. Retrieve matching fraud patterns
            evidence["patterns"] = self._retrieve_patterns(risk_indicators, top_k)

            # 3. Retrieve similar historical cases
            evidence["related_cases"] = self._retrieve_similar_cases(investigation_context, top_k)

            # 4. Retrieve graph neighbors (connected entities)
            if user_id:
                evidence["graph_neighbors"] = self._get_graph_neighbors(user_id, "User", max_depth=2)

            logger.info(
                f"Retrieved evidence: {len(evidence['policies'])} policies, "
                f"{len(evidence['patterns'])} patterns, "
                f"{len(evidence['related_cases'])} cases, "
                f"{len(evidence['graph_neighbors'])} neighbors"
            )

            return evidence

        except Exception as e:
            logger.error(f"✗ Evidence retrieval failed: {str(e)}")
            raise

    def _retrieve_policies(self, risk_indicators: List[str], top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant fraud policies"""
        try:
            # Create query from risk indicators
            query = " ".join(risk_indicators) if risk_indicators else "fraud policy"

            # Search for policies
            results = self.indexer.search(query, top_k=top_k)

            # Filter for policies
            policies = [doc for doc in results if doc.get("type") == "policy"]

            logger.debug(f"Retrieved {len(policies)} relevant policies")
            return policies

        except Exception as e:
            logger.error(f"✗ Policy retrieval failed: {str(e)}")
            return []

    def _retrieve_patterns(self, risk_indicators: List[str], top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve matching fraud patterns"""
        try:
            # Create query from indicators
            query = " ".join(risk_indicators) if risk_indicators else "fraud pattern"

            # Search for patterns
            results = self.indexer.search(query, top_k=top_k)

            # Filter for patterns
            patterns = [doc for doc in results if doc.get("type") == "fraud_pattern"]

            logger.debug(f"Retrieved {len(patterns)} matching fraud patterns")
            return patterns

        except Exception as e:
            logger.error(f"✗ Pattern retrieval failed: {str(e)}")
            return []

    def _retrieve_similar_cases(
        self, investigation_context: Dict[str, Any], top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve similar historical cases"""
        try:
            # Create case summary from context
            indicators = investigation_context.get("indicators", [])
            merchant = investigation_context.get("merchant", "")
            amount = investigation_context.get("amount", 0)

            case_query = f"fraud case with indicators: {' '.join(indicators)} merchant: {merchant} amount: {amount}"

            # Search for similar cases
            results = self.indexer.search(case_query, top_k=top_k)

            # Filter for case summaries
            cases = [doc for doc in results if doc.get("type") == "case_summary"]

            logger.debug(f"Retrieved {len(cases)} similar historical cases")
            return cases

        except Exception as e:
            logger.error(f"✗ Case retrieval failed: {str(e)}")
            return []

    def _get_graph_neighbors(self, vertex_id: str, vertex_type: str, max_depth: int = 2) -> List[Dict[str, Any]]:
        """Get neighboring vertices from TigerGraph"""
        try:
            neighbors = self.client.get_neighbors(vertex_type, vertex_id, max_depth=max_depth)

            # Format results
            result_list = []
            if isinstance(neighbors, dict):
                for key, value in neighbors.items():
                    result_list.append({"neighbor_type": key, "neighbor": value})

            logger.debug(f"Retrieved {len(result_list)} graph neighbors")
            return result_list

        except Exception as e:
            logger.error(f"✗ Graph neighbor retrieval failed: {str(e)}")
            return []

    def retrieve_evidence_by_query(
        self, query: str, top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve evidence using natural language query
        
        Args:
            query: Natural language query
            top_k: Number of results
        
        Returns:
            List of relevant documents
        """
        try:
            results = self.indexer.search(query, top_k=top_k)
            logger.debug(f"Retrieved {len(results)} documents for query: {query}")
            return results
        except Exception as e:
            logger.error(f"✗ Query retrieval failed: {str(e)}")
            raise

    def add_case_evidence(self, case_id: str, evidence_text: str, evidence_type: str = "general"):
        """Add evidence to a case in the index"""
        try:
            document = {
                "id": f"evidence_{case_id}_{evidence_type}",
                "type": "case_evidence",
                "title": f"Evidence for {case_id}",
                "content": evidence_text,
                "case_id": case_id,
                "evidence_type": evidence_type,
                "added_at": datetime.now().isoformat(),
                "source": "case",
            }

            self.indexer.add_document(document)
            logger.debug(f"Added evidence for case {case_id}")

        except Exception as e:
            logger.error(f"✗ Failed to add case evidence: {str(e)}")
            raise

    def get_policy_check_results(self, case_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check which policies are triggered by the case
        
        Args:
            case_context: Case context with indicators
        
        Returns:
            Dictionary of policy check results
        """
        try:
            indicators = case_context.get("indicators", [])
            policies = self._retrieve_policies(indicators, top_k=10)

            results = {
                "policies_checked": len(policies),
                "policies_triggered": [],
                "policies_passed": [],
            }

            for policy in policies:
                # Simple heuristic: if any indicator matches policy category
                policy_category = policy.get("category", "")
                matched = any(indicator.lower() in policy_category.lower() for indicator in indicators)

                if matched:
                    results["policies_triggered"].append(
                        {
                            "policy_id": policy.get("id"),
                            "policy_name": policy.get("title"),
                            "severity": policy.get("category", "MEDIUM"),
                            "matched_indicators": [ind for ind in indicators if ind.lower() in policy_category.lower()],
                        }
                    )
                else:
                    results["policies_passed"].append({"policy_id": policy.get("id"), "policy_name": policy.get("title")})

            logger.info(f"Policy check: {len(results['policies_triggered'])} triggered, {len(results['policies_passed'])} passed")
            return results

        except Exception as e:
            logger.error(f"✗ Policy check failed: {str(e)}")
            raise

    def get_index_stats(self) -> Dict[str, Any]:
        """Get GraphRAG index statistics"""
        return self.indexer.get_stats()
