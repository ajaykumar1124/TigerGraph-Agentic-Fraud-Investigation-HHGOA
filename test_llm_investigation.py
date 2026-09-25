"""
Test LLM Investigation Agent
Demonstrates AI-powered fraud investigation capabilities
"""

import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.abspath('.'))

from backend.services.llm_investigation_agent import fraud_investigation_agent

def test_agent_initialization():
    """Test agent initialization"""
    print("=" * 70)
    print("🔍 LLM Investigation Agent Test")
    print("=" * 70)
    print()
    
    print("1. Agent Configuration:")
    print(f"   Model: {fraud_investigation_agent.model}")
    print(f"   Temperature: {fraud_investigation_agent.temperature}")
    print(f"   Max Tokens: {fraud_investigation_agent.max_tokens}")
    print(f"   OpenAI Client: {'✅ Connected' if fraud_investigation_agent.client else '❌ Not available (fallback mode)'}")
    print()

def test_fraud_patterns():
    """Test fraud patterns knowledge base"""
    print("2. Fraud Patterns Knowledge Base:")
    print()
    
    for pattern_name, pattern_info in fraud_investigation_agent.fraud_patterns.items():
        print(f"   📋 {pattern_name.replace('_', ' ').title()}")
        print(f"      Severity: {pattern_info['severity']}")
        print(f"      Description: {pattern_info['description']}")
        print(f"      Typical Loss: {pattern_info['typical_loss']}")
        print()

def test_case_analysis():
    """Test case analysis with sample data"""
    print("3. Testing Case Analysis:")
    print()
    
    # Sample case data
    case_data = {
        "case_id": "CASE_TEST_001",
        "title": "Suspicious High-Value Transactions",
        "status": "open",
        "severity": "high",
        "description": "Multiple high-value transactions detected within 2 hours",
        "created_at": "2026-09-23T10:00:00",
        "assigned_to": "investigator@bank.com",
        "amount_at_risk": 15000.00,
        "pattern_type": "rapid_spending"
    }
    
    # Sample transactions
    transactions = [
        {
            "transaction_id": "TXN_001",
            "amount": 5000.00,
            "merchant_name": "Electronics Store",
            "merchant_category": "Electronics",
            "payment_method": "credit_card",
            "timestamp": "2026-09-23T10:15:00",
            "risk_score": 0.85,
            "status": "flagged",
            "fraud_flag": True
        },
        {
            "transaction_id": "TXN_002",
            "amount": 4500.00,
            "merchant_name": "Jewelry Store",
            "merchant_category": "Luxury",
            "payment_method": "credit_card",
            "timestamp": "2026-09-23T11:30:00",
            "risk_score": 0.92,
            "status": "flagged",
            "fraud_flag": True
        },
        {
            "transaction_id": "TXN_003",
            "amount": 5500.00,
            "merchant_name": "Online Electronics",
            "merchant_category": "Electronics",
            "payment_method": "credit_card",
            "timestamp": "2026-09-23T11:45:00",
            "risk_score": 0.88,
            "status": "flagged",
            "fraud_flag": True
        }
    ]
    
    # Sample user data
    user_data = {
        "user_id": "USR_001",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "created_at": "2025-01-15T00:00:00",
        "risk_score": 0.75,
        "status": "flagged"
    }
    
    print("   Analyzing case with AI...")
    print()
    
    # Run analysis
    analysis = fraud_investigation_agent.analyze_case(
        case_data=case_data,
        transactions=transactions,
        user_data=user_data
    )
    
    print("   ✅ Analysis Complete!")
    print()
    print("   📊 Results:")
    print(f"      Risk Score: {analysis.get('risk_score', 0):.2f} / 1.00")
    print(f"      Confidence: {analysis.get('confidence', 0) * 100:.0f}%")
    print(f"      Model: {analysis.get('model_used', 'unknown')}")
    print(f"      Patterns: {', '.join(analysis.get('pattern_matches', ['None']))}")
    print()
    
    if analysis.get('recommendations'):
        print("   🎯 Top Recommendations:")
        for i, rec in enumerate(analysis.get('recommendations', [])[:3], 1):
            print(f"      {i}. {rec}")
        print()
    
    print("   📄 Full Analysis:")
    print("   " + "-" * 66)
    for line in analysis.get('analysis', 'No analysis').split('\n'):
        print(f"   {line}")
    print("   " + "-" * 66)
    print()

