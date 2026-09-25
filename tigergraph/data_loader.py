"""
Data Loader: Transforms CSV data into TigerGraph vertices and edges.
"""

import pandas as pd
import hashlib
from typing import Dict, List, Tuple, Set
from pathlib import Path
from datetime import datetime
import json


class TigerGraphDataLoader:
    """Loads and transforms data for TigerGraph."""
    
    def __init__(self):
        self.customers: Dict = {}
        self.accounts: Dict = {}
        self.transactions: Dict = {}
        self.devices: Dict = {}
        self.ips: Dict = {}
        self.merchants: Dict = {}
        self.fraud_cases: Dict = {}
        self.evidence_list: List = []
        self.actions_list: List = []
        
        # Edges
        self.owns_edges: List = []
        self.performs_edges: List = []
        self.uses_device_edges: List = []
        self.uses_ip_edges: List = []
        self.transaction_to_edges: List = []
        self.seen_in_transaction_edges: List = []
        self.investigates_edges: List = []
        self.matches_pattern_edges: List = []
        self.has_evidence_edges: List = []
        self.recommends_action_edges: List = []
    
    @staticmethod
    def hash_id(parts: List[str]) -> str:
        """Generate a deterministic hash ID."""
        combined = "_".join(str(p) for p in parts if p)
        return hashlib.md5(combined.encode()).hexdigest()[:16]
    
    def load_transactions(self, transactions_df: pd.DataFrame) -> Tuple[int, int, int]:
        """
        Load transactions and create Customer, Account, Transaction, Merchant vertices.
        
        Returns: (customer_count, account_count, transaction_count)
        """
        print("\n📥 Loading Transactions...")
        
        for idx, row in transactions_df.iterrows():
            customer_id = str(row["customer_id"]).strip()
            transaction_id = str(row["TransactionID"]).strip()
            
            # Create Customer
            if customer_id not in self.customers:
                self.customers[customer_id] = {
                    "customer_id": customer_id,
                    "email": None,
                    "phone": None,
                    "account_status": "ACTIVE",
                    "created_date": datetime.now().isoformat(),
                    "risk_profile": "NORMAL",
                    "fraud_history_count": 0
                }
            
            # Create Account (from card info)
            card1 = str(row.get("card1", "0"))
            card2 = str(row.get("card2", "0"))
            account_id = self.hash_id([customer_id, card1, card2])
            
            if account_id not in self.accounts:
                self.accounts[account_id] = {
                    "account_id": account_id,
                    "account_type": "CREDIT_CARD",
                    "card_last_4": card1[-4:] if len(card1) > 4 else card1,
                    "is_active": True,
                    "created_date": datetime.now().isoformat()
                }
            
            # Create Transaction
            self.transactions[transaction_id] = {
                "transaction_id": transaction_id,
                "customer_id": customer_id,
                "account_id": account_id,
                "amount": float(row.get("TransactionAmt", 0)),
                "currency": "USD",
                "product_code": str(row.get("ProductCD", "UNKNOWN")),
                "timestamp": str(row.get("TransactionDT", datetime.now().isoformat())),
                "status": "COMPLETED",
                "bank_risk_score": float(row.get("risk_score", 0.5)),
                "is_fraud": int(row.get("isFraud", 0))
            }
            
            # Create Merchant (derived from domain)
            merchant_domain = str(row.get("P_emaildomain", "unknown.com"))
            merchant_id = self.hash_id([merchant_domain, row.get("ProductCD", "UNKNOWN")])
            
            if merchant_id not in self.merchants:
                self.merchants[merchant_id] = {
                    "merchant_id": merchant_id,
                    "merchant_name": f"Merchant_{merchant_domain}",
                    "merchant_category": str(row.get("ProductCD", "UNKNOWN")),
                    "country": "UNKNOWN",
                    "risk_level": "NORMAL"
                }
            
            # Create Edges
            self.owns_edges.append({"from": customer_id, "to": account_id})
            self.performs_edges.append({"from": customer_id, "to": transaction_id})
            self.transaction_to_edges.append({"from": transaction_id, "to": merchant_id})
            
            if idx % 1000 == 0:
                print(f"  ✓ Processed {idx} transactions...")
        
        print(f"  ✓ Customers: {len(self.customers)}")
        print(f"  ✓ Accounts: {len(self.accounts)}")
        print(f"  ✓ Transactions: {len(self.transactions)}")
        
        return len(self.customers), len(self.accounts), len(self.transactions)
    
    def load_identity(self, identity_df: pd.DataFrame, transactions_df: pd.DataFrame) -> Tuple[int, int]:
        """
        Load device and IP information from identity data.
        
        Returns: (device_count, ip_count)
        """
        print("\n📱 Loading Identity/Device Data...")
        
        # Create transaction ID mapping for timestamp lookups
        tx_timestamps = {}
        for _, row in transactions_df.iterrows():
            tx_id = str(row["TransactionID"]).strip()
            tx_timestamps[tx_id] = str(row.get("TransactionDT", datetime.now().isoformat()))
        
        for idx, row in identity_df.iterrows():
            transaction_id = str(row["TransactionID"]).strip()
            customer_id = str(transactions_df.loc[
                transactions_df["TransactionID"].astype(str) == transaction_id,
                "customer_id"
            ].iloc[0]) if not transactions_df[
                transactions_df["TransactionID"].astype(str) == transaction_id
            ].empty else "UNKNOWN"
            
            # Create Device
            device_type_code = str(row.get("DeviceType", "1"))
            device_type_map = {"1": "DESKTOP", "2": "MOBILE", "3": "TABLET", "4": "UNKNOWN"}
            device_info = str(row.get("DeviceInfo", "UNKNOWN"))
            user_agent = str(row.get("user_agent", ""))
            
            device_id = self.hash_id([device_info, device_type_code, user_agent])
            
            if device_id not in self.devices:
                self.devices[device_id] = {
                    "device_id": device_id,
                    "device_type": device_type_map.get(device_type_code, "UNKNOWN"),
                    "device_os": str(row.get("DeviceOS", "UNKNOWN")),
                    "browser": str(row.get("browser", "UNKNOWN")),
                    "user_agent": user_agent,
                    "first_seen": tx_timestamps.get(transaction_id, datetime.now().isoformat()),
                    "last_seen": tx_timestamps.get(transaction_id, datetime.now().isoformat()),
                    "customer_count": 1
                }
            
            # Create IPAddress
            ip_address = str(row.get("IP_addr", "0.0.0.0"))
            
            if ip_address not in self.ips:
                self.ips[ip_address] = {
                    "ip_address": ip_address,
                    "country": "UNKNOWN",
                    "city": "UNKNOWN",
                    "latitude": None,
                    "longitude": None,
                    "isp": "UNKNOWN",
                    "first_seen": tx_timestamps.get(transaction_id, datetime.now().isoformat()),
                    "last_seen": tx_timestamps.get(transaction_id, datetime.now().isoformat()),
                    "customer_count": 1
                }
            
            # Create Edges
            if customer_id != "UNKNOWN" and customer_id in self.customers:
                self.uses_device_edges.append({"from": customer_id, "to": device_id})
                self.uses_ip_edges.append({"from": customer_id, "to": ip_address})
            
            self.seen_in_transaction_edges.append({"from": device_id, "to": ip_address})
            
            if idx % 1000 == 0:
                print(f"  ✓ Processed {idx} identity records...")
        
        print(f"  ✓ Devices: {len(self.devices)}")
        print(f"  ✓ IP Addresses: {len(self.ips)}")
        
        return len(self.devices), len(self.ips)
    
    def load_historical_cases(self, cases_df: pd.DataFrame) -> int:
        """Load historical fraud cases."""
        print("\n📋 Loading Historical Cases...")
        
        for idx, row in cases_df.iterrows():
            case_id = str(row.get("case_id", f"CASE_{idx}"))
            customer_id = str(row.get("customer_id", "UNKNOWN"))
            fraud_pattern = str(row.get("fraud_pattern", "UNKNOWN"))
            
            self.fraud_cases[case_id] = {
                "case_id": case_id,
                "customer_id": customer_id,
                "trigger_transaction_id": None,
                "trigger_type": "HISTORICAL",
                "case_status": "CLOSED",
                "initial_risk_score": float(row.get("initial_risk_score", 0.5)),
                "current_risk_score": float(row.get("final_risk_score", 0.5)),
                "confidence_score": 1.0,
                "fraud_pattern_detected": fraud_pattern,
                "created_timestamp": datetime.now().isoformat(),
                "updated_timestamp": str(row.get("closed_timestamp", datetime.now().isoformat())),
                "investigation_notes": str(row.get("outcome", "")),
                "approval_status": "APPROVED"
            }
            
            # Match to pattern
            self.matches_pattern_edges.append({
                "from": case_id,
                "to": fraud_pattern
            })
            
            # Create synthetic evidence
            evidence_count = int(row.get("evidence_count", 3))
            for i in range(evidence_count):
                evidence_id = f"{case_id}_evidence_{i}"
                self.evidence_list.append({
                    "evidence_id": evidence_id,
                    "case_id": case_id,
                    "evidence_type": "HISTORICAL",
                    "description": f"Historical case evidence {i+1}",
                    "confidence": 0.8,
                    "source_entity_id": None,
                    "source_entity_type": None,
                    "created_timestamp": datetime.now().isoformat()
                })
                self.has_evidence_edges.append({
                    "from": case_id,
                    "to": evidence_id
                })
            
            if idx % 100 == 0:
                print(f"  ✓ Processed {idx} historical cases...")
        
        print(f"  ✓ Historical Cases: {len(self.fraud_cases)}")
        
        return len(self.fraud_cases)
    
    def load_benchmark_cases(self, benchmark_df: pd.DataFrame) -> int:
        """Load benchmark cases for evaluation."""
        print("\n🎯 Loading Benchmark Cases...")
        
        for idx, row in benchmark_df.iterrows():
            case_id = str(row.get("case_id", f"BENCH_{idx}"))
            customer_id = str(row.get("customer_id", "UNKNOWN"))
            trigger_tx_id = str(row.get("flagged_txn_id", "UNKNOWN"))
            trigger_type = str(row.get("trigger_type", "HIGH_RISK"))
            fraud_pattern = str(row.get("expected_fraud_type", "UNKNOWN"))
            
            self.fraud_cases[case_id] = {
                "case_id": case_id,
                "customer_id": customer_id,
                "trigger_transaction_id": trigger_tx_id,
                "trigger_type": trigger_type,
                "case_status": "OPEN",
                "initial_risk_score": float(row.get("fraud_confidence", 0.5)),
                "current_risk_score": float(row.get("fraud_confidence", 0.5)),
                "confidence_score": 0.0,
                "fraud_pattern_detected": fraud_pattern,
                "created_timestamp": datetime.now().isoformat(),
                "updated_timestamp": datetime.now().isoformat(),
                "investigation_notes": "Benchmark case - under investigation",
                "approval_status": "PENDING"
            }
            
            # Link to transaction
            if trigger_tx_id in self.transactions:
                self.investigates_edges.append({
                    "from": case_id,
                    "to": trigger_tx_id
                })
            
            # Match to pattern
            self.matches_pattern_edges.append({
                "from": case_id,
                "to": fraud_pattern
            })
        
        print(f"  ✓ Benchmark Cases: {len(benchmark_df)}")
        
        return len(benchmark_df)
    
    def get_summary(self) -> Dict:
        """Return loading summary."""
        return {
            "vertices": {
                "customers": len(self.customers),
                "accounts": len(self.accounts),
                "transactions": len(self.transactions),
                "devices": len(self.devices),
                "ip_addresses": len(self.ips),
                "merchants": len(self.merchants),
                "fraud_cases": len(self.fraud_cases),
                "evidence": len(self.evidence_list),
                "actions": len(self.actions_list)
            },
            "edges": {
                "owns": len(self.owns_edges),
                "performs": len(self.performs_edges),
                "uses_device": len(self.uses_device_edges),
                "uses_ip": len(self.uses_ip_edges),
                "transaction_to": len(self.transaction_to_edges),
                "seen_in_transaction": len(self.seen_in_transaction_edges),
                "investigates": len(self.investigates_edges),
                "matches_pattern": len(self.matches_pattern_edges),
                "has_evidence": len(self.has_evidence_edges)
            }
        }
    
    def save_to_json(self, output_dir: Path):
        """Save all vertices and edges to JSON files for batch loading."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n💾 Saving to {output_dir}...")
        
        # Save vertices
        json.dump(self.customers, open(output_dir / "customers.json", "w"), indent=2)
        json.dump(self.accounts, open(output_dir / "accounts.json", "w"), indent=2)
        json.dump(self.transactions, open(output_dir / "transactions.json", "w"), indent=2)
        json.dump(self.devices, open(output_dir / "devices.json", "w"), indent=2)
        json.dump(self.ips, open(output_dir / "ip_addresses.json", "w"), indent=2)
        json.dump(self.merchants, open(output_dir / "merchants.json", "w"), indent=2)
        json.dump(self.fraud_cases, open(output_dir / "fraud_cases.json", "w"), indent=2)
        json.dump(self.evidence_list, open(output_dir / "evidence.json", "w"), indent=2)
        
        # Save edges
        json.dump(self.owns_edges, open(output_dir / "edges_owns.json", "w"), indent=2)
        json.dump(self.performs_edges, open(output_dir / "edges_performs.json", "w"), indent=2)
        json.dump(self.uses_device_edges, open(output_dir / "edges_uses_device.json", "w"), indent=2)
        json.dump(self.uses_ip_edges, open(output_dir / "edges_uses_ip.json", "w"), indent=2)
        json.dump(self.transaction_to_edges, open(output_dir / "edges_transaction_to.json", "w"), indent=2)
        json.dump(self.seen_in_transaction_edges, open(output_dir / "edges_seen_in_transaction.json", "w"), indent=2)
        json.dump(self.investigates_edges, open(output_dir / "edges_investigates.json", "w"), indent=2)
        json.dump(self.matches_pattern_edges, open(output_dir / "edges_matches_pattern.json", "w"), indent=2)
        json.dump(self.has_evidence_edges, open(output_dir / "edges_has_evidence.json", "w"), indent=2)
        
        print(f"✓ Data saved to {output_dir}")


def load_all_data(data_dir: Path = None, output_dir: Path = None) -> Dict:
    """Load all datasets and return summary."""
    if data_dir is None:
        data_dir = Path(r"C:\Users\ajayk\Downloads")
    if output_dir is None:
        output_dir = Path(r"c:\Users\ajayk\OneDrive\Documents\TigerGraph Agentic Fraud Investigation HHGOA\tigergraph\data")
    
    print("\n" + "="*70)
    print("LOADING DATA INTO TIGERGRAPH")
    print("="*70)
    
    # Load CSVs
    transactions_df = pd.read_csv(data_dir / "transactions.csv")
    identity_df = pd.read_csv(data_dir / "identity.csv")
    cases_df = pd.read_csv(data_dir / "closed_cases_history.csv")
    benchmark_df = pd.read_csv(data_dir / "case_pack.csv")
    
    # Create loader and load data
    loader = TigerGraphDataLoader()
    loader.load_transactions(transactions_df)
    loader.load_identity(identity_df, transactions_df)
    loader.load_historical_cases(cases_df)
    loader.load_benchmark_cases(benchmark_df)
    
    # Save results
    loader.save_to_json(output_dir)
    
    summary = loader.get_summary()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\n📊 Vertices Created:")
    for vtype, count in summary["vertices"].items():
        print(f"  {vtype:20s}: {count:6d}")
    
    print(f"\n🔗 Edges Created:")
    for etype, count in summary["edges"].items():
        print(f"  {etype:25s}: {count:6d}")
    
    print("\n" + "="*70 + "\n")
    
    return summary


if __name__ == "__main__":
    load_all_data()
