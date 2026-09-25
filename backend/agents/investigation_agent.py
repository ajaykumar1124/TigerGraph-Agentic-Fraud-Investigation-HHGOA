"""
Investigation Agent - 6-Phase Fraud Investigation Workflow
Orchestrates query, evidence, uncertainty, action, and recording phases
"""

import logging
import time
from typing import Any, Dict, List
from datetime import datetime

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

from backend.agents.investigation_state import InvestigationState, create_initial_state
from backend.mcp.server import get_mcp_server
from backend.config import settings

logger = logging.getLogger(__name__)


class InvestigationAgent:
    """6-phase fraud investigation agent using LangGraph"""

    def __init__(self):
        """Initialize agent"""
        self.mcp = get_mcp_server()
        self.llm = ChatOpenAI(
            model=settings.llm.model,
            temperature=settings.llm.temperature,
            api_key=settings.llm.api_key,
        )
        self.graph = None

    def build_graph(self) -> StateGraph:
        """Build LangGraph workflow"""
        workflow = StateGraph(InvestigationState)

        # Add nodes (phases)
        workflow.add_node("phase_1_query_graph", self._phase_1_query_graph)
        workflow.add_node("phase_2_get_evidence", self._phase_2_get_evidence)
        workflow.add_node("phase_3_assess_uncertainty", self._phase_3_assess_uncertainty)
        workflow.add_node("phase_4_request_evidence", self._phase_4_request_evidence)
        workflow.add_node("phase_5_recommend_action", self._phase_5_recommend_action)
        workflow.add_node("phase_6_record_case", self._phase_6_record_case)

        # Add edges (transitions)
        workflow.add_edge(START, "phase_1_query_graph")
        workflow.add_edge("phase_1_query_graph", "phase_2_get_evidence")
        workflow.add_edge("phase_2_get_evidence", "phase_3_assess_uncertainty")

        # Conditional: if uncertain, request evidence; otherwise recommend action
        workflow.add_conditional_edges(
            "phase_3_assess_uncertainty",
            self._should_request_evidence,
            {
                True: "phase_4_request_evidence",
                False: "phase_5_recommend_action",
            },
        )

        # Evidence phase loops or goes to recommendation
        workflow.add_conditional_edges(
            "phase_4_request_evidence",
            self._evidence_complete,
            {
                True: "phase_5_recommend_action",
                False: "phase_3_assess_uncertainty",
            },
        )

        workflow.add_edge("phase_5_recommend_action", "phase_6_record_case")
        workflow.add_edge("phase_6_record_case", END)

        self.graph = workflow.compile()
        logger.info("✓ Investigation graph compiled (6 phases)")
        return self.graph

    def _phase_1_query_graph(self, state: InvestigationState) -> InvestigationState:
        """Phase 1: Query TigerGraph for entity relationships"""
        logger.info(f"[Phase 1] Querying graph for case {state['case_id']}")
        state["phase"] = 1

        try:
            # Query user profile
            user_result = self.mcp.call_tool("query_user_profile", {"user_id": state["user_id"]})
            if user_result.get("success"):
                state["user_profile"] = user_result.get("profile")
                state["user_risk_score"] = float(user_result.get("profile", {}).get("risk_score", 0.0))

            # Query transaction details
            txn_result = self.mcp.call_tool(
                "query_transaction_details", {"transaction_id": state["transaction_id"]}
            )
            if txn_result.get("success"):
                state["transaction_details"] = txn_result.get("transaction")

            # Query merchant
            if state["transaction_details"]:
                merchant_id = state["transaction_details"].get("merchant_id", "unknown")
                merchant_result = self.mcp.call_tool(
                    "query_merchant_profile", {"merchant_id": str(merchant_id)}
                )
                if merchant_result.get("success"):
                    state["merchant_profile"] = merchant_result.get("merchant")

            state["case_notes"] += f"\n[Phase 1] Graph query complete. User risk: {state['user_risk_score']:.2f}"
            logger.info("✓ Phase 1 complete: Graph entities queried")

        except Exception as e:
            logger.error(f"✗ Phase 1 failed: {str(e)}")
            state["errors"].append(f"Phase 1: {str(e)}")

        return state

    def _phase_2_get_evidence(self, state: InvestigationState) -> InvestigationState:
        """Phase 2: Retrieve evidence using GraphRAG"""
        logger.info(f"[Phase 2] Retrieving evidence for case {state['case_id']}")
        state["phase"] = 2

        try:
            case_context = {
                "user_id": state["user_id"],
                "indicators": state["risk_indicators"],
                "merchant": state.get("merchant_profile", {}).get("merchant_name", "unknown"),
                "amount": state.get("transaction_details", {}).get("amount", 0),
            }

            # Retrieve evidence
            evidence_result = self.mcp.call_tool("retrieve_evidence", {"case_context": case_context})
            if evidence_result.get("success"):
                state["retrieved_evidence"] = evidence_result.get("evidence")
                evidence = evidence_result.get("evidence", {})
                state["policies_triggered"] = evidence.get("policies", [])
                state["patterns_matched"] = evidence.get("patterns", [])
                state["related_cases"] = evidence.get("related_cases", [])

                # Generate summary
                state["evidence_summary"] = (
                    f"Policies: {len(state['policies_triggered'])}, "
                    f"Patterns: {len(state['patterns_matched'])}, "
                    f"Related cases: {len(state['related_cases'])}"
                )

            # Check policies
            policy_result = self.mcp.call_tool("check_policies", {"case_context": case_context})
            if policy_result.get("success"):
                policies = policy_result.get("policies", {})
                triggered = policies.get("policies_triggered", [])
                state["policy_violations"] = [p["policy_name"] for p in triggered]

            state["case_notes"] += f"\n[Phase 2] Evidence retrieved: {state['evidence_summary']}"
            logger.info("✓ Phase 2 complete: Evidence retrieved")

        except Exception as e:
            logger.error(f"✗ Phase 2 failed: {str(e)}")
            state["errors"].append(f"Phase 2: {str(e)}")

        return state

    def _phase_3_assess_uncertainty(self, state: InvestigationState) -> InvestigationState:
        """Phase 3: Assess confidence and uncertainty"""
        logger.info(f"[Phase 3] Assessing uncertainty for case {state['case_id']}")
        state["phase"] = 3

        try:
            # Calculate confidence based on evidence
            evidence_count = len(state["patterns_matched"]) + len(state["policies_triggered"])
            user_risk = state["user_risk_score"]
            indicator_count = len(state["risk_indicators"])

            # Confidence formula
            confidence = min(1.0, (evidence_count * 0.3 + user_risk * 0.4 + indicator_count * 0.3) / 10.0)
            state["confidence_score"] = confidence
            state["uncertainty_score"] = 1.0 - confidence

            # Determine if additional evidence needed
            state["needs_additional_evidence"] = confidence < settings.agent.uncertainty_threshold
            state["uncertainty_reason"] = (
                f"Confidence: {confidence:.2f}, Evidence: {evidence_count}, "
                f"Indicators: {indicator_count}"
            )

            state["case_notes"] += (
                f"\n[Phase 3] Confidence: {confidence:.2f}, "
                f"Needs evidence: {state['needs_additional_evidence']}"
            )
            logger.info(
                f"✓ Phase 3 complete: Confidence {confidence:.2f}, "
                f"Uncertain: {state['needs_additional_evidence']}"
            )

        except Exception as e:
            logger.error(f"✗ Phase 3 failed: {str(e)}")
            state["errors"].append(f"Phase 3: {str(e)}")

        return state

    def _phase_4_request_evidence(self, state: InvestigationState) -> InvestigationState:
        """Phase 4: Request additional evidence if uncertain"""
        logger.info(f"[Phase 4] Requesting additional evidence for case {state['case_id']}")
        state["phase"] = 4

        try:
            # Generate evidence request using LLM
            prompt = f"""
Based on this fraud investigation:
- User ID: {state['user_id']}
- Risk Indicators: {', '.join(state['risk_indicators'])}
- Current Confidence: {state['confidence_score']:.2f}
- Uncertainty Reason: {state['uncertainty_reason']}

What additional evidence should we request to confirm or refute fraud?
Keep it concise (1-2 sentences).
"""

            message = self.llm.invoke(prompt)
            state["evidence_request"] = message.content

            # Simulate customer response
            state["customer_response"] = "Customer confirmed legitimate travel"
            state["additional_evidence_requested"] = True

            state["case_notes"] += f"\n[Phase 4] Evidence requested: {state['evidence_request']}"
            logger.info("✓ Phase 4 complete: Additional evidence requested")

        except Exception as e:
            logger.error(f"✗ Phase 4 failed: {str(e)}")
            state["errors"].append(f"Phase 4: {str(e)}")

        return state

    def _phase_5_recommend_action(self, state: InvestigationState) -> InvestigationState:
        """Phase 5: Recommend next-best action"""
        logger.info(f"[Phase 5] Recommending action for case {state['case_id']}")
        state["phase"] = 5

        try:
            # Generate recommendation using LLM
            prompt = f"""
Based on this fraud investigation summary:
- User Risk Score: {state['user_risk_score']:.2f}
- Confidence: {state['confidence_score']:.2f}
- Patterns Matched: {len(state['patterns_matched'])}
- Policies Violated: {', '.join(state['policy_violations']) if state['policy_violations'] else 'None'}

Recommend one action: ALLOW, HOLD, CHALLENGE, or BLOCK.
Provide 1-2 sentence reasoning.
Format: ACTION: [action], REASONING: [reasoning]
"""

            message = self.llm.invoke(prompt)
            response = message.content

            # Parse response
            if "ALLOW" in response.upper():
                state["recommended_action"] = "ALLOW"
            elif "BLOCK" in response.upper():
                state["recommended_action"] = "BLOCK"
            elif "CHALLENGE" in response.upper():
                state["recommended_action"] = "CHALLENGE"
            else:
                state["recommended_action"] = "HOLD"

            state["action_confidence"] = state["confidence_score"]
            state["reasoning"] = response

            state["case_notes"] += f"\n[Phase 5] Recommendation: {state['recommended_action']}"
            logger.info(f"✓ Phase 5 complete: Action {state['recommended_action']} recommended")

        except Exception as e:
            logger.error(f"✗ Phase 5 failed: {str(e)}")
            state["errors"].append(f"Phase 5: {str(e)}")
            state["recommended_action"] = "HOLD"  # Safe default

        return state

    def _phase_6_record_case(self, state: InvestigationState) -> InvestigationState:
        """Phase 6: Record case and findings in TigerGraph"""
        logger.info(f"[Phase 6] Recording case {state['case_id']}")
        state["phase"] = 6

        try:
            # Update case status
            status_map = {
                "ALLOW": "APPROVED",
                "BLOCK": "BLOCKED",
                "CHALLENGE": "UNDER_REVIEW",
                "HOLD": "PENDING",
            }
            case_status = status_map.get(state["recommended_action"], "PENDING")

            update_result = self.mcp.call_tool(
                "update_case_status",
                {
                    "case_id": state["case_id"],
                    "status": "INVESTIGATING",
                    "next_action": state["recommended_action"],
                    "findings": state["reasoning"],
                },
            )

            if update_result.get("success"):
                state["case_status"] = case_status

                # Add evidence
                for pattern in state["patterns_matched"]:
                    self.mcp.call_tool(
                        "add_case_evidence",
                        {
                            "case_id": state["case_id"],
                            "evidence_text": f"Pattern: {pattern.get('title')}",
                            "evidence_type": "pattern",
                        },
                    )

            state["investigation_complete"] = True
            workflow_end = datetime.now()
            workflow_start = datetime.fromisoformat(state["workflow_start_time"])
            state["execution_time_ms"] = (workflow_end - workflow_start).total_seconds() * 1000

            state["case_notes"] += f"\n[Phase 6] Case recorded. Status: {case_status}"
            logger.info(f"✓ Phase 6 complete: Case recorded in graph")

        except Exception as e:
            logger.error(f"✗ Phase 6 failed: {str(e)}")
            state["errors"].append(f"Phase 6: {str(e)}")

        return state

    def _should_request_evidence(self, state: InvestigationState) -> bool:
        """Conditional: should request additional evidence?"""
        return state.get("needs_additional_evidence", False)

    def _evidence_complete(self, state: InvestigationState) -> bool:
        """Conditional: is evidence collection complete?"""
        return not state.get("additional_evidence_requested", False) or state.get("iteration_count", 0) >= 2

    def invoke(self, case_id: str, user_id: str, transaction_id: str, **kwargs) -> Dict[str, Any]:
        """Run investigation workflow"""
        logger.info("=" * 70)
        logger.info(f"Starting investigation workflow for case {case_id}")
        logger.info("=" * 70)

        try:
            # Create initial state
            state = create_initial_state(
                case_id=case_id,
                user_id=user_id,
                transaction_id=transaction_id,
                **kwargs,
            )

            # Build graph if not already built
            if self.graph is None:
                self.build_graph()

            # Run workflow
            result = self.graph.invoke(state)

            logger.info("=" * 70)
            logger.info(f"✓ Investigation complete")
            logger.info(f"  Recommendation: {result.get('recommended_action')}")
            logger.info(f"  Confidence: {result.get('action_confidence'):.2f}")
            logger.info(f"  Time: {result.get('execution_time_ms'):.0f}ms")
            logger.info("=" * 70)

            return result

        except Exception as e:
            logger.error(f"✗ Workflow failed: {str(e)}")
            logger.exception("Full traceback:")
            return {"error": str(e), "case_id": case_id}


def create_investigation_agent() -> InvestigationAgent:
    """Create investigation agent"""
    return InvestigationAgent()


def run_investigation(case_id: str, user_id: str, transaction_id: str, **kwargs) -> Dict[str, Any]:
    """Run investigation workflow"""
    agent = create_investigation_agent()
    return agent.invoke(case_id, user_id, transaction_id, **kwargs)
