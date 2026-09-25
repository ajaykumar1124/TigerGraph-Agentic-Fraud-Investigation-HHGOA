"""
Policy Engine for Fraud Investigation

Manages fraud policies, action approvals, and compliance rules.
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass


class ApprovalRole(str, Enum):
    """Roles that can approve actions."""
    ANALYST = "ANALYST"
    SENIOR_ANALYST = "SENIOR_ANALYST"
    MANAGER = "MANAGER"
    SYSTEM = "SYSTEM"


class FraudPolicy:
    """Fraud detection and response policy."""
    
    # Risk thresholds
    LOW_RISK_THRESHOLD = 0.4
    MEDIUM_RISK_THRESHOLD = 0.65
    HIGH_RISK_THRESHOLD = 0.85
    CRITICAL_RISK_THRESHOLD = 0.95
    
    @classmethod
    def _get_rules(cls):
        """Get decision rules (as method to access class attributes)."""
        return {
            # Critical risk, high confidence -> Block immediately
            "critical_high_confidence": {
                "condition": lambda r, c: r >= cls.CRITICAL_RISK_THRESHOLD and c >= 0.85,
                "action": "BLOCK_ACCOUNT",
                "requires_approval": True,
                "approval_role": "MANAGER"
            },
            
            # High risk, high confidence -> Block with analyst approval
            "high_high_confidence": {
                "condition": lambda r, c: r >= cls.HIGH_RISK_THRESHOLD and c >= 0.75,
                "action": "BLOCK_ACCOUNT",
                "requires_approval": True,
                "approval_role": "ANALYST"
            },
            
            # High risk, medium confidence -> Request authentication
            "high_medium_confidence": {
                "condition": lambda r, c: r >= cls.HIGH_RISK_THRESHOLD and 0.5 <= c < 0.75,
                "action": "REQUEST_AUTH",
                "requires_approval": False,
                "approval_role": None
            },
            
            # High risk, low confidence -> Hold for review
            "high_low_confidence": {
                "condition": lambda r, c: r >= cls.HIGH_RISK_THRESHOLD and c < 0.5,
                "action": "HOLD_TRANSACTION",
                "requires_approval": True,
                "approval_role": "ANALYST"
            },
            
            # Medium risk -> Hold or request validation
            "medium_risk": {
                "condition": lambda r, c: cls.MEDIUM_RISK_THRESHOLD <= r < cls.HIGH_RISK_THRESHOLD,
                "action": "HOLD_TRANSACTION",
                "requires_approval": True,
                "approval_role": "ANALYST"
            },
            
            # Low risk -> Allow with monitoring
            "low_risk": {
                "condition": lambda r, c: r < cls.MEDIUM_RISK_THRESHOLD,
                "action": "ALLOW",
                "requires_approval": False,
                "approval_role": None
            }
        }
    
    @classmethod
    def get_action_for_risk(
        cls,
        risk_score: float,
        confidence_score: float
    ) -> Tuple[str, bool, Optional[str]]:
        """
        Determine recommended action based on risk and confidence.
        
        Returns: (action, requires_approval, approval_role)
        """
        rules = cls._get_rules()
        for rule_name, rule in rules.items():
            if rule["condition"](risk_score, confidence_score):
                return (
                    rule["action"],
                    rule["requires_approval"],
                    rule["approval_role"]
                )
        
        # Default
        return ("ALLOW", False, None)
    
    @classmethod
    def get_policy_description(cls) -> str:
        """Get human-readable policy description."""
        return """
FRAUD DETECTION POLICY

Risk Thresholds:
- Low:      < 0.40
- Medium:   0.40 - 0.64
- High:     0.65 - 0.84
- Critical: >= 0.95

Decision Matrix:
1. Critical Risk + High Confidence -> BLOCK (Manager approval)
2. High Risk + High Confidence -> BLOCK (Analyst approval)
3. High Risk + Medium Confidence -> REQUEST_AUTH (No approval)
4. High Risk + Low Confidence -> HOLD (Analyst approval)
5. Medium Risk -> HOLD (Analyst approval)
6. Low Risk -> ALLOW (No approval)

Action Definitions:
- ALLOW: Permit transaction, add to monitoring list
- HOLD_TRANSACTION: Prevent transaction, pending review
- REQUEST_AUTH: Request step-up authentication from customer
- BLOCK_ACCOUNT: Block account for suspicious activity
- MONITOR: Continue transaction but flag account
- ESCALATE: Escalate to senior analyst for manual review

