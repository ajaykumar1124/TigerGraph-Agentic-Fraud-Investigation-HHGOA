"""
TigerGraph Query Executor

Executes GSQL queries for fraud investigation.
When TigerGraph is not available, returns simulated/sample results.
"""

import json
from typing import Dict, List, Optional, Any
from pathlib import Path


class QueryExecutor:
    """Executes TigerGraph queries for the fraud investigation agent."""
    
    def __init__(self, use_simulation: bool = True):
        """Initialize query executor."""
        self.use_simulation = use_simulation
        self.sample_data_dir = Path(
            r"c:\Users\ajayk\OneDrive\Documents\TigerGraph Agentic Fraud Investigation HHGOA\tigergraph\data"
        )
        self.sample_data = self._load_sample_data()
    
    def _load_sample_data(self) -> Dict:
        """Load sample data from JSON files."""
        data = {}
        try:
            if self.sample_data_dir.exists():
                data = {
                    "customers": json.load(open(self.sample_data_dir / "customers.json")),
                    "transactions": json.load(open(self.sample_data_dir / "transactions.json")),
                    "devices": json.load(open(self.sample_data_dir / "devices.json")),
                    "ip_addresses": json.load(open(self.sample_data_dir / "ip_addresses.json")),
                    "merchants": json.load(open(self.sample_data_dir / "merchants.json")),
                    "fraud_cases": json.load(open(self.sample_data_dir / "fraud_cases.json")),
                    "evidence": json.load(open(self.sample_data_dir / "evidence.json")),
                }
        except Exception as e:
            print(f"⚠️  Could not load sample data: {e}")
        
        return data
    
    def find_shared_devices(self, customer_id: str, device_threshold: int = 1) -> Dict:
        """
        Find all customers who share a device with the given customer.
        
        Returns:
        {
          "shared_customers": [{"customer_id": "...", "shared_device_count": N, ...}],
          "devices_used": [...],
          "risk_level": "HIGH" | "MEDIUM" | "LOW"
        }
        """
        if self.use_simulation:
            return self._simulate_find_shared_devices(customer_id, device_threshold)
        
        # Would call actual TigerGraph query here
        return {}
    
    def _simulate_find_shared_devices(self, customer_id: str, device_threshold: int = 1) -> Dict:
        """Simulate finding shared devices using sample data."""
        result = {
            "customer_id": customer_id,
            "query": "find_shared_devices",
            "shared_customers": [],
            "devices_used": [],
            "risk_level": "LOW"
        }
        
        if not self.sample_data.get("devices"):
            return result
        
        # Find devices used by input customer
        devices_used = []
        for device_id, device in self.sample_data["devices"].items():
            if "customer_count" in device and device["customer_count"] > device_threshold:
                devices_used.append(device)
        
        result["devices_used"] = devices_used
        
        # Simulate shared customers
        if len(devices_used) > 0:
            shared_customers = []
            for i, device in enumerate(devices_used[:3]):  # Sample 3 devices
                shared_customers.append({
                    "customer_id": f"C{i:06d}",
                    "shared_device_count": len(devices_used),
                    "transaction_count": 5 + i,
                    "risk_score": 0.65 + (i * 0.1)
                })
            result["shared_customers"] = shared_customers
            result["risk_level"] = "HIGH" if len(shared_customers) > 2 else "MEDIUM"
        
        return result
    
    def find_shared_ips(self, customer_id: str, ip_threshold: int = 1) -> Dict:
        """
        Find all customers who share an IP address with the given customer.
        
        Returns:
        {
          "shared_customers": [{"customer_id": "...", "shared_ip_count": N, ...}],
          "ips_used": [...],
          "risk_level": "HIGH" | "MEDIUM" | "LOW"
        }
        """
        if self.use_simulation:
            return self._simulate_find_shared_ips(customer_id, ip_threshold)
        
        return {}
    
    def _simulate_find_shared_ips(self, customer_id: str, ip_threshold: int = 1) -> Dict:
        """Simulate finding shared IPs using sample data."""
        result = {
            "customer_id": customer_id,
            "query": "find_shared_ips",
            "shared_customers": [],
            "ips_used": [],
            "risk_level": "LOW"
        }
        
        if not self.sample_data.get("ip_addresses"):
            return result
        
        # Find IPs used by input customer
        ips_used = []
        ip_list = list(self.sample_data["ip_addresses"].values())[:5]
        ips_used = ip_list
        
        result["ips_used"] = ips_used
        
        # Simulate shared customers
        if len(ips_used) > 0:
            shared_customers = []
            for i, ip in enumerate(ips_used[:3]):
                shared_customers.append({
                    "customer_id": f"C{1000 + i:06d}",
                    "shared_ip_count": len(ips_used),
                    "ip_address": ip.get("ip_address", "Unknown"),
                    "risk_score": 0.60 + (i * 0.15)
                })
            result["shared_customers"] = shared_customers
            result["risk_level"] = "HIGH" if len(shared_customers) > 2 else "MEDIUM"
        
        return result
    
    def detect_transaction_velocity(self, customer_id: str, time_window_minutes: int = 60) -> Dict:
        """
        Detect transaction velocity anomalies.
        
        Returns:
        {
          "transaction_count": N,
          "total_amount": X.XX,
          "avg_transaction_amount": X.XX,
          "unique_merchants": N,
          "velocity_anomaly_score": 0.0-1.0,
          "risk_level": "HIGH" | "MEDIUM" | "LOW"
        }
        """
        if self.use_simulation:
            return self._simulate_detect_transaction_velocity(customer_id, time_window_minutes)
        
        return {}
    
    def _simulate_detect_transaction_velocity(self, customer_id: str, time_window_minutes: int = 60) -> Dict:
        """Simulate detecting velocity anomalies."""
        import random
        random.seed(hash(customer_id) % 2**32)
        
        tx_count = random.randint(1, 15)
        total_amount = random.uniform(100, 50000)
        avg_amount = total_amount / tx_count if tx_count > 0 else 0
        max_amount = max(random.uniform(1000, 15000), avg_amount)
        unique_merchants = random.randint(1, 8)
        
        # Calculate anomaly score
        velocity_score = 0
        if tx_count > 10:
            velocity_score += 0.3
        if avg_amount > 500:
            velocity_score += 0.2
        if unique_merchants > 5:
            velocity_score += 0.3
        if max_amount > 10000:
            velocity_score += 0.2
        
        velocity_score = min(velocity_score, 1.0)
        
        risk_level = "HIGH" if velocity_score > 0.7 else "MEDIUM" if velocity_score > 0.4 else "LOW"
        
        return {
            "customer_id": customer_id,
            "query": "detect_transaction_velocity",
            "time_window_minutes": time_window_minutes,
            "transaction_count": tx_count,
            "total_amount": round(total_amount, 2),
            "avg_transaction_amount": round(avg_amount, 2),
            "max_transaction_amount": round(max_amount, 2),
            "unique_merchants": unique_merchants,
            "velocity_anomaly_score": round(velocity_score, 2),
            "risk_level": risk_level
        }
    
    def find_fraud_network(self, customer_id: str, max_hops: int = 2) -> Dict:
        """
        Find fraud network around the given customer.
        
        Returns:
        {
          "network_size": N,
          "high_risk_nodes": [...],
          "network_risk_score": 0.0-1.0
        }
        """
        if self.use_simulation:
            return self._simulate_find_fraud_network(customer_id, max_hops)
        
        return {}
    
    def _simulate_find_fraud_network(self, customer_id: str, max_hops: int = 2) -> Dict:
        """Simulate finding fraud network."""
        import random
        random.seed(hash(customer_id) % 2**32)
        
        network_size = random.randint(3, 20)
        high_risk_count = random.randint(1, 5)
        
        high_risk_nodes = []
        for i in range(high_risk_count):
            high_risk_nodes.append({
                "customer_id": f"NETWORK_{i:03d}",
                "centrality": random.randint(10, 100),
                "risk_rank": random.choice(["CRITICAL", "HIGH", "MEDIUM"])
            })
        
        network_risk_score = min(0.5 + (high_risk_count * 0.15), 1.0)
        
        return {
            "customer_id": customer_id,
            "query": "find_fraud_network",
            "network_size": network_size,
            "hops": max_hops,
            "high_risk_nodes": high_risk_nodes,
            "network_risk_score": round(network_risk_score, 2),
            "risk_level": "CRITICAL" if network_risk_score > 0.8 else "HIGH" if network_risk_score > 0.6 else "MEDIUM"
        }
    
    def find_similar_historical_cases(
        self,
        fraud_pattern: str,
        min_risk: float = 0.5,
        max_risk: float = 1.0,
        limit: int = 5
    ) -> Dict:
        """
        Find similar historical fraud cases.
        
        Returns:
        {
          "similar_cases": [
            {"case_id": "...", "pattern": "...", "outcome": "...", "similarity": 0.8}
          ],
          "recommended_actions": [...]
        }
        """
        if self.use_simulation:
            return self._simulate_find_similar_historical_cases(fraud_pattern, min_risk, max_risk, limit)
        
        return {}
    
    def _simulate_find_similar_historical_cases(
        self,
        fraud_pattern: str,
        min_risk: float = 0.5,
        max_risk: float = 1.0,
        limit: int = 5
    ) -> Dict:
        """Simulate finding similar historical cases."""
        similar_cases = []
        
        fraud_patterns = [
            "ACCOUNT_TAKEOVER",
            "PAYMENT_FRAUD",
            "CARD_FRAUD",
            "FRAUD_NETWORK",
            "VELOCITY_ANOMALY"
        ]
        
        outcomes = ["CONFIRMED_FRAUD", "FALSE_POSITIVE", "PENDING"]
        actions = ["BLOCK_ACCOUNT", "HOLD_TRANSACTION", "REQUEST_AUTH", "ESCALATE", "ALLOW"]
        
        for i in range(min(limit, 5)):
            similar_cases.append({
                "case_id": f"CASE{100000 + i:06d}",
                "pattern": fraud_pattern,
                "initial_risk": min_risk + (i * 0.1),
                "final_risk": max_risk - (i * 0.05),
                "outcome": outcomes[i % len(outcomes)],
                "recommended_action": actions[i % len(actions)],
                "similarity": round(1.0 - (i * 0.15), 2),
                "evidence_count": 3 + i
            })
        
        return {
            "query": "find_similar_historical_cases",
            "fraud_pattern": fraud_pattern,
            "similar_cases": similar_cases,
            "recommended_actions": [c["recommended_action"] for c in similar_cases]
        }
    
    def get_investigation_context(self, case_id: str) -> Dict:
        """
        Get complete investigation context for a case.
        
        Returns:
        {
          "case_details": {...},
          "transactions": [...],
          "customers": [...],
          "devices": [...],
          "ips": [...],
          "merchants": [...],
          "patterns": [...],
          "evidence": [...],
          "actions": [...],
          "related_cases": [...]
        }
        """
        if self.use_simulation:
            return self._simulate_get_investigation_context(case_id)
        
        return {}
    
    def _simulate_get_investigation_context(self, case_id: str) -> Dict:
        """Simulate getting investigation context."""
        return {
            "case_id": case_id,
            "query": "get_investigation_context",
            "case_details": {
                "case_id": case_id,
                "customer_id": "C000001",
                "case_status": "OPEN",
                "trigger_type": "HIGH_RISK",
                "fraud_pattern": "ACCOUNT_TAKEOVER",
                "approval_status": "PENDING"
            },
            "transactions": [
                {
                    "transaction_id": f"TX{i:08d}",
                    "amount": 1000 + (i * 100),
                    "timestamp": "2024-09-23T10:00:00",
                    "risk_score": 0.7 + (i * 0.05)
                }
                for i in range(3)
            ],
            "customers": [{"customer_id": "C000001"}],
            "devices": [{"device_id": "D001", "device_type": "MOBILE"}],
            "ips": [{"ip_address": "192.168.1.1"}],
            "merchants": [{"merchant_id": "M001", "merchant_name": "Merchant A"}],
            "patterns": [{"pattern_id": "ACCOUNT_TAKEOVER", "pattern_name": "Account Takeover"}],
            "evidence": [
                {"evidence_id": "E001", "evidence_type": "SHARED_DEVICE", "confidence": 0.9}
            ],
            "actions": [
                {"action_id": "A001", "action_type": "REQUEST_AUTH", "status": "RECOMMENDED"}
            ],
            "related_cases": [{"case_id": "CASE000001"}]
        }


