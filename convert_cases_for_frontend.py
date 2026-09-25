"""
Convert all 20 case JSON files into frontend-compatible format
"""
import json
import os
from pathlib import Path

def convert_cases():
    cases_dir = Path("cases")
    frontend_cases = []
    
    for i in range(1, 21):
        filename = f"HHG-{i:03d}.json"
        filepath = cases_dir / filename
        
        with open(filepath, 'r', encoding='utf-8') as f:
            case_data = json.load(f)
        
        # Convert to frontend format
        summary = case_data.get('investigation_summary', {})
        
        # Map fraud type to short title
        fraud_type = summary.get('primary_fraud_type', 'Unknown Fraud')
        
        # Determine status based on risk level and fraud detected
        fraud_detected = summary.get('fraud_detected', False)
        risk_level = summary.get('risk_level', 'MEDIUM')
        
        if not fraud_detected:
            status = 'LOW'
        elif risk_level == 'CRITICAL':
            status = 'CRITICAL'
        elif risk_level in ['HIGH', 'MEDIUM']:
            status = 'HIGH'
        else:
            status = 'MEDIUM'
        
        # Extract customer ID from evidence or use case ID
        customer = f"USR_{i:04d}"
        
        # Count transactions (estimate from evidence)
        transactions = len(case_data.get('key_findings', []))
        
        frontend_case = {
            'id': case_data['case_id'],
            'customer': customer,
            'title': fraud_type,
            'risk': summary.get('confidence_score', 50),
            'status': status,
            'amount': summary.get('estimated_loss', 0),
            'transactions': transactions,
            'time': f'{i * 2} hours ago',
            'findings': case_data.get('key_findings', []),
            'recommendations': case_data.get('recommendations', [])
        }
        
        frontend_cases.append(frontend_case)
    
    # Generate JavaScript code
    js_code = "const cases = " + json.dumps(frontend_cases, indent=2) + ";\n"
    
    print("=" * 60)
    print("Frontend Cases Data Generated!")
    print("=" * 60)
    print(f"\nTotal cases: {len(frontend_cases)}")
    print("\nCopy this to CasesPage.jsx:")
    print("=" * 60)
    print(js_code)
    
    # Also save to file
    with open("frontend_cases_data.js", "w", encoding="utf-8") as f:
        f.write(js_code)
    
    print("\n✅ Saved to: frontend_cases_data.js")
    print("\nCase summary:")
    for case in frontend_cases:
        print(f"  {case['id']}: {case['title'][:50]} - Risk: {case['risk']}%")

if __name__ == "__main__":
    convert_cases()
