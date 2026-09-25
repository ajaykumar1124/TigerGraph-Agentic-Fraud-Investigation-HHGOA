"""Benchmark case evaluator - runs all 20 benchmark cases through the agent and collects metrics."""

import json
import time
from pathlib import Path
from backend.agents.investigation_agent import FraudInvestigationAgent
from backend.policies.policy_engine import PolicyEngine

# Initialize agent and policy engine
agent = FraudInvestigationAgent(use_simulation=True)
policy_engine = PolicyEngine()

# Paths
BENCHMARK_CASES_PATH = Path("tigergraph/data/benchmark_cases.json")
RESULTS_OUTPUT_PATH = Path("benchmark/results.json")
RESULTS_OUTPUT_PATH.parent.mkdir(exist_ok=True)

def load_benchmark_cases():
    """Load the 20 benchmark cases."""
    if not BENCHMARK_CASES_PATH.exists():
        print(f"ERROR: Benchmark cases file not found at {BENCHMARK_CASES_PATH}")
        return []
    
    with open(BENCHMARK_CASES_PATH, 'r') as f:
        data = json.load(f)
    
    return data.get('benchmark_cases', []) if isinstance(data, dict) else data

def run_benchmark_case(case_idx, case_data):
    """Run a single benchmark case through the agent."""
    print(f"\n{'='*60}")
    print(f"Benchmark Case {case_idx + 1}/20")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Start investigation
        case_id = f"BENCH_{case_idx:02d}_{int(time.time() * 1000) % 10000}"
        customer_id = case_data.get('customer_id', f'CUST_{case_idx:03d}')
        transaction_id = case_data.get('transaction_id', f'TXN_{case_idx:06d}')
        
        print(f"Case ID: {case_id}")
        print(f"Customer: {customer_id}, Transaction: {transaction_id}")
        print(f"Ground truth label: {case_data.get('label', 'UNKNOWN')}")
        
        # Initialize investigation state
        state = agent.start_investigation(
            case_id=case_id,
            customer_id=customer_id,
            transaction_id=transaction_id,
            trigger_type=case_data.get('trigger_type', 'HIGH_RISK'),
            initial_risk=case_data.get('initial_risk', 0.5)
        )
        
        print(f"Initial risk: {state.current_risk_score:.2f}")
        
        # Run investigation workflow
        state = agent.investigate(state)
        print(f"After investigation: risk={state.current_risk_score:.2f}")
        
        state = agent.gather_evidence(state)
        print(f"After evidence gathering: {len(state.evidence)} evidence items, confidence={state.confidence_score:.2f}")
        
        state = agent.assess_risk(state)
        print(f"After risk assessment: risk={state.current_risk_score:.2f}")
        
        # Check if we need more evidence
        state, needs_more = agent.assess_uncertainty(state)
        if needs_more:
            print(f"System requests additional evidence (confidence={state.confidence_score:.2f})")
            # Simulate customer response
            state = agent.receive_additional_evidence(
                state,
                "CUSTOMER_RESPONSE",
                {"response": case_data.get('customer_response', 'Transaction authorized')}
            )
            state, needs_more = agent.assess_uncertainty(state)
            print(f"After customer response: risk={state.current_risk_score:.2f}, needs_more={needs_more}")
        
        state = agent.recommend_action(state)
        
        # Get policy evaluation
        policy_eval = policy_engine.evaluate_action(
            case_id,
            state.current_risk_score,
            state.confidence_score
        )
        
        execution_time = time.time() - start_time
        
        # Determine if prediction matches ground truth
        ground_truth = case_data.get('label', 'UNKNOWN').upper()
        predicted_action = state.recommended_action.action_type.value if state.recommended_action else 'UNKNOWN'
        
        # Map actions to fraud/legitimate
        fraud_actions = ['BLOCK', 'ESCALATE', 'MANUAL_REVIEW']
        legitimate_actions = ['ALLOW', 'APPROVE']
        
        predicted_label = 'FRAUD' if predicted_action in fraud_actions else 'LEGITIMATE'
        ground_label = 'FRAUD' if ground_truth == 'FRAUD' else 'LEGITIMATE'
        
        accuracy = 1 if predicted_label == ground_label else 0
        
        print(f"Predicted: {predicted_label} ({predicted_action})")
        print(f"Ground truth: {ground_label}")
        print(f"Match: {'✓' if accuracy else '✗'}")
        print(f"Execution time: {execution_time:.2f}s")
        
        result = {
            'case_index': case_idx,
            'case_id': case_id,
            'customer_id': customer_id,
            'transaction_id': transaction_id,
            'ground_truth': ground_truth,
            'predicted_action': predicted_action,
            'predicted_label': predicted_label,
            'ground_label': ground_label,
            'accuracy': accuracy,
            'final_risk_score': round(state.current_risk_score, 3),
            'confidence_score': round(state.confidence_score, 3),
            'evidence_items': len(state.evidence),
            'fraud_pattern': state.suspected_fraud_pattern or 'None',
            'policy_compliant': policy_eval.get('compliant', False),
            'policy_rule': policy_eval.get('policy_rule', 'N/A'),
            'execution_time_seconds': round(execution_time, 2),
            'requires_approval': state.recommended_action.requires_approval if state.recommended_action else False,
        }
        
        return result
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        
        execution_time = time.time() - start_time
        return {
            'case_index': case_idx,
            'case_id': f"BENCH_{case_idx:02d}",
            'error': str(e),
            'execution_time_seconds': round(execution_time, 2),
            'accuracy': 0
        }