Approval Requirements:
- System: Automatic (no human approval needed)
- Analyst: Fraud team member (junior level)
- Senior Analyst: Fraud team lead
- Manager: Fraud department manager
"""


class PolicyEngine:
    """Manages policy decisions and approvals."""
    
    def __init__(self):
        """Initialize policy engine."""
        self.fraud_policy = FraudPolicy()
        self.approval_history: List[Dict] = []
    
    def evaluate_action(
        self,
        case_id: str,
        risk_score: float,
        confidence_score: float
    ) -> Dict:
        """
        Evaluate what action should be taken for a case.
        
        Returns:
        {
          "action": "BLOCK_ACCOUNT",
          "requires_approval": True,
          "approval_role": "ANALYST",
          "policy_rationale": "High risk + high confidence",
          "case_id": "..."
        }
        """
        action, requires_approval, approval_role = self.fraud_policy.get_action_for_risk(
            risk_score,
            confidence_score
        )
        
        # Determine rationale
        if risk_score >= self.fraud_policy.CRITICAL_RISK_THRESHOLD:
            risk_level = "CRITICAL"
        elif risk_score >= self.fraud_policy.HIGH_RISK_THRESHOLD:
            risk_level = "HIGH"
        elif risk_score >= self.fraud_policy.MEDIUM_RISK_THRESHOLD:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        if confidence_score >= 0.75:
            confidence_level = "HIGH"
        elif confidence_score >= 0.5:
            confidence_level = "MEDIUM"
        else:
            confidence_level = "LOW"
        
        rationale = f"{risk_level} risk ({risk_score:.2f}) + {confidence_level} confidence ({confidence_score:.2f})"
        
        return {
            "case_id": case_id,
            "action": action,
            "requires_approval": requires_approval,
            "approval_role": approval_role,
            "policy_rationale": rationale,
            "risk_level": risk_level,
            "confidence_level": confidence_level
        }
    
    def can_execute_action(
        self,
        action: str,
        user_role: str
    ) -> Tuple[bool, str]:
        """
        Check if a user can execute an action.
        
        Returns: (allowed, reason)
        """
        # Define role hierarchy
        role_hierarchy = {
            "ANALYST": 1,
            "SENIOR_ANALYST": 2,
            "MANAGER": 3,
            "SYSTEM": 99  # System can do anything
        }
        
        # Actions that require specific approvals
        action_requirements = {
            "BLOCK_ACCOUNT": ("MANAGER", "SENIOR_ANALYST", "ANALYST"),
            "HOLD_TRANSACTION": ("ANALYST", "SENIOR_ANALYST", "MANAGER"),
            "REQUEST_AUTH": ("SYSTEM",),  # Automatic
            "ALLOW": ("SYSTEM",),  # Automatic
            "ESCALATE": ("ANALYST", "SENIOR_ANALYST", "MANAGER")
        }
        
        # Check if action exists in requirements
        if action not in action_requirements:
            return False, f"Unknown action: {action}"
        
        required_roles = action_requirements[action]
        
        if user_role not in role_hierarchy:
            return False, f"Unknown user role: {user_role}"
        
        if user_role in required_roles:
            return True, "Authorized"
        
        return False, f"User role '{user_role}' cannot execute action '{action}'"
    
    def record_approval(
        self,
        case_id: str,
        action: str,
        approved: bool,
        approved_by: str,
        notes: str = ""
    ) -> Dict:
        """Record an approval decision."""
        from datetime import datetime
        
        record = {
            "case_id": case_id,
            "action": action,
            "approved": approved,
            "approved_by": approved_by,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        
        self.approval_history.append(record)
        
        return record
    
    def get_approval_history(self, case_id: str) -> List[Dict]:
        """Get approval history for a case."""
        return [a for a in self.approval_history if a["case_id"] == case_id]


class SuspiciousActivityReport:
    """Generate Suspicious Activity Reports (SARs) when required by policy."""
    
    @staticmethod
    def should_file_sar(
        risk_score: float,
        fraud_pattern: Optional[str] = None,
        transaction_amount: float = 0
    ) -> bool:
        """
        Determine if a SAR should be filed based on policy.
        
        SAR triggers:
        - Risk score > 0.95
        - Confirmed fraud pattern
        - Transaction > $5000 with high risk
        """
        if risk_score > 0.95:
            return True
        
        if fraud_pattern in ["ACCOUNT_TAKEOVER", "FRAUD_NETWORK"]:
            if risk_score > 0.85:
                return True
        
        if transaction_amount > 5000 and risk_score > 0.80:
            return True
        
        return False
    
    @staticmethod
    def generate_sar(
        case_id: str,
        customer_id: str,
        transaction_id: Optional[str],
        risk_score: float,
        fraud_pattern: Optional[str],
        evidence_summary: Dict,
        investigation_notes: str
    ) -> Dict:
        """
        Generate a Suspicious Activity Report.
        
        Returns SAR document (would be filed with financial regulator).
        """
        from datetime import datetime
        
        return {
            "report_type": "SAR",
            "report_date": datetime.now().isoformat(),
            "filing_institution": "BankGuard",
            "case_id": case_id,
            "customer_id": customer_id,
            "transaction_id": transaction_id,
            "risk_score": risk_score,
            "fraud_pattern": fraud_pattern,
            "evidence_summary": evidence_summary,
            "investigation_notes": investigation_notes,
            "status": "PENDING_REVIEW",
            "filed": False
        }


def print_policy_info():
    """Print policy information."""
    engine = PolicyEngine()
    
    print("\n" + "="*70)
    print("FRAUD DETECTION POLICY")
    print("="*70)
    
    print(FraudPolicy.get_policy_description())
    
    print("\n" + "="*70)
    print("EXAMPLE DECISIONS")
    print("="*70 + "\n")
    
    test_cases = [
        (0.95, 0.95, "CASE_CRITICAL"),
        (0.85, 0.80, "CASE_HIGH_HIGH"),
        (0.85, 0.60, "CASE_HIGH_MED"),
        (0.70, 0.70, "CASE_MEDIUM"),
        (0.30, 0.50, "CASE_LOW"),
    ]
    
    for risk, conf, case in test_cases:
        result = engine.evaluate_action(case, risk, conf)
        print(f"Risk: {risk:.2f}, Confidence: {conf:.2f}")
        print(f"  → Action: {result['action']}")
        print(f"  → Approval: {result['approval_role'] if result['requires_approval'] else 'None'}")
        print(f"  → Rationale: {result['policy_rationale']}\n")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    print_policy_info()
