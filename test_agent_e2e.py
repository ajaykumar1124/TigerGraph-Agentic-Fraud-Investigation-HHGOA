#!/usr/bin/env python
"""
End-to-End Test of Fraud Investigation Agent

Demonstrates the full investigation workflow:
1. Start investigation
2. Run agent analysis
3. Get recommendation
4. Submit additional evidence
5. Get final case record
"""

import requests
import json
import time
from typing import Dict

BASE_URL = "http://localhost:8000/api/v1"

class FraudInvestigationTester:
    def __init__(self):
        self.session = requests.Session()
        self.current_case_id = None
    
    def test_health(self):
        """Test API health."""
        print("\n" + "="*70)
        print("STEP 1: Check API Health")
        print("="*70)
        
        try:
            response = requests.get("http://localhost:8000/health")
            print(f"✓ API is running: {response.json()}")
            return True
        except Exception as e:
            print(f"✗ API health check failed: {e}")
            return False
    
    def start_investigation(self):
        """Start a new investigation."""
        print("\n" + "="*70)
        print("STEP 2: Start Investigation")
        print("="*70)
        
        payload = {
            "customer_id": "C000001",
            "transaction_id": "TX00000001",
            "trigger_type": "HIGH_RISK",
            "initial_risk": 0.75
        }
        
        print(f"\nStarting investigation with payload:")
        print(json.dumps(payload, indent=2))
        
        try:
            response = requests.post(
                f"{BASE_URL}/investigations/start",
                json=payload
            )
            result = response.json()
            self.current_case_id = result["case_id"]
            
            print(f"\n✓ Investigation started!")
            print(f"  Case ID: {self.current_case_id}")
            print(f"  Initial Risk: {result['initial_risk']}")
            
            return True
        except Exception as e:
            print(f"✗ Failed to start investigation: {e}")
            return False
    
    def run_investigation(self):
        """Run the investigation workflow."""
        print("\n" + "="*70)
        print("STEP 3: Run Investigation Workflow")
        print("="*70)
        
        if not self.current_case_id:
            print("✗ No case ID. Start investigation first.")
            return False
        
        print(f"\nRunning investigation for case: {self.current_case_id}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/investigations/{self.current_case_id}/investigate"
            )
            result = response.json()
            
            print(f"\n✓ Investigation workflow complete!")
            print(f"  Risk Score: {result['risk_score']:.2f}")
            print(f"  Confidence: {result['confidence_score']:.2f}")
            print(f"  Evidence Collected: {result['evidence_count']}")
            print(f"  Recommended Action: {result['recommended_action']['action']}")
            
            return True
        except Exception as e:
            print(f"✗ Investigation workflow failed: {e}")
            return False
    
    def get_investigation_details(self):
        """Get detailed investigation information."""
        print("\n" + "="*70)
        print("STEP 4: Get Investigation Details")
        print("="*70)
        
        if not self.current_case_id:
            print("✗ No case ID.")
            return False
        
        try:
            response = requests.get(
                f"{BASE_URL}/investigations/{self.current_case_id}"
            )
            result = response.json()
            
            print(f"\n📋 Investigation Summary for {self.current_case_id}:")
            print(f"  Customer: {result['customer_id']}")
            print(f"  Status: {result['status']}")
            print(f"  Risk Score: {result['risk_score']:.2f}")
            print(f"  Confidence: {result['confidence_score']:.2f}")
            
            print(f"\n📊 Evidence Collected:")
            evidence_summary = result['evidence']
            print(f"  Total Evidence: {evidence_summary['total_evidence']}")
            for etype, count in evidence_summary['by_type'].items():
                print(f"    - {etype}: {count}")
            print(f"  Average Confidence: {evidence_summary['average_confidence']:.2f}")
            
            if result['recommended_action']:
                print(f"\n⚡ Recommended Action:")
                action = result['recommended_action']
                print(f"  Action: {action['action_type']}")
                print(f"  Requires Approval: {action['requires_approval']}")
                print(f"  Rationale: {action['rationale']}")
            
            print(f"\n📝 Investigation Log (last 5 entries):")
            for log in result['investigation_log'][-5:]:
                print(f"  {log}")
            
            return True
        except Exception as e:
            print(f"✗ Failed to get investigation details: {e}")
            return False
    
    def submit_additional_evidence(self):
        """Submit additional evidence."""
        print("\n" + "="*70)
        print("STEP 5: Submit Additional Evidence")
        print("="*70)
        
        if not self.current_case_id:
            print("✗ No case ID.")
            return False
        
        payload = {
            "evidence_type": "CUSTOMER_VALIDATION",
            "evidence_data": {
                "confirmed": False,
                "message": "Customer denied making this transaction"
            }
        }
        
        print(f"\nSubmitting additional evidence:")
        print(json.dumps(payload, indent=2))
        
        try:
            response = requests.post(
                f"{BASE_URL}/investigations/{self.current_case_id}/additional-evidence",
                json=payload
            )
            result = response.json()
            
            print(f"\n✓ Additional evidence submitted!")
            print(f"  Updated Risk Score: {result['risk_score']:.2f}")
            print(f"  Updated Confidence: {result['confidence_score']:.2f}")
            print(f"  Needs More Evidence: {result['needs_more_evidence']}")
            
            if result['recommended_action']:
                print(f"  Updated Action: {result['recommended_action']['action_type']}")
            
            return True
        except Exception as e:
            print(f"✗ Failed to submit additional evidence: {e}")
            return False
    
    def get_recommendation(self):
        """Get the final recommendation."""
        print("\n" + "="*70)
        print("STEP 6: Get Final Recommendation")
        print("="*70)
        
        if not self.current_case_id:
            print("✗ No case ID.")
            return False
        
        try:
            response = requests.get(
                f"{BASE_URL}/investigations/{self.current_case_id}/recommendation"
            )
            result = response.json()
            
            print(f"\n📋 Final Recommendation for {self.current_case_id}:")
            
            if "recommended_action" in result:
                action = result['recommended_action']
                print(f"  Action: {action['action_type']}")
                print(f"  Confidence: {action['confidence']:.2f}")
                print(f"  Requires Approval: {action['requires_approval']}")
                print(f"  Approval Role: {action['approval_role']}")
                print(f"  Rationale: {action['rationale']}")
            
            if "policy_evaluation" in result:
                policy = result['policy_evaluation']
                print(f"\n⚖️ Policy Evaluation:")
                print(f"  Policy Action: {policy['action']}")
                print(f"  Requires Approval: {policy['requires_approval']}")
                print(f"  Approval Role: {policy['approval_role']}")
                print(f"  Rationale: {policy['policy_rationale']}")
            
            return True
        except Exception as e:
            print(f"✗ Failed to get recommendation: {e}")
            return False
    
    def list_investigations(self):
        """List all investigations."""
        print("\n" + "="*70)
        print("STEP 7: List All Investigations")
        print("="*70)
        
        try:
            response = requests.get(f"{BASE_URL}/investigations")
            result = response.json()
            
            print(f"\n📊 Total Investigations: {result['total']}")
            print(f"\nInvestigations:")
            for case in result['cases']:
                print(f"\n  Case: {case['case_id']}")
                print(f"    Customer: {case['customer_id']}")
                print(f"    Status: {case['status']}")
                print(f"    Risk: {case['risk_score']:.2f}")
                print(f"    Confidence: {case['confidence_score']:.2f}")
            
            return True
        except Exception as e:
            print(f"✗ Failed to list investigations: {e}")
            return False
    
    def run_full_test(self):
        """Run the complete test suite."""
        print("\n" + "="*70)
        print("FRAUD INVESTIGATION AGENT - END-TO-END TEST")
        print("="*70)
        
        steps = [
            ("API Health", self.test_health),
            ("Start Investigation", self.start_investigation),
            ("Run Investigation Workflow", self.run_investigation),
            ("Get Investigation Details", self.get_investigation_details),
            ("Submit Additional Evidence", self.submit_additional_evidence),
            ("Get Investigation Details (Updated)", self.get_investigation_details),
            ("Get Final Recommendation", self.get_recommendation),
            ("List All Investigations", self.list_investigations),
        ]
        
        results = []
        for step_name, step_func in steps:
            try:
                success = step_func()
                results.append((step_name, "✓ PASS" if success else "✗ FAIL"))
            except Exception as e:
                print(f"\n✗ Step failed with exception: {e}")
                results.append((step_name, f"✗ ERROR: {str(e)[:50]}"))
        
        print("\n" + "="*70)
        print("TEST RESULTS SUMMARY")
        print("="*70)
        for step, result in results:
            print(f"{step:40s} {result}")
        
        passed = sum(1 for _, r in results if "✓" in r)
        total = len(results)
        print(f"\nTotal: {passed}/{total} steps passed")
        print("="*70 + "\n")


if __name__ == "__main__":
    print("\n🚀 Starting Fraud Investigation Agent E2E Test\n")
    print("Make sure both servers are running:")
    print("  Backend: http://localhost:8000")
    print("  Frontend: http://localhost:5173")
    
    tester = FraudInvestigationTester()
    tester.run_full_test()
