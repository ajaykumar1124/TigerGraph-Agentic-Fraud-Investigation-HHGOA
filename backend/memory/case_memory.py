"""
Case Memory System for Fraud Investigation Agent

Stores historical cases and enables similarity-based retrieval for learning.
Uses simple in-memory vector database (can be upgraded to Pinecone/Weaviate).
"""

import json
import hashlib
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import math


@dataclass
class CaseMemoryRecord:
    """A historical case stored in memory."""
    case_id: str
    customer_id: str
    fraud_pattern: str  # ACCOUNT_TAKEOVER, PAYMENT_FRAUD, etc.
    initial_risk_score: float
    final_risk_score: float
    confidence_score: float
    evidence_collected: List[str]  # Evidence types found
    evidence_count: int
    action_recommended: str  # BLOCK_ACCOUNT, HOLD_TRANSACTION, etc.
    action_outcome: str  # CONFIRMED_FRAUD, FALSE_POSITIVE, ALLOWED
    approval_required: bool
    approved_by: Optional[str]
    investigation_duration_hours: int
    narrative: str  # Human-readable summary
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "case_id": self.case_id,
            "customer_id": self.customer_id,
            "fraud_pattern": self.fraud_pattern,
            "initial_risk_score": self.initial_risk_score,
            "final_risk_score": self.final_risk_score,
            "confidence_score": self.confidence_score,
            "evidence_collected": self.evidence_collected,
            "evidence_count": self.evidence_count,
            "action_recommended": self.action_recommended,
            "action_outcome": self.action_outcome,
            "approval_required": self.approval_required,
            "approved_by": self.approved_by,
            "investigation_duration_hours": self.investigation_duration_hours,
            "narrative": self.narrative,
            "created_at": self.created_at
        }


class SimpleVectorStore:
    """
    Simple in-memory vector database.
    
    For production: use Pinecone, Weaviate, or FAISS.
    This uses TF-IDF-like similarity for MVP.
    """
    
    def __init__(self):
        """Initialize vector store."""
        self.cases: Dict[str, CaseMemoryRecord] = {}
        self.vectors: Dict[str, List[float]] = {}
        self.vocabulary: Dict[str, int] = {}
        self.word_index = 0
    
    def add_case(self, record: CaseMemoryRecord) -> str:
        """Add a case to memory."""
        self.cases[record.case_id] = record
        
        # Generate vector representation from narrative
        vector = self._generate_vector(record)
        self.vectors[record.case_id] = vector
        
        return record.case_id
    
    def _generate_vector(self, record: CaseMemoryRecord) -> List[float]:
        """
        Generate a simple vector representation of a case.
        
        Uses:
        - Fraud pattern
        - Evidence types
        - Risk score
        - Outcome
        - Narrative keywords
        """
        vector = []
        
        # Pattern encoding (one-hot-like)
        patterns = ["ACCOUNT_TAKEOVER", "PAYMENT_FRAUD", "CARD_FRAUD", "FRAUD_NETWORK", "VELOCITY_ANOMALY"]
        for p in patterns:
            vector.append(1.0 if record.fraud_pattern == p else 0.0)
        
        # Risk score (normalized)
        vector.append(record.initial_risk_score)
        vector.append(record.final_risk_score)
        vector.append(record.confidence_score)
        
        # Evidence types
        evidence_types = ["SHARED_DEVICE", "SHARED_IP", "VELOCITY_ANOMALY", "NETWORK_ANALYSIS", 
                         "HISTORICAL_CASE", "BEHAVIORAL_ANOMALY", "PATTERN_MATCH", "CUSTOMER_VALIDATION"]
        for et in evidence_types:
            vector.append(1.0 if et in record.evidence_collected else 0.0)
        
        # Evidence count (normalized)
        vector.append(min(record.evidence_count / 10.0, 1.0))
        
        # Action encoding
        actions = ["ALLOW", "HOLD_TRANSACTION", "BLOCK_ACCOUNT", "REQUEST_AUTH", "ESCALATE"]
        for a in actions:
            vector.append(1.0 if record.action_recommended == a else 0.0)
        
        # Outcome encoding
        outcomes = ["CONFIRMED_FRAUD", "FALSE_POSITIVE", "ALLOWED", "PENDING"]
        for o in outcomes:
            vector.append(1.0 if record.action_outcome == o else 0.0)
        
        return vector
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        mag1 = math.sqrt(sum(a * a for a in vec1))
        mag2 = math.sqrt(sum(b * b for b in vec2))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    def find_similar_cases(
        self,
        query_vector: List[float],
        top_k: int = 5,
        similarity_threshold: float = 0.3
    ) -> List[Tuple[CaseMemoryRecord, float]]:
        """
        Find similar cases using vector similarity.
        
        Returns: List of (case, similarity_score) tuples
        """
        similarities = []
        
        for case_id, vector in self.vectors.items():
            similarity = self._cosine_similarity(query_vector, vector)
            if similarity >= similarity_threshold:
                similarities.append((case_id, similarity))
        
        # Sort by similarity descending
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top K
        results = []
        for case_id, similarity in similarities[:top_k]:
            results.append((self.cases[case_id], similarity))
        
        return results
    
    def find_by_fraud_pattern(
        self,
        fraud_pattern: str,
        top_k: int = 5
    ) -> List[Tuple[CaseMemoryRecord, float]]:
        """Find cases by fraud pattern."""
        matching = []
        
        for case_id, record in self.cases.items():
            if record.fraud_pattern == fraud_pattern:
                # Score by how well the outcome aligns
                outcome_score = 1.0 if record.action_outcome == "CONFIRMED_FRAUD" else 0.5
                matching.append((record, outcome_score))
        
        # Sort by score
        matching.sort(key=lambda x: x[1], reverse=True)
        
        return matching[:top_k]


