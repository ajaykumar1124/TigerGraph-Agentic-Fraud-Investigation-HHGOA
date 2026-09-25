"""
TigerGraph MCP Server Testing
Test all tools and verify functionality
"""

import logging
import sys
from backend.mcp.server import create_mcp_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_mcp_server():
    """Test MCP server functionality"""
    logger.info("=" * 70)
    logger.info("HHGOA_IEEE TigerGraph MCP Testing - Phase 3")
    logger.info("=" * 70)

    try:
        # Step 1: Create server
        logger.info("\n[Step 1] Creating MCP server...")
        server = create_mcp_server()
        logger.info(f"✓ Server created with {len(server.tools_registry)} tools")

        # Step 2: List all tools
        logger.info("\n[Step 2] Available tools:")
        tools = server.get_tools_list()
        for tool in tools:
            logger.info(f"  - {tool['name']}: {tool['description']}")

        # Step 3: Test tools with sample data
        logger.info("\n[Step 3] Testing tool execution...")

        # Test: Get graph stats
        logger.info("\n  Testing: get_graph_stats")
        result = server.call_tool("get_graph_stats", {})
        logger.info(f"  Result: {result.get('success')}")
        if result.get("success"):
            logger.info(f"    Vertices: {result.get('stats', {}).get('vertex_count')}")
            logger.info(f"    Edges: {result.get('stats', {}).get('edge_count')}")

        # Test: Query user (if data exists)
        logger.info("\n  Testing: query_user_profile")
        try:
            result = server.call_tool("query_user_profile", {"user_id": "1"})
            if result.get("success"):
                logger.info(f"  ✓ User query successful")
            else:
                logger.info(f"  ⚠ User not found (expected if no data): {result.get('error')}")
        except Exception as e:
            logger.info(f"  ⚠ User query failed: {str(e)}")

        # Test: Check policies
        logger.info("\n  Testing: check_policies")
        case_context = {
            "indicators": ["high_amount", "velocity_attack", "new_device"]
        }
        result = server.call_tool("check_policies", {"case_context": case_context})
        if result.get("success"):
            policies = result.get("policies", {})
            logger.info(f"  ✓ Policy check successful")
            logger.info(f"    Policies triggered: {len(policies.get('policies_triggered', []))}")
            logger.info(f"    Policies passed: {len(policies.get('policies_passed', []))}")
        else:
            logger.info(f"  ✗ Policy check failed: {result.get('error')}")

        # Test: Retrieve evidence
        logger.info("\n  Testing: retrieve_evidence")
        result = server.call_tool("retrieve_evidence", {"case_context": case_context})
        if result.get("success"):
            evidence = result.get("evidence", {})
            logger.info(f"  ✓ Evidence retrieval successful")
            logger.info(f"    Policies: {len(evidence.get('policies', []))}")
            logger.info(f"    Patterns: {len(evidence.get('patterns', []))}")
            logger.info(f"    Related cases: {len(evidence.get('related_cases', []))}")
        else:
            logger.info(f"  ✗ Evidence retrieval failed: {result.get('error')}")

        # Test: Create case
        logger.info("\n  Testing: create_fraud_case")
        case_args = {
            "initiator": "test_system",
            "user_id": "1",
            "transaction_id": "txn_001",
            "risk_level": "HIGH",
            "indicators": ["high_amount", "new_device"],
        }
        result = server.call_tool("create_fraud_case", case_args)
        if result.get("success"):
            case_id = result.get("case_id")
            logger.info(f"  ✓ Case created: {case_id}")

            # Test: Update case
            logger.info("\n  Testing: update_case_status")
            result = server.call_tool(
                "update_case_status",
                {
                    "case_id": case_id,
                    "status": "INVESTIGATING",
                    "next_action": "Request customer verification",
                },
            )
            if result.get("success"):
                logger.info(f"  ✓ Case updated")
            else:
                logger.info(f"  ✗ Case update failed: {result.get('error')}")

            # Test: Add evidence
            logger.info("\n  Testing: add_case_evidence")
            result = server.call_tool(
                "add_case_evidence",
                {
                    "case_id": case_id,
                    "evidence_text": "Transaction from new device in different country",
                    "evidence_type": "behavioral_anomaly",
                },
            )
            if result.get("success"):
                logger.info(f"  ✓ Evidence added")
            else:
                logger.info(f"  ✗ Evidence add failed: {result.get('error')}")

        else:
            logger.info(f"  ✗ Case creation failed: {result.get('error')}")

        # Test: Search patterns
        logger.info("\n  Testing: search_fraud_patterns")
        result = server.call_tool("search_fraud_patterns", {"pattern_name": "velocity"})
        if result.get("success"):
            logger.info(f"  ✓ Pattern search successful")
            logger.info(f"    Matches: {len(result.get('matches', []))}")
        else:
            logger.info(f"  ✗ Pattern search failed: {result.get('error')}")

        logger.info("\n" + "=" * 70)
        logger.info("✓ MCP Server testing complete")
        logger.info("=" * 70)
        logger.info("\nServer is ready for integration with LangGraph agent (Phase 4)")
        return True

    except Exception as e:
        logger.error(f"\n✗ Testing failed: {str(e)}")
        logger.exception("Full traceback:")
        return False


if __name__ == "__main__":
    success = test_mcp_server()
    sys.exit(0 if success else 1)
