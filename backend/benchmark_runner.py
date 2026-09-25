"""
Benchmark Runner - Test fraud investigation accuracy on multiple cases
Tests the system end-to-end with realistic scenarios
"""

import requests
import json
import time
import logging
from typing import List, Dict, Any
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE = "http://localhost:8000/api/v1"

# Test cases with expected outcomes
TEST_CASES = [
    {
        "name": "Low Risk Normal Transaction",
        "user_id": "USR_LOWRISK_001",
        "transaction_id": "TXN_NORMAL_001",
        "initial_risk_level": "LOW",
        "expected_fraud": False
    },
    {
        "name": "Medium Risk with Velocity Check",
        "user_id": "USR_MEDIUM_002",
        "transaction_id": "TXN_VELOCITY_002",
        "initial_risk_level": "MEDIUM",
        "expected_fraud": False
    },
    {
        "name": "High Risk Account Takeover",
        "user_id": "USR_HIGHRISK_003",
        "transaction_id": "TXN_ATO_003",
        "initial_risk_level": "HIGH",
        "expected_fraud": True
    },
    {
        "name": "Critical Risk Pattern Match",
        "user_id": "USR_CRITICAL_004",
        "transaction_id": "TXN_PATTERN_004",
        "initial_risk_level": "HIGH",
        "expected_fraud": True
    },
    {
        "name": "Medium Risk False Positive",
        "user_id": "USR_FALSE_POS_005",
        "transaction_id": "TXN_FALSEPOS_005",
        "initial_risk_level": "MEDIUM",
        "expected_fraud": False
    },
]