def evaluate_metrics(results):
    """Calculate evaluation metrics from results."""
    successful = [r for r in results if 'error' not in r]
    failed = [r for r in results if 'error' in r]
    
    if not successful:
        return {
            'total_cases': len(results),
            'successful': 0,
            'failed': len(failed),
            'metrics': {}
        }
    
    accuracies = [r['accuracy'] for r in successful]
    overall_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0
    
    fraud_cases = [r for r in successful if r['ground_label'] == 'FRAUD']
    legitimate_cases = [r for r in successful if r['ground_label'] == 'LEGITIMATE']
    
    fraud_accuracy = sum([r['accuracy'] for r in fraud_cases]) / len(fraud_cases) if fraud_cases else 0
    legitimate_accuracy = sum([r['accuracy'] for r in legitimate_cases]) / len(legitimate_cases) if legitimate_cases else 0
    
    avg_risk_score = sum([r['final_risk_score'] for r in successful]) / len(successful) if successful else 0
    avg_confidence = sum([r['confidence_score'] for r in successful]) / len(successful) if successful else 0
    avg_evidence_items = sum([r['evidence_items'] for r in successful]) / len(successful) if successful else 0
    avg_execution_time = sum([r['execution_time_seconds'] for r in results]) / len(results) if results else 0
    
    policy_compliant = sum([r['policy_compliant'] for r in successful if r.get('policy_compliant')])
    
    return {
        'total_cases': len(results),
        'successful': len(successful),
        'failed': len(failed),
        'metrics': {
            'overall_accuracy': round(overall_accuracy, 3),
            'fraud_detection_accuracy': round(fraud_accuracy, 3),
            'legitimate_approval_accuracy': round(legitimate_accuracy, 3),
            'fraud_cases_count': len(fraud_cases),
            'legitimate_cases_count': len(legitimate_cases),
            'average_risk_score': round(avg_risk_score, 3),
            'average_confidence_score': round(avg_confidence, 3),
            'average_evidence_items': round(avg_evidence_items, 2),
            'average_execution_time_seconds': round(avg_execution_time, 2),
            'policy_compliant_actions': policy_compliant
        }
    }

def run_benchmark():
    """Run the complete benchmark evaluation."""
    print("\n" + "="*60)
    print("TigerGraph Agentic Fraud Investigation - Benchmark Evaluation")
    print("="*60)
    
    cases = load_benchmark_cases()
    
    if not cases:
        print("ERROR: No benchmark cases found!")
        return
    
    print(f"\nLoaded {len(cases)} benchmark cases")
    print("Starting evaluation...")
    
    results = []
    for idx, case in enumerate(cases):
        result = run_benchmark_case(idx, case)
        results.append(result)
        # Small delay between cases
        time.sleep(0.1)
    
    # Calculate metrics
    metrics = evaluate_metrics(results)
    
    # Save results
    output = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_cases_run': len(results),
        'successful_cases': metrics['successful'],
        'failed_cases': metrics['failed'],
        'metrics': metrics['metrics'],
        'results': results
    }
    
    with open(RESULTS_OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "="*60)
    print("BENCHMARK EVALUATION COMPLETE")
    print("="*60)
    print(f"\nResults saved to: {RESULTS_OUTPUT_PATH}")
    print(f"\nMetrics Summary:")
    print(f"  Total cases: {metrics['total_cases']}")
    print(f"  Successful: {metrics['successful']}")
    print(f"  Failed: {metrics['failed']}")
    print(f"\nAccuracy Metrics:")
    print(f"  Overall accuracy: {metrics['metrics']['overall_accuracy']:.1%}")
    print(f"  Fraud detection: {metrics['metrics']['fraud_detection_accuracy']:.1%}")
    print(f"  Legitimate approval: {metrics['metrics']['legitimate_approval_accuracy']:.1%}")
    print(f"\nQuality Metrics:")
    print(f"  Avg risk score: {metrics['metrics']['average_risk_score']:.2f}")
    print(f"  Avg confidence: {metrics['metrics']['average_confidence_score']:.2f}")
    print(f"  Avg evidence items: {metrics['metrics']['average_evidence_items']:.1f}")
    print(f"  Avg execution time: {metrics['metrics']['average_execution_time_seconds']:.2f}s")
    print(f"  Policy compliant actions: {metrics['metrics']['policy_compliant_actions']}/{metrics['successful']}")

if __name__ == '__main__':
    run_benchmark()
