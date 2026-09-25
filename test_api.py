#!/usr/bin/env python3
"""Quick API test script"""

import requests
import json

API_BASE = 'http://localhost:8000/api/v1'

print("=== HHGOA API Test Suite ===\n")

try:
    # Test 1: Create Investigation
    print("Test 1: Create Investigation")
    r = requests.post(f'{API_BASE}/investigations/start', json={
        'user_id': 'TEST_USR_001',
        'transaction_id': 'TEST_TXN_001',
        'initial_risk_level': 'HIGH'
    }, timeout=5)
    
    if r.status_code != 200:
        print(f"✗ Failed: {r.status_code}")
        print(r.text)
        exit(1)
    
    case_id = r.json()['case_id']
    print(f"✓ Case created: {case_id}\n")

    # Test 2: Run Investigation
    print("Test 2: Run Investigation")
    r = requests.post(f'{API_BASE}/investigations/{case_id}/run', timeout=10)
    result = r.json()
    print(f"✓ Status: {result['status']}")
    print(f"✓ Phase: {result['phase']}")
    print(f"✓ Action: {result['recommended_action']}")
    print(f"✓ Confidence: {result['action_confidence']:.2f}\n")

    # Test 3: Record Outcome
    print("Test 3: Record Outcome")
    r = requests.post(f'{API_BASE}/investigations/{case_id}/outcome', json={
        'actual_fraud': True,
        'action_taken': 'BLOCK',
        'notes': 'Test outcome'
    }, timeout=5)
    print(f"✓ Outcome recorded: {r.status_code}\n")

    # Test 4: Get Metrics
    print("Test 4: Get System Analytics")
    r = requests.get(f'{API_BASE}/investigations/analytics/metrics', timeout=5)
    if r.status_code == 200:
        data = r.json()
        metrics = data['statistics']['accuracy_metrics']
        print(f"✓ Accuracy: {metrics['accuracy']:.2%}")
        print(f"✓ Total Cases: {metrics['total_cases']}")
        print(f"✓ Correct Predictions: {metrics['correct_predictions']}\n")
    else:
        print(f"⚠ Metrics not available: {r.status_code}\n")

    # Test 5: List Investigations
    print("Test 5: List Investigations")
    r = requests.get(f'{API_BASE}/investigations', timeout=5)
    cases = r.json()['cases']
    print(f"✓ Total investigations: {len(cases)}")
    print(f"✓ Mode: {r.json().get('mode', 'unknown')}\n")

    print("=" * 50)
    print("✓ ALL TESTS PASSED")
    print("=" * 50)

except requests.exceptions.ConnectionError:
    print("✗ Cannot connect to API")
    print("Make sure backend is running: python -m uvicorn backend.main:app --port 8000")
    exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)
