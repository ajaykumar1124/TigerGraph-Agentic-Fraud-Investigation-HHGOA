"""
Synthetic Dataset Generator for HHGOA Fraud Investigation
Generates realistic synthetic data matching the expected schema.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import random
import string


def generate_transactions(num_records=10000, output_dir=None):
    """Generate synthetic transaction dataset."""
    np.random.seed(42)
    random.seed(42)
    
    customer_ids = [f"C{i:06d}" for i in range(1, 500)]
    transaction_ids = [f"TX{i:08d}" for i in range(1, num_records + 1)]
    
    base_date = datetime(2024, 1, 1)
    timestamps = [base_date + timedelta(hours=int(i * 0.5)) for i in range(num_records)]
    
    merchants = [f"MERCHANT_{i}" for i in range(1, 100)]
    
    data = {
        "TransactionID": transaction_ids,
        "customer_id": np.random.choice(customer_ids, num_records),
        "TransactionDT": timestamps,
        "TransactionAmt": np.random.lognormal(mean=5.5, sigma=1.5, size=num_records),
        "ProductCD": np.random.choice(["W", "H", "S", "C"], num_records),
        "card1": np.random.randint(10000, 50000, num_records),
        "card2": np.random.randint(100, 600, num_records),
        "card3": np.random.randint(100, 600, num_records),
        "card4": np.random.randint(1000, 5000, num_records),
        "card5": np.random.randint(100, 600, num_records),
        "card6": np.random.choice(["credit", "debit"], num_records),
        "addr1": np.random.randint(100000, 700000, num_records),
        "addr2": np.random.randint(100, 900, num_records),
        "dist1": np.random.exponential(200, num_records),
        "dist2": np.random.exponential(20, num_records),
        "P_emaildomain": np.random.choice(["gmail.com", "yahoo.com", "outlook.com", "bank.com"], num_records),
        "R_emaildomain": np.random.choice(["gmail.com", "yahoo.com", "outlook.com", "bank.com"], num_records),
        "C1": np.random.randint(0, 200, num_records),
        "C2": np.random.randint(0, 200, num_records),
        "C3": np.random.randint(0, 200, num_records),
        "C4": np.random.randint(0, 200, num_records),
        "C5": np.random.randint(0, 200, num_records),
        "C6": np.random.randint(0, 200, num_records),
        "C7": np.random.randint(0, 200, num_records),
        "C8": np.random.randint(0, 200, num_records),
        "C9": np.random.randint(0, 200, num_records),
        "C10": np.random.randint(0, 200, num_records),
        "C11": np.random.randint(0, 200, num_records),
        "C12": np.random.randint(0, 200, num_records),
        "C13": np.random.randint(0, 200, num_records),
        "C14": np.random.randint(0, 200, num_records),
        "D1": np.random.randint(0, 500, num_records),
        "D2": np.random.randint(0, 500, num_records),
        "D3": np.random.randint(0, 500, num_records),
        "D4": np.random.randint(0, 500, num_records),
        "D5": np.random.randint(0, 500, num_records),
        "D6": np.random.randint(0, 500, num_records),
        "D7": np.random.randint(0, 500, num_records),
        "D8": np.random.randint(0, 500, num_records),
        "D9": np.random.randint(0, 500, num_records),
        "D10": np.random.randint(0, 500, num_records),
        "D11": np.random.randint(0, 500, num_records),
        "D12": np.random.randint(0, 500, num_records),
        "D13": np.random.randint(0, 500, num_records),
        "D14": np.random.randint(0, 500, num_records),
        "D15": np.random.randint(0, 500, num_records),
        "M1": np.random.choice(["T", "F"], num_records),
        "M2": np.random.choice(["T", "F"], num_records),
        "M3": np.random.choice(["T", "F"], num_records),
        "M4": np.random.choice(["T", "F"], num_records),
        "M5": np.random.choice(["T", "F"], num_records),
        "M6": np.random.choice(["T", "F"], num_records),
        "M7": np.random.choice(["T", "F"], num_records),
        "M8": np.random.choice(["T", "F"], num_records),
        "M9": np.random.choice(["T", "F"], num_records),
        "isFraud": np.random.choice([0, 1], num_records, p=[0.965, 0.035]),
        "risk_score": np.random.uniform(0, 1, num_records),
    }
    
    df = pd.DataFrame(data)
    
    if output_dir:
        output_path = Path(output_dir) / "transactions.csv"
        df.to_csv(output_path, index=False)
        print(f"✓ Generated transactions.csv: {output_path}")
    
    return df


def generate_identity(num_records=8000, output_dir=None):
    """Generate synthetic identity/device dataset."""
    np.random.seed(42)
    random.seed(42)
    
    transaction_ids = [f"TX{i:08d}" for i in range(1, num_records + 1)]
    
    # Device features
    device_info = [
    f"DeviceType_{np.random.choice(['Mobile', 'Desktop', 'Tablet'])}_OS_{np.random.choice(['iOS', 'Android', 'Windows', 'Mac'])}"
        for _ in range(num_records)
    ]
    
    ip_addrs = [f"{np.random.randint(1,255)}.{np.random.randint(0,255)}.{np.random.randint(0,255)}.{np.random.randint(1,255)}" 
                for _ in range(num_records)]
    
    data = {
        "TransactionID": transaction_ids,
        "DeviceInfo": device_info,
        "DeviceType": np.random.choice(["1", "2", "3", "4"], num_records),
        "DeviceOS": np.random.choice(["Windows", "iOS", "Android", "Mac"], num_records),
        "browser": np.random.choice(["Chrome", "Safari", "Firefox", "Edge"], num_records),
        "IP_addr": ip_addrs,
        "id_01": np.random.randint(1, 300, num_records),
        "id_02": np.random.randint(1, 300, num_records),
        "id_03": np.random.randint(1, 300, num_records),
        "id_04": np.random.randint(1, 300, num_records),
        "id_05": np.random.randint(1, 300, num_records),
        "id_06": np.random.randint(1, 300, num_records),
        "id_07": np.random.randint(1, 300, num_records),
        "id_08": np.random.randint(1, 300, num_records),
        "id_09": np.random.randint(1, 300, num_records),
        "id_10": np.random.randint(1, 300, num_records),
        "id_11": np.random.choice(["F", "M", "U"], num_records),
        "id_12": np.random.randint(0, 150, num_records),
        "id_13": np.random.choice(["T", "F"], num_records),
        "id_14": np.random.randint(0, 10, num_records),
        "id_15": np.random.randint(0, 500, num_records),
        "id_16": np.random.randint(0, 500, num_records),
        "id_17": np.random.randint(0, 500, num_records),
        "id_18": np.random.randint(0, 500, num_records),
        "id_19": np.random.randint(0, 500, num_records),
        "id_20": np.random.randint(0, 500, num_records),
        "id_21": np.random.randint(0, 500, num_records),
        "id_22": np.random.randint(0, 500, num_records),
        "id_23": np.random.randint(0, 500, num_records),
        "id_24": np.random.randint(0, 500, num_records),
        "id_25": np.random.randint(0, 500, num_records),
        "id_26": np.random.randint(0, 500, num_records),
        "id_27": np.random.randint(0, 500, num_records),
        "id_28": np.random.randint(0, 500, num_records),
        "id_29": np.random.randint(0, 500, num_records),
        "id_30": np.random.randint(0, 500, num_records),
        "id_31": np.random.randint(0, 500, num_records),
    }
    
    df = pd.DataFrame(data)
    
    if output_dir:
        output_path = Path(output_dir) / "identity.csv"
        df.to_csv(output_path, index=False)
        print(f"✓ Generated identity.csv: {output_path}")
    
    return df


def generate_closed_cases_history(num_cases=500, output_dir=None):
    """Generate synthetic closed investigation history."""
    np.random.seed(42)
    random.seed(42)
    
    fraud_patterns = ["ACCOUNT_TAKEOVER", "PAYMENT_FRAUD", "CARD_FRAUD", "FRAUD_NETWORK", "VELOCITY_ANOMALY"]
    actions = ["BLOCK_ACCOUNT", "HOLD_TRANSACTION", "REQUEST_AUTH", "ESCALATE", "ALLOW"]
    
    base_date = datetime(2023, 1, 1)
    
    data = {
        "case_id": [f"CASE{i:06d}" for i in range(1, num_cases + 1)],
        "customer_id": [f"C{i%400:06d}" for i in range(1, num_cases + 1)],
        "fraud_pattern": np.random.choice(fraud_patterns, num_cases),
        "initial_risk_score": np.random.uniform(0.5, 1.0, num_cases),
        "final_risk_score": np.random.uniform(0.4, 1.0, num_cases),
        "evidence_count": np.random.randint(2, 10, num_cases),
        "investigation_duration_hours": np.random.randint(1, 72, num_cases),
        "action_taken": np.random.choice(actions, num_cases),
        "approved_by": [f"ANALYST_{i%20:02d}" for i in range(num_cases)],
        "outcome": np.random.choice(["CONFIRMED_FRAUD", "FALSE_POSITIVE", "PENDING"], num_cases),
        "closed_timestamp": [base_date + timedelta(days=i, hours=np.random.randint(0, 24)) for i in range(num_cases)],
    }
    
    df = pd.DataFrame(data)
    
    if output_dir:
        output_path = Path(output_dir) / "closed_cases_history.csv"
        df.to_csv(output_path, index=False)
        print(f"✓ Generated closed_cases_history.csv: {output_path}")
    
    return df


def generate_case_pack(num_benchmark_cases=20, output_dir=None):
    """Generate benchmark cases for evaluation."""
    np.random.seed(42)
    random.seed(42)
    
    data = {
        "case_id": [f"BENCH_{i:03d}" for i in range(1, num_benchmark_cases + 1)],
        "flagged_txn_id": [f"TX{100000 + i:06d}" for i in range(1, num_benchmark_cases + 1)],
        "customer_id": [f"C{i%400:06d}" for i in range(1, num_benchmark_cases + 1)],
        "trigger_type": np.random.choice(["HIGH_RISK", "VELOCITY", "NETWORK", "PATTERN"], num_benchmark_cases),
        "expected_fraud_type": np.random.choice(
            ["ACCOUNT_TAKEOVER", "PAYMENT_FRAUD", "CARD_FRAUD", "FRAUD_NETWORK"], 
            num_benchmark_cases
        ),
        "fraud_confidence": np.random.uniform(0.0, 1.0, num_benchmark_cases),
        "benchmark_notes": [f"Benchmark case {i}" for i in range(1, num_benchmark_cases + 1)],
    }
    
    df = pd.DataFrame(data)
    
    if output_dir:
        output_path = Path(output_dir) / "case_pack.csv"
        df.to_csv(output_path, index=False)
        print(f"✓ Generated case_pack.csv: {output_path}")
    
    return df


def generate_all_synthetic_data(output_dir=None, transactions_count=10000, cases_count=500, benchmark_cases=20):
    """Generate all synthetic datasets."""
    if output_dir is None:
        output_dir = Path(r"C:\Users\ajayk\Downloads")
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n🔄 Generating synthetic HHGOA dataset...\n")
    
    generate_transactions(num_records=transactions_count, output_dir=output_dir)
    generate_identity(num_records=transactions_count, output_dir=output_dir)
    generate_closed_cases_history(num_cases=cases_count, output_dir=output_dir)
    generate_case_pack(num_benchmark_cases=benchmark_cases, output_dir=output_dir)
    
    print("\n✅ Synthetic dataset generation complete!")
    print(f"📁 Dataset saved to: {output_dir}")
    
    return {
        "transactions": output_dir / "transactions.csv",
        "identity": output_dir / "identity.csv",
        "closed_cases_history": output_dir / "closed_cases_history.csv",
        "case_pack": output_dir / "case_pack.csv",
    }


if __name__ == "__main__":
    generate_all_synthetic_data()
