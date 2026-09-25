"""
GraphRAG Indexer - Build vector embeddings for semantic search
Uses FAISS + Sentence Transformers for efficient similarity search
"""

import logging
import json
import pickle
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import numpy as np
from datetime import datetime

from sentence_transformers import SentenceTransformer
import faiss

from backend.config import settings

logger = logging.getLogger(__name__)


class GraphRAGIndexer:
    """
    GraphRAG vector indexer
    - Loads fraud policies, patterns, case findings
    - Creates embeddings using sentence transformers
    - Stores in FAISS for similarity search
    """

    def __init__(self, config=None):
        """Initialize indexer"""
        self.config = config or settings.graphrag
        self.embedding_model = SentenceTransformer(self.config.embedding_model)
        self.index: Optional[faiss.IndexFlatL2] = None
        self.documents: List[Dict[str, Any]] = []
        self.metadata: List[Dict[str, Any]] = []
        self.index_path = Path("backend/graphrag/index")
        self.index_path.mkdir(parents=True, exist_ok=True)
        self._load_or_build()

    def _load_or_build(self):
        """Load existing index or build new one"""
        if self._index_exists():
            logger.info("Loading existing GraphRAG index...")
            self._load_index()
        else:
            logger.info("Building new GraphRAG index...")
            self._build_index()

    def _index_exists(self) -> bool:
        """Check if index files exist"""
        index_file = self.index_path / "faiss.index"
        docs_file = self.index_path / "documents.pkl"
        return index_file.exists() and docs_file.exists()

    def _build_index(self):
        """Build vector index from scratch"""
        try:
            # Load all documents
            self._load_documents()

            if not self.documents:
                logger.warning("No documents loaded for indexing")
                self._create_empty_index()
                return

            # Create embeddings
            logger.info(f"Creating embeddings for {len(self.documents)} documents...")
            embeddings = self._create_embeddings()

            # Create FAISS index
            logger.info(f"Creating FAISS index with {len(embeddings)} vectors...")
            self.index = faiss.IndexFlatL2(self.config.vector_dim)
            self.index.add(embeddings.astype(np.float32))

            # Save index
            self._save_index()
            logger.info(f"✓ Index built with {self.index.ntotal} vectors")

        except Exception as e:
            logger.error(f"✗ Failed to build index: {str(e)}")
            raise

    def _load_documents(self):
        """Load documents from multiple sources"""
        data_dir = Path(settings.data.data_dir)

        # Load policies
        self._load_policies(data_dir)

        # Load fraud patterns
        self._load_patterns(data_dir)

        # Load closed case summaries
        self._load_case_summaries(data_dir)

        # Load default evidence templates
        self._load_evidence_templates()

        logger.info(f"Loaded {len(self.documents)} documents for indexing")

    def _load_policies(self, data_dir: Path):
        """Load fraud policies"""
        logger.info("Loading fraud policies...")
        policies_file = data_dir / settings.data.policies_file

        default_policies = [
            {
                "id": "policy_1",
                "type": "policy",
                "name": "High Risk Merchant Detection",
                "text": "Flag and review transactions with high-risk merchant categories (online gambling, digital goods, money transfers)",
                "category": "merchant",
            },
            {
                "id": "policy_2",
                "type": "policy",
                "name": "Velocity Check Rule",
                "text": "Alert if user makes more than 5 transactions within 1 hour from different geographic locations",
                "category": "velocity",
            },
            {
                "id": "policy_3",
                "type": "policy",
                "name": "Geographic Anomaly Detection",
                "text": "Flag transactions from countries not in user's transaction history, especially high-fraud countries",
                "category": "location",
            },
            {
                "id": "policy_4",
                "type": "policy",
                "name": "Device Fingerprint Mismatch",
                "text": "Alert when device characteristics change (new browser, OS, or unusual device combination)",
                "category": "device",
            },
            {
                "id": "policy_5",
                "type": "policy",
                "name": "Amount Threshold Violation",
                "text": "Block if transaction amount exceeds user's typical daily spending or account-specific limits",
                "category": "amount",
            },
            {
                "id": "policy_6",
                "type": "policy",
                "name": "KYC Incomplete Check",
                "text": "Require additional verification if user's KYC profile is incomplete or has been updated recently",
                "category": "kyc",
            },
        ]

        policies = default_policies
        if policies_file.exists():
            try:
                with open(policies_file) as f:
                    content = f.read()
                    # Try to parse as JSON
                    try:
                        policies = json.loads(content)
                    except:
                        # If not JSON, treat as markdown and create documents
                        policies = [
                            {"id": "policy_custom", "type": "policy", "text": content, "name": "Custom Policies"}
                        ]
            except Exception as e:
                logger.warning(f"Could not load policies file: {str(e)}")

        for policy in policies:
            doc = {
                "id": policy.get("id", f"policy_{len(self.documents)}"),
                "type": "policy",
                "title": policy.get("name", "Unknown Policy"),
                "content": policy.get("text", ""),
                "category": policy.get("category", "general"),
                "source": "fraud_policies",
            }
            self.documents.append(doc)

        logger.info(f"  Loaded {len(policies)} policies")

    def _load_patterns(self, data_dir: Path):
        """Load fraud patterns"""
        logger.info("Loading fraud patterns...")
        patterns_file = data_dir / settings.data.patterns_file

        default_patterns = [
            {
                "id": "pattern_1",
                "name": "Velocity Attack",
                "description": "Multiple small transactions in rapid succession to test card validity or build trust",
                "indicators": ["high_frequency", "low_amount", "short_timespan"],
                "risk": "HIGH",
            },
            {
                "id": "pattern_2",
                "name": "Card Testing",
                "description": "Series of small purchases to validate stolen card before large transactions",
                "indicators": ["escalating_amount", "new_card", "unusual_merchant"],
                "risk": "HIGH",
            },
            {
                "id": "pattern_3",
                "name": "Geographic Impossibility",
                "description": "Transactions from geographically impossible locations within short timeframe",
                "indicators": ["location_jump", "high_speed", "country_mismatch"],
                "risk": "CRITICAL",
            },
            {
                "id": "pattern_4",
                "name": "Account Takeover",
                "description": "Sudden behavioral change: new devices, locations, merchants, unusual amounts",
                "indicators": ["device_change", "location_change", "behavior_change"],
                "risk": "HIGH",
            },
            {
                "id": "pattern_5",
                "name": "Synthetic Identity Fraud",
                "description": "New account with rapid transaction activity and unusual patterns",
                "indicators": ["new_account", "high_velocity", "risky_behavior"],
                "risk": "MEDIUM",
            },
        ]

        patterns = default_patterns
        if patterns_file.exists():
            try:
                with open(patterns_file) as f:
                    patterns = json.load(f)
            except Exception as e:
                logger.warning(f"Could not load patterns file: {str(e)}")

        for pattern in patterns:
            doc = {
                "id": pattern.get("id", f"pattern_{len(self.documents)}"),
                "type": "fraud_pattern",
                "title": pattern.get("name", "Unknown Pattern"),
                "content": pattern.get("description", ""),
                "indicators": pattern.get("indicators", []),
                "risk_level": pattern.get("risk", "MEDIUM"),
                "source": "fraud_patterns",
            }
            self.documents.append(doc)

        logger.info(f"  Loaded {len(patterns)} patterns")

    def _load_case_summaries(self, data_dir: Path):
        """Load historical case summaries"""
        logger.info("Loading case summaries...")
        cases_file = data_dir / settings.data.closed_cases_file

        default_cases = [
            {
                "id": "case_summary_1",
                "case_id": "CASE_001",
                "outcome": "FRAUD_CONFIRMED",
                "summary": "User account was compromised through phishing. Multiple transactions from new device in different country.",
                "patterns_matched": ["account_takeover", "geographic_anomaly"],
            },
            {
                "id": "case_summary_2",
                "case_id": "CASE_002",
                "outcome": "LEGITIMATE",
                "summary": "User made unusual purchases during vacation. Confirmed via phone verification.",
                "patterns_matched": ["geographic_anomaly"],
            },
            {
                "id": "case_summary_3",
                "case_id": "CASE_003",
                "outcome": "FRAUD_CONFIRMED",
                "summary": "Card testing pattern detected. Series of small transactions followed by large purchase attempt.",
                "patterns_matched": ["card_testing", "velocity_attack"],
            },
        ]

        cases = default_cases
        if cases_file.exists():
            try:
                import pandas as pd

                df = pd.read_csv(cases_file)
                cases = []
                for idx, row in df.iterrows():
                    cases.append(
                        {
                            "id": f"case_{idx}",
                            "case_id": str(row.get("CaseID", idx)),
                            "outcome": row.get("Outcome", "UNKNOWN"),
                            "summary": row.get("Summary", ""),
                            "patterns_matched": str(row.get("Patterns", "[]")).split(","),
                        }
                    )
            except Exception as e:
                logger.warning(f"Could not load cases file: {str(e)}")

        for case in cases:
            doc = {
                "id": case.get("id", f"case_{len(self.documents)}"),
                "type": "case_summary",
                "title": f"Case {case.get('case_id')}",
                "content": case.get("summary", ""),
                "outcome": case.get("outcome", "UNKNOWN"),
                "patterns": case.get("patterns_matched", []),
                "source": "closed_cases",
            }
            self.documents.append(doc)

        logger.info(f"  Loaded {len(cases)} case summaries")

    def _load_evidence_templates(self):
        """Load evidence templates for common evidence types"""
        logger.info("Loading evidence templates...")

        templates = [
            {
                "id": "evidence_template_1",
                "type": "evidence_template",
                "title": "Transaction Amount Anomaly",
                "content": "Transaction amount significantly exceeds user's average or daily limit",
                "category": "amount_anomaly",
            },
            {
                "id": "evidence_template_2",
                "type": "evidence_template",
                "title": "Merchant Category Risk",
                "content": "Merchant MCC code indicates high-risk category (gambling, money transfer, etc.)",
                "category": "merchant_risk",
            },
            {
                "id": "evidence_template_3",
                "type": "evidence_template",
                "title": "Device Fingerprint Mismatch",
                "content": "Device fingerprint differs from user's known devices",
                "category": "device_anomaly",
            },
            {
                "id": "evidence_template_4",
                "type": "evidence_template",
                "title": "Geographic Anomaly",
                "content": "Transaction location differs from user's historical patterns",
                "category": "location_anomaly",
            },
            {
                "id": "evidence_template_5",
                "type": "evidence_template",
                "title": "IP Address Risk",
                "content": "IP address associated with VPN, proxy, or datacenter",
                "category": "ip_risk",
            },
            {
                "id": "evidence_template_6",
                "type": "evidence_template",
                "title": "Velocity Attack Pattern",
                "content": "Multiple transactions detected within short timeframe",
                "category": "velocity_attack",
            },
        ]

        for template in templates:
            doc = {
                "id": template.get("id"),
                "type": "evidence_template",
                "title": template.get("title"),
                "content": template.get("content"),
                "category": template.get("category"),
                "source": "templates",
            }
            self.documents.append(doc)

        logger.info(f"  Loaded {len(templates)} evidence templates")

    def _create_embeddings(self) -> np.ndarray:
        """Create embeddings for all documents"""
        texts = [doc.get("content", doc.get("title", "")) for doc in self.documents]
        embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
        return embeddings

    def _save_index(self):
        """Save index to disk"""
        try:
            faiss.write_index(self.index, str(self.index_path / "faiss.index"))

            with open(self.index_path / "documents.pkl", "wb") as f:
                pickle.dump(self.documents, f)

            with open(self.index_path / "metadata.json", "w") as f:
                json.dump(
                    {
                        "document_count": len(self.documents),
                        "vector_dim": self.config.vector_dim,
                        "embedding_model": self.config.embedding_model,
                        "created_at": datetime.now().isoformat(),
                    },
                    f,
                    indent=2,
                )

            logger.info(f"✓ Index saved to {self.index_path}")
        except Exception as e:
            logger.error(f"✗ Failed to save index: {str(e)}")
            raise

    def _load_index(self):
        """Load index from disk"""
        try:
            self.index = faiss.read_index(str(self.index_path / "faiss.index"))

            with open(self.index_path / "documents.pkl", "rb") as f:
                self.documents = pickle.load(f)

            logger.info(f"✓ Index loaded: {self.index.ntotal} vectors, {len(self.documents)} documents")
        except Exception as e:
            logger.error(f"✗ Failed to load index: {str(e)}")
            raise

    def _create_empty_index(self):
        """Create empty index"""
        logger.warning("Creating empty index (no documents)")
        self.index = faiss.IndexFlatL2(self.config.vector_dim)
        self.documents = []

    def search(
        self, query: str, top_k: int = None, similarity_threshold: float = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            query: Query text
            top_k: Number of results (default: MAX_RESULTS)
            similarity_threshold: Minimum similarity (default: SIMILARITY_THRESHOLD)
        
        Returns:
            List of matching documents with scores
        """
        if not self.index or not self.documents:
            logger.warning("Index is empty")
            return []

        top_k = top_k or self.config.max_results
        similarity_threshold = similarity_threshold or self.config.similarity_threshold

        try:
            # Create embedding for query
            query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)

            # Search FAISS index
            distances, indices = self.index.search(query_embedding.astype(np.float32), top_k)

            # Convert distances to similarity scores (1 / (1 + distance))
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx >= 0 and idx < len(self.documents):
                    # FAISS returns L2 distances; convert to similarity
                    similarity = 1.0 / (1.0 + distance)

                    if similarity >= similarity_threshold:
                        doc = self.documents[idx].copy()
                        doc["similarity_score"] = float(similarity)
                        doc["rank"] = i + 1
                        results.append(doc)

            logger.debug(f"Found {len(results)} similar documents for query: {query[:50]}")
            return results

        except Exception as e:
            logger.error(f"✗ Search failed: {str(e)}")
            raise

    def add_document(self, document: Dict[str, Any]):
        """Add new document to index"""
        try:
            self.documents.append(document)

            # Create embedding
            text = document.get("content", document.get("title", ""))
            embedding = self.embedding_model.encode([text], convert_to_numpy=True)

            # Add to index
            self.index.add(embedding.astype(np.float32))

            logger.debug(f"Added document: {document.get('id')}")
        except Exception as e:
            logger.error(f"✗ Failed to add document: {str(e)}")
            raise

    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        return {
            "total_documents": len(self.documents),
            "vector_count": self.index.ntotal if self.index else 0,
            "vector_dimension": self.config.vector_dim,
            "embedding_model": self.config.embedding_model,
            "index_path": str(self.index_path),
        }


# Singleton instance
_indexer: Optional[GraphRAGIndexer] = None


def get_indexer() -> GraphRAGIndexer:
    """Get or create indexer"""
    global _indexer
    if _indexer is None:
        _indexer = GraphRAGIndexer()
    return _indexer