def test_transaction_investigation():
    """Test single transaction investigation"""
    print("4. Testing Transaction Investigation:")
    print()
    
    transaction = {
        "transaction_id": "TXN_SUSPICIOUS_001",
        "amount": 8500.00,
        "merchant_name": "Unknown Merchant",
        "merchant_category": "Other",
        "payment_method": "credit_card",
        "timestamp": "2026-09-23T14:30:00",
        "risk_score": 0.78,
        "status": "pending"
    }
    
    print("   Investigating suspicious transaction...")
    print()
    
    result = fraud_investigation_agent.investigate_transaction(transaction)
    
    print("   ✅ Investigation Complete!")
    print()
    print(f"      Transaction ID: {result.get('transaction_id')}")
    print(f"      Fraud Likelihood: {result.get('fraud_likelihood', 0):.2f}")
    print(f"      Recommendation: {result.get('recommendation', 'unknown').upper()}")
    print()
    print("   Analysis:")
    print(f"   {result.get('analysis', 'No analysis')}")
    print()

def test_report_generation():
    """Test report generation"""
    print("5. Testing Report Generation:")
    print()
    
    case_data = {
        "case_id": "CASE_REPORT_TEST",
        "title": "Test Investigation Report",
        "status": "open",
        "severity": "high",
        "description": "Sample case for report testing",
        "created_at": "2026-09-23T10:00:00",
        "assigned_to": "ai-investigator@bank.com",
        "amount_at_risk": 25000.00
    }
    
    analysis = {
        "risk_score": 0.87,
        "confidence": 0.92,
        "model_used": "gpt-4o-mini",
        "pattern_matches": ["rapid_spending", "account_takeover"],
        "analysis": "Test analysis with multiple indicators of fraud including rapid spending patterns and suspicious account activity.",
        "recommendations": [
            "Block all pending transactions",
            "Contact user immediately",
            "Review account history",
            "File fraud report"
        ]
    }
    
    report = fraud_investigation_agent.generate_investigation_report(
        case_data=case_data,
        analysis=analysis
    )
    
    print(report)
    print()

def test_not_found_case():
    """Test 'Investigation not found' scenario (training data)"""
    print("6. Testing 'Investigation Not Found' Scenario:")
    print()
    
    case_data = {
        "case_id": "CASE_NONEXISTENT",
        "title": "Case Not Found",
        "status": "not_found",
        "severity": "unknown",
        "description": "This investigation could not be retrieved.",
        "created_at": None,
        "assigned_to": None,
        "amount_at_risk": 0
    }
    
    analysis = {
        "risk_score": 0.0,
        "analysis": "Investigation not found. This investigation could not be retrieved. Please verify the case ID and try again.",
        "recommendations": ["Verify case ID", "Check if case was deleted", "Contact administrator"],
        "pattern_matches": [],
        "confidence": 0.0,
        "model_used": "system"
    }
    
    report = fraud_investigation_agent.generate_investigation_report(
        case_data=case_data,
        analysis=analysis
    )
    
    print(report)
    print()

def main():
    """Run all tests"""
    print()
    
    test_agent_initialization()
    test_fraud_patterns()
    
    if fraud_investigation_agent.client:
        print("🚀 OpenAI API is configured - Running full AI tests")
        print()
        test_case_analysis()
        test_transaction_investigation()
    else:
        print("⚠️  OpenAI API not configured - Running fallback mode tests")
        print()
        print("To test full AI capabilities, set OPENAI_API_KEY in .env")
        print()
    
    test_report_generation()
    test_not_found_case()
    
    print("=" * 70)
    print("✅ All Tests Complete!")
    print("=" * 70)
    print()
    
    if fraud_investigation_agent.client:
        print("🎯 LLM Investigation Agent is fully operational!")
    else:
        print("🔧 LLM Investigation Agent running in fallback mode")
        print("   Set OPENAI_API_KEY in .env to enable full AI capabilities")
    print()

if __name__ == "__main__":
    main()
