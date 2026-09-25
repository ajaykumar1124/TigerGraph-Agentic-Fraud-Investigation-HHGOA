"""
Investigation Agent Testing
Test 6-phase workflow
"""

import logging
import sys
from backend.agents.investigation_agent import create_investigation_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_investigation_agent():
    """Test investigation agent workflow"""
    logger.info("=" * 70)
    logger.info("HHGOA_IEEE Investigation Agent Testing - Phase 4")
    logger.info("=" * 70)

    try:
        # Step 1: Create agent
        logger.info("\n[Step 1] Creating investigation agent...")
        agent = create_investigation_agent()
        logger.info("✓ Agent created")

        # Step 2: Build graph
        logger.info("\n[Step 2] Building LangGraph workflow...")
        graph = agent.build_graph()
        logger.info("✓ Graph compiled (6 phases)")

        # Step 3: Run investigation
        logger.info("\n[Step 3] Running investigation workflow...")
        result = agent.invoke(
            case_id="test_case_001",
            user_id="1",
            transaction_id="txn_001",
            initiator="test_system",
            risk_indicators=["velocity_attack", "new_device", "high_amount"],
            initial_risk_level="HIGH",
        )

        # Step 4: Display results
        logger.info("\n[Step 4] Investigation Results:")
        logger.info("=" * 70)

        if "error" in result:
            logger.error(f"Investigation failed: {result['error']}")
            return False

        logger.info(f"Case ID: {result.get('case_id')}")
        logger.info(f"Status: {result.get('case_status')}")
        logger.info(f"Recommended Action: {result.get('recommended_action')}")
        logger.info(f"Confidence: {result.get('action_confidence'):.2f}")
        logger.info(f"Uncertainty: {result.get('uncertainty_score'):.2f}")
        logger.info(f"Execution Time: {result.get('execution_time_ms'):.0f}ms")
        
        logger.info(f"\nEvidence Summary: {result.get('evidence_summary')}")
        logger.info(f"Policy Violations: {', '.join(result.get('policy_violations', [])) or 'None'}")
        logger.info(f"Patterns Matched: {len(result.get('patterns_matched', []))}")
        
        logger.info(f"\nReasoning:\n{result.get('reasoning', 'N/A')}")
        
        if result.get("errors"):
            logger.info(f"\nErrors encountered: {', '.join(result['errors'])}")

        logger.info("\n" + "=" * 70)
        logger.info("✓ Investigation workflow testing complete")
        logger.info("=" * 70)

        return True

    except Exception as e:
        logger.error(f"\n✗ Testing failed: {str(e)}")
        logger.exception("Full traceback:")
        return False


if __name__ == "__main__":
    success = test_investigation_agent()
    sys.exit(0 if success else 1)
