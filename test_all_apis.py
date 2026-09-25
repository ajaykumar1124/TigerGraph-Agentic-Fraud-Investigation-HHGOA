"""
Comprehensive API Testing Script
Tests all backend endpoints and checks connectivity
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(title):
    print(f"\n{'='*70}")
    print(f"{BLUE}{title}{RESET}")
    print(f"{'='*70}")

def print_success(message):
    print(f"{GREEN}✅ {message}{RESET}")

def print_error(message):
    print(f"{RED}❌ {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠️  {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ️  {message}{RESET}")

def test_endpoint(method, url, description, data=None):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        else:
            print_error(f"Unknown method: {method}")
            return False
        
        if response.status_code < 400:
            print_success(f"{description}")
            print(f"   Status: {response.status_code}")
            
            # Show response preview
            try:
                resp_json = response.json()
                if isinstance(resp_json, dict):
                    # Show first few keys
                    keys = list(resp_json.keys())[:3]
                    print(f"   Response keys: {keys}")
                elif isinstance(resp_json, list):
                    print(f"   Response: List with {len(resp_json)} items")
                else:
                    print(f"   Response: {str(resp_json)[:100]}")
            except:
                print(f"   Response: {response.text[:100]}")
            
            return True
        else:
            print_error(f"{description}")
            print(f"   Status: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error(f"{description}")
        print(f"   Error: Cannot connect to {url}")
        return False
    except requests.exceptions.Timeout:
        print_error(f"{description}")
        print(f"   Error: Request timeout")
        return False
    except Exception as e:
        print_error(f"{description}")
        print(f"   Error: {str(e)}")
        return False

def main():
    print_header("🚀 BACKEND API COMPREHENSIVE TEST")
    print(f"Testing API at: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'total': 0,
        'passed': 0,
        'failed': 0
    }
    
    # Test 1: Root endpoint
    print_header("1. Basic Connectivity")
    results['total'] += 1
    if test_endpoint("GET", f"{BASE_URL}/", "Root endpoint"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 2: Health endpoint
    print_header("2. Health Check")
    results['total'] += 1
    if test_endpoint("GET", f"{BASE_URL}/api/health", "Health endpoint"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 3: API root
    results['total'] += 1
    if test_endpoint("GET", f"{BASE_URL}/api", "API root"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 4: Investigations endpoints
    print_header("3. Investigations API")
    
    results['total'] += 1
    if test_endpoint("GET", f"{BASE_URL}/api/v1/investigations", "List investigations"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    results['total'] += 1
    if test_endpoint("GET", f"{BASE_URL}/api/v1/investigations/metrics", "Investigation metrics"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    results['total'] += 1
    if test_endpoint("GET", f"{BASE_URL}/api/v1/investigations/analytics/metrics", "Analytics metrics"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 5: Cases endpoints
    print_header("4. Cases API")
    
    results['total'] += 1
    if test_endpoint("GET", f"{BASE_URL}/api/v1/cases", "List cases"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    results['total'] += 1
    if test_endpoint("GET", f"{BASE_URL}/api/v1/cases/stats", "Case statistics"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 6: Fraud detection
    print_header("5. Fraud Detection API")
    
    results['total'] += 1
    if test_endpoint("GET", f"{BASE_URL}/api/v1/fraud/patterns", "Fraud patterns"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    results['total'] += 1
    test_transaction = {
        "transaction_id": "TEST_TXN_001",
        "amount": 5000,
        "merchant_name": "Test Merchant",
        "timestamp": datetime.now().isoformat()
    }
    if test_endpoint("POST", f"{BASE_URL}/api/v1/fraud/detect", "Fraud detection", test_transaction):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 7: LLM Investigation Agent
    print_header("6. LLM Investigation Agent API")
    
    results['total'] += 1
    if test_endpoint("GET", f"{BASE_URL}/api/investigation/health", "LLM agent health"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    results['total'] += 1
    if test_endpoint("GET", f"{BASE_URL}/api/investigation/patterns", "Fraud patterns knowledge"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    results['total'] += 1
    analyze_request = {
        "case_id": "TEST_CASE_001",
        "include_user_data": True,
        "max_transactions": 10
    }
    if test_endpoint("POST", f"{BASE_URL}/api/investigation/analyze-case", "Analyze case", analyze_request):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    results['total'] += 1
    investigate_request = {
        "transaction_id": "TEST_TXN_001"
    }
    if test_endpoint("POST", f"{BASE_URL}/api/investigation/investigate-transaction", "Investigate transaction", investigate_request):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 8: API Documentation
    print_header("7. API Documentation")
    
    results['total'] += 1
    if test_endpoint("GET", f"{BASE_URL}/api/docs", "Swagger UI"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    results['total'] += 1
    if test_endpoint("GET", f"{BASE_URL}/api/openapi.json", "OpenAPI spec"):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Summary
    print_header("📊 TEST SUMMARY")
    print(f"\nTotal Tests: {results['total']}")
    print_success(f"Passed: {results['passed']}")
    print_error(f"Failed: {results['failed']}")
    
    success_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
    print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    if results['failed'] == 0:
        print_success("\n🎉 ALL TESTS PASSED! API is fully functional!")
    elif results['passed'] > results['failed']:
        print_warning(f"\n⚠️  {results['failed']} tests failed. API is partially functional.")
    else:
        print_error(f"\n❌ {results['failed']} tests failed. API has issues.")
    
    print("\n" + "="*70)
    print("📋 ENDPOINT REFERENCE:")
    print("="*70)
    print(f"\n🌐 API Documentation: {BASE_URL}/api/docs")
    print(f"🔍 Health Check: {BASE_URL}/api/health")
    print(f"📊 Investigations: {BASE_URL}/api/v1/investigations")
    print(f"📁 Cases: {BASE_URL}/api/v1/cases")
    print(f"🚨 Fraud Detection: {BASE_URL}/api/v1/fraud/detect")
    print(f"🤖 LLM Investigation: {BASE_URL}/api/investigation/analyze-case")
    print("\n" + "="*70)
    
    return results['failed'] == 0

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