def run_benchmark(num_cases: int = 5) -> Dict[str, Any]:
    """Run benchmark on multiple test cases."""
    logger.info(f"Starting benchmark with {num_cases} test cases...")
    
    results = {
        "test_run_date": datetime.now().isoformat(),
        "total_cases": num_cases,
        "cases": [],
        "metrics": {
            "total": 0,
            "correct": 0,
            "false_positives": 0,
            "false_negatives": 0,
            "avg_confidence": 0.0,
            "avg_latency_ms": 0.0
        }
    }
    
    total_latency = 0.0
    confidences = []
    
    for i, test_case in enumerate(TEST_CASES[:num_cases]):
        logger.info(f"\n[{i+1}/{num_cases}] Testing: {test_case['name']}")
        
        try:
            # Start investigation
            start_time = time.time()
            
            response = requests.post(
                f"{API_BASE}/investigations/start",
                json={
                    "user_id": test_case["user_id"],
                    "transaction_id": test_case["transaction_id"],
                    "initial_risk_level": test_case["initial_risk_level"]
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to start investigation: {response.text}")
                continue
            
            case_id = response.json()["case_id"]
            logger.info(f"  Case created: {case_id}")
            
            # Run investigation
            response = requests.post(f"{API_BASE}/investigations/{case_id}/run")
            if response.status_code != 200:
                logger.error(f"Failed to run investigation: {response.text}")
                continue
            
            result = response.json()
            
            # Get recommendation
            response = requests.get(f"{API_BASE}/investigations/{case_id}/recommendation")
            if response.status_code == 200:
                rec = response.json()
                recommended_action = rec.get("recommended_action", "ALLOW")
                confidence = rec.get("action_confidence", 0.0)
            else:
                recommended_action = "UNKNOWN"
                confidence = 0.0
            
            latency_ms = (time.time() - start_time) * 1000
            total_latency += latency_ms
            confidences.append(confidence)
            
            # Determine if predicted fraud
            predicted_fraud = recommended_action in ["HOLD", "CHALLENGE", "BLOCK"]
            expected_fraud = test_case["expected_fraud"]
            is_correct = predicted_fraud == expected_fraud
            
            # Record outcome
            requests.post(
                f"{API_BASE}/investigations/{case_id}/outcome",
                json={
                    "actual_fraud": expected_fraud,
                    "action_taken": recommended_action,
                    "notes": f"Benchmark test: {test_case['name']}"
                }
            )
            
            # Update metrics
            results["metrics"]["total"] += 1
            if is_correct:
                results["metrics"]["correct"] += 1
            elif predicted_fraud and not expected_fraud:
                results["metrics"]["false_positives"] += 1
            elif not predicted_fraud and expected_fraud:
                results["metrics"]["false_negatives"] += 1
            
            case_result = {
                "case_id": case_id,
                "test_name": test_case["name"],
                "predicted_fraud": predicted_fraud,
                "actual_fraud": expected_fraud,
                "correct": is_correct,
                "recommended_action": recommended_action,
                "confidence": confidence,
                "latency_ms": round(latency_ms, 2)
            }
            
            results["cases"].append(case_result)
            
            status = "✓" if is_correct else "✗"
            logger.info(f"  {status} Predicted: {predicted_fraud} (confidence: {confidence:.2f})")
            logger.info(f"     Actual: {expected_fraud} | Action: {recommended_action}")
            logger.info(f"     Latency: {latency_ms:.0f}ms")
            
        except Exception as e:
            logger.error(f"  ✗ Error: {e}")
    
    # Calculate final metrics
    if results["metrics"]["total"] > 0:
        results["metrics"]["accuracy"] = results["metrics"]["correct"] / results["metrics"]["total"]
        results["metrics"]["false_positive_rate"] = (
            results["metrics"]["false_positives"] / results["metrics"]["total"]
        )
        results["metrics"]["false_negative_rate"] = (
            results["metrics"]["false_negatives"] / results["metrics"]["total"]
        )
        results["metrics"]["avg_confidence"] = (
            sum(confidences) / len(confidences) if confidences else 0.0
        )
        results["metrics"]["avg_latency_ms"] = total_latency / results["metrics"]["total"]
    
    return results


def print_benchmark_results(results: Dict[str, Any]):
    """Print formatted benchmark results."""
    print("\n" + "=" * 80)
    print("FRAUD INVESTIGATION SYSTEM - BENCHMARK RESULTS")
    print("=" * 80)
    
    print(f"\nTest Run: {results['test_run_date']}")
    print(f"Total Cases: {results['total_cases']}")
    
    metrics = results["metrics"]
    print(f"\nMetrics:")
    print(f"  Accuracy:             {metrics.get('accuracy', 0):.2%}")
    print(f"  Correct Predictions:  {metrics['correct']}/{metrics['total']}")
    print(f"  False Positives:      {metrics['false_positives']} ({metrics.get('false_positive_rate', 0):.2%})")
    print(f"  False Negatives:      {metrics['false_negatives']} ({metrics.get('false_negative_rate', 0):.2%})")
    print(f"  Avg Confidence:       {metrics.get('avg_confidence', 0):.2f}")
    print(f"  Avg Latency:          {metrics.get('avg_latency_ms', 0):.0f}ms")
    
    print(f"\nDetailed Results:")
    print(f"{'Test Name':<35} {'Pred':<6} {'Actual':<8} {'Conf':<6} {'Result':<8}")
    print("-" * 80)
    
    for case in results["cases"]:
        pred = "FRAUD" if case["predicted_fraud"] else "CLEAN"
        actual = "FRAUD" if case["actual_fraud"] else "CLEAN"
        result = "✓" if case["correct"] else "✗"
        print(f"{case['test_name']:<35} {pred:<6} {actual:<8} {case['confidence']:<6.2f} {result:<8}")
    
    print("=" * 80 + "\n")


def main():
    """Run the benchmark."""
    try:
        # Check if API is running
        response = requests.get(f"{API_BASE.rsplit('/', 1)[0]}", timeout=5)
        logger.info("✓ API is running")
    except Exception as e:
        logger.error(f"✗ API not available: {e}")
        logger.info("Please start the backend with: python -m uvicorn backend.main:app --port 8000")
        return
    
    # Run benchmark
    results = run_benchmark(num_cases=min(5, len(TEST_CASES)))
    
    # Print results
    print_benchmark_results(results)
    
    # Save results
    output_file = "benchmark_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"✓ Results saved to {output_file}")
    
    # Get metrics
    try:
        response = requests.get(f"{API_BASE}/investigations/analytics/metrics")
        if response.status_code == 200:
            analytics = response.json()
            print("\nSystem Analytics:")
            print(json.dumps(analytics, indent=2))
    except Exception as e:
        logger.warning(f"Could not fetch system analytics: {e}")


if __name__ == "__main__":
    main()