class CaseMemoryManager:
    """Manages case memory and historical learning."""
    
    def __init__(self):
        """Initialize case memory manager."""
        self.vector_store = SimpleVectorStore()
        self.statistics = {
            "total_cases": 0,
            "confirmed_fraud": 0,
            "false_positives": 0,
            "patterns": {},
            "avg_investigation_time": 0,
            "avg_accuracy": 0
        }
    
    def store_case(
        self,
        case_id: str,
        customer_id: str,
        fraud_pattern: str,
        initial_risk: float,
        final_risk: float,
        confidence: float,
        evidence_types: List[str],
        action: str,
        outcome: str,
        approval_required: bool,
        approved_by: Optional[str],
        investigation_duration_hours: int,
        narrative: str
    ) -> str:
        """Store a completed investigation in memory."""
        
        record = CaseMemoryRecord(
            case_id=case_id,
            customer_id=customer_id,
            fraud_pattern=fraud_pattern,
            initial_risk_score=initial_risk,
            final_risk_score=final_risk,
            confidence_score=confidence,
            evidence_collected=evidence_types,
            evidence_count=len(evidence_types),
            action_recommended=action,
            action_outcome=outcome,
            approval_required=approval_required,
            approved_by=approved_by,
            investigation_duration_hours=investigation_duration_hours,
            narrative=narrative
        )
        
        # Add to memory
        self.vector_store.add_case(record)
        
        # Update statistics
        self._update_statistics(record)
        
        return case_id
    
    def _update_statistics(self, record: CaseMemoryRecord):
        """Update aggregated statistics."""
        self.statistics["total_cases"] += 1
        
        if record.action_outcome == "CONFIRMED_FRAUD":
            self.statistics["confirmed_fraud"] += 1
        elif record.action_outcome == "FALSE_POSITIVE":
            self.statistics["false_positives"] += 1
        
        # Pattern statistics
        pattern = record.fraud_pattern
        if pattern not in self.statistics["patterns"]:
            self.statistics["patterns"][pattern] = {"count": 0, "confirmed": 0}
        
        self.statistics["patterns"][pattern]["count"] += 1
        if record.action_outcome == "CONFIRMED_FRAUD":
            self.statistics["patterns"][pattern]["confirmed"] += 1
    
    def retrieve_similar_cases(
        self,
        fraud_pattern: str,
        initial_risk: float,
        confidence: float,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Retrieve similar cases from memory.
        
        Used by agent to learn from past investigations.
        """
        # Build query vector
        patterns = ["ACCOUNT_TAKEOVER", "PAYMENT_FRAUD", "CARD_FRAUD", "FRAUD_NETWORK", "VELOCITY_ANOMALY"]
        query_vec = []
        
        for p in patterns:
            query_vec.append(1.0 if fraud_pattern == p else 0.0)
        
        query_vec.append(initial_risk)
        query_vec.append(0.5)  # placeholder for final risk
        query_vec.append(confidence)
        
        # Find similar cases
        similar_cases = self.vector_store.find_similar_cases(query_vec, top_k=top_k)
        
        results = []
        for case, similarity in similar_cases:
            results.append({
                "case_id": case.case_id,
                "fraud_pattern": case.fraud_pattern,
                "initial_risk": case.initial_risk_score,
                "final_risk": case.final_risk_score,
                "confidence": case.confidence_score,
                "action_recommended": case.action_recommended,
                "action_outcome": case.action_outcome,
                "similarity": round(similarity, 2),
                "evidence_types": case.evidence_collected,
                "narrative": case.narrative[:200] + "..." if len(case.narrative) > 200 else case.narrative
            })
        
        return results
    
    def get_pattern_insights(self, fraud_pattern: str) -> Dict:
        """Get insights about a fraud pattern from past cases."""
        if fraud_pattern not in self.statistics["patterns"]:
            return {"pattern": fraud_pattern, "cases_seen": 0}
        
        pattern_stats = self.statistics["patterns"][fraud_pattern]
        confirmed_rate = (
            pattern_stats["confirmed"] / pattern_stats["count"]
            if pattern_stats["count"] > 0 else 0
        )
        
        # Get all cases of this pattern
        matching_cases = self.vector_store.find_by_fraud_pattern(fraud_pattern, top_k=10)
        
        actions_taken = {}
        for case, _ in matching_cases:
            action = case.action_recommended
            if action not in actions_taken:
                actions_taken[action] = 0
            actions_taken[action] += 1
        
        return {
            "pattern": fraud_pattern,
            "total_cases_seen": pattern_stats["count"],
            "confirmed_fraud_cases": pattern_stats["confirmed"],
            "confirmation_rate": round(confirmed_rate, 2),
            "common_actions": actions_taken,
            "recent_cases": [c.case_id for c, _ in matching_cases[:3]]
        }
    
    def get_statistics(self) -> Dict:
        """Get overall memory statistics."""
        if self.statistics["total_cases"] > 0:
            accuracy = (
                self.statistics["confirmed_fraud"] + 
                (self.statistics["total_cases"] - self.statistics["confirmed_fraud"] - self.statistics["false_positives"])
            ) / self.statistics["total_cases"]
            self.statistics["avg_accuracy"] = round(accuracy, 2)
        
        return self.statistics


def test_case_memory():
    """Test case memory system."""
    print("\n" + "="*70)
    print("CASE MEMORY SYSTEM TEST")
    print("="*70 + "\n")
    
    manager = CaseMemoryManager()
    
    # Add some sample cases
    cases = [
        {
            "case_id": "CASE_HIST_001",
            "customer_id": "C001",
            "fraud_pattern": "ACCOUNT_TAKEOVER",
            "initial_risk": 0.85,
            "final_risk": 0.92,
            "confidence": 0.95,
            "evidence": ["SHARED_DEVICE", "SHARED_IP", "VELOCITY_ANOMALY"],
            "action": "BLOCK_ACCOUNT",
            "outcome": "CONFIRMED_FRAUD",
            "narrative": "New device with high velocity activity confirmed as account takeover"
        },
        {
            "case_id": "CASE_HIST_002",
            "customer_id": "C002",
            "fraud_pattern": "ACCOUNT_TAKEOVER",
            "initial_risk": 0.80,
            "final_risk": 0.88,
            "confidence": 0.90,
            "evidence": ["SHARED_IP", "VELOCITY_ANOMALY"],
            "action": "HOLD_TRANSACTION",
            "outcome": "CONFIRMED_FRAUD",
            "narrative": "Similar pattern: shared IP and high velocity, confirmed fraud"
        },
        {
            "case_id": "CASE_HIST_003",
            "customer_id": "C003",
            "fraud_pattern": "PAYMENT_FRAUD",
            "initial_risk": 0.70,
            "final_risk": 0.65,
            "confidence": 0.75,
            "evidence": ["NETWORK_ANALYSIS", "BEHAVIORAL_ANOMALY"],
            "action": "HOLD_TRANSACTION",
            "outcome": "FALSE_POSITIVE",
            "narrative": "Transaction seemed suspicious but customer confirmed legitimacy"
        },
    ]
    
    print("📝 Storing historical cases...")
    for case in cases:
        manager.store_case(
            case_id=case["case_id"],
            customer_id=case["customer_id"],
            fraud_pattern=case["fraud_pattern"],
            initial_risk=case["initial_risk"],
            final_risk=case["final_risk"],
            confidence=case["confidence"],
            evidence_types=case["evidence"],
            action=case["action"],
            outcome=case["outcome"],
            approval_required=True,
            approved_by="ANALYST_01",
            investigation_duration_hours=2,
            narrative=case["narrative"]
        )
    
    print(f"✓ Stored {len(cases)} cases\n")
    
    # Test retrieval
    print("🔍 Retrieving similar cases...")
    similar = manager.retrieve_similar_cases(
        fraud_pattern="ACCOUNT_TAKEOVER",
        initial_risk=0.82,
        confidence=0.85,
        top_k=3
    )
    
    print(f"Found {len(similar)} similar cases to ACCOUNT_TAKEOVER:\n")
    for case in similar:
        print(f"  Case: {case['case_id']}")
        print(f"    Pattern: {case['fraud_pattern']}")
        print(f"    Risk: {case['initial_risk']:.2f} → {case['final_risk']:.2f}")
        print(f"    Action: {case['action_recommended']}")
        print(f"    Outcome: {case['action_outcome']}")
        print(f"    Similarity: {case['similarity']}")
        print()
    
    # Get insights
    print("📊 Pattern Insights for ACCOUNT_TAKEOVER:")
    insights = manager.get_pattern_insights("ACCOUNT_TAKEOVER")
    print(f"  Total cases: {insights['total_cases_seen']}")
    print(f"  Confirmed fraud: {insights['confirmed_fraud_cases']}")
    print(f"  Confirmation rate: {insights['confirmation_rate']}")
    print(f"  Common actions: {insights['common_actions']}\n")
    
    # Get statistics
    print("📈 Overall Statistics:")
    stats = manager.get_statistics()
    print(f"  Total cases: {stats['total_cases']}")
    print(f"  Confirmed fraud: {stats['confirmed_fraud']}")
    print(f"  False positives: {stats['false_positives']}")
    print(f"  Average accuracy: {stats['avg_accuracy']}")
    print(f"  Patterns: {list(stats['patterns'].keys())}\n")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    test_case_memory()