def print_query_executor_info():
    """Print query executor information."""
    executor = QueryExecutor()
    
    print("\n" + "="*70)
    print("TIGERGRAPH QUERY EXECUTOR")
    print("="*70)
    
    print("\n📋 Available Queries:")
    print("  1. find_shared_devices(customer_id, device_threshold)")
    print("     → Find customers sharing devices")
    print("  2. find_shared_ips(customer_id, ip_threshold)")
    print("     → Find customers sharing IP addresses")
    print("  3. detect_transaction_velocity(customer_id, time_window_minutes)")
    print("     → Detect unusual transaction patterns")
    print("  4. find_fraud_network(customer_id, max_hops)")
    print("     → Find connected fraud networks")
    print("  5. find_similar_historical_cases(fraud_pattern, min_risk, max_risk)")
    print("     → Find similar past cases")
    print("  6. get_investigation_context(case_id)")
    print("     → Get complete case context")
    
    print("\n🔧 Mode: SIMULATION (TigerGraph not connected)")
    print("   In production, queries execute against live TigerGraph instance")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print_query_executor_info()
    
    # Test one query
    executor = QueryExecutor()
    result = executor.detect_transaction_velocity("C000001")
    print("\n📊 Sample Query Result: detect_transaction_velocity")
    print(json.dumps(result, indent=2))
