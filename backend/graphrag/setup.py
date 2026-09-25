"""
GraphRAG Setup - Build and test vector index
"""

import logging
import sys
from backend.graphrag.indexer import GraphRAGIndexer, get_indexer
from backend.graphrag.retriever import GraphRAGRetriever

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main setup workflow"""
    logger.info("=" * 70)
    logger.info("HHGOA_IEEE GraphRAG Setup - Phase 2")
    logger.info("=" * 70)

    try:
        # Step 1: Build index
        logger.info("\n[Step 1] Building GraphRAG index...")
        indexer = GraphRAGIndexer()
        stats = indexer.get_stats()

        logger.info(f"✓ Index built:")
        logger.info(f"  Documents: {stats['total_documents']}")
        logger.info(f"  Vectors: {stats['vector_count']}")
        logger.info(f"  Dimension: {stats['vector_dimension']}")
        logger.info(f"  Model: {stats['embedding_model']}")

        # Step 2: Test retriever
        logger.info("\n[Step 2] Testing GraphRAG retriever...")
        retriever = GraphRAGRetriever(indexer)

        # Test queries
        test_queries = [
            "velocity attack high frequency transactions",
            "device fingerprint mismatch",
            "geographic anomaly new country",
            "high risk merchant gambling",
            "amount threshold violation daily limit",
        ]

        for query in test_queries:
            logger.info(f"\n  Query: {query}")
            results = retriever.retrieve_evidence_by_query(query, top_k=3)

            for i, doc in enumerate(results, 1):
                logger.info(f"    [{i}] {doc.get('title')} (similarity: {doc.get('similarity_score', 0):.3f})")

        # Step 3: Test case context retrieval
        logger.info("\n[Step 3] Testing case context retrieval...")

        case_context = {
            "user_id": "user_001",
            "card_id": "card_001",
            "transaction_id": "txn_001",
            "merchant": "Online_Casino",
            "amount": 5000,
            "indicators": ["high_amount", "high_risk_merchant", "velocity_attack", "new_device"],
        }

        evidence = retriever.retrieve_evidence("case_001", case_context, top_k=5)

        logger.info(f"✓ Evidence retrieved:")
        logger.info(f"  Policies: {len(evidence['policies'])}")
        logger.info(f"  Patterns: {len(evidence['patterns'])}")
        logger.info(f"  Related Cases: {len(evidence['related_cases'])}")

        # Step 4: Test policy checks
        logger.info("\n[Step 4] Testing policy checks...")

        policy_results = retriever.get_policy_check_results(case_context)

        logger.info(f"✓ Policy checks:")
        logger.info(f"  Policies Checked: {policy_results['policies_checked']}")
        logger.info(f"  Policies Triggered: {len(policy_results['policies_triggered'])}")
        logger.info(f"  Policies Passed: {len(policy_results['policies_passed'])}")

        for triggered in policy_results["policies_triggered"]:
            logger.info(f"    - {triggered['policy_name']}")

        logger.info("\n" + "=" * 70)
        logger.info("✓ Phase 2 Complete: GraphRAG ready for agent integration")
        logger.info("=" * 70)
        logger.info("\nNext: Phase 3 - TigerGraph MCP Setup")

        return True

    except Exception as e:
        logger.error(f"\n✗ Setup failed: {str(e)}")
        logger.exception("Full traceback:")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
