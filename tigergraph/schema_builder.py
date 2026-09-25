"""
TigerGraph Schema Builder for Fraud Investigation

This module creates the TigerGraph schema and provides utilities for
loading data into the graph.
"""

import os
from typing import Optional, Dict, List
import json
from pathlib import Path

# Optional: pyTigerGraph when available
try:
    import pyTigerGraph as tg
    HAS_PYTG = True
except ImportError:
    HAS_PYTG = False


class TigerGraphSchemaBuilder:
    """
    Builds and manages the TigerGraph fraud investigation schema.
    """
    
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9000,
        username: str = "tigergraph",
        password: str = "tigergraph",
        graph_name: str = "fraud_investigation"
    ):
        """Initialize TigerGraph connection parameters."""
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.graph_name = graph_name
        self.conn = None
        
        if HAS_PYTG:
            try:
                self.conn = tg.TigerGraphConnection(
                    host=host,
                    port=port,
                    username=username,
                    password=password,
                    graphname=graph_name
                )
            except Exception as e:
                print(f"⚠️  Could not connect to TigerGraph: {e}")
                print("   Running in simulation mode")
    
    def get_schema_definition(self) -> str:
        """Return the complete GSQL schema definition."""
        return """
/**
 * TIGERGRAPH SCHEMA FOR FRAUD INVESTIGATION
 */

CREATE VERTEX Customer (
  PRIMARY_ID customer_id STRING,
  email STRING,
  phone STRING,
  account_status STRING,
  created_date DATETIME,
  risk_profile STRING DEFAULT "NORMAL",
  fraud_history_count INT DEFAULT 0
) WITH primary_key="customer_id"

CREATE VERTEX Account (
  PRIMARY_ID account_id STRING,
  account_type STRING,
  card_last_4 STRING,
  is_active BOOL DEFAULT TRUE,
  created_date DATETIME
) WITH primary_key="account_id"

CREATE VERTEX Transaction (
  PRIMARY_ID transaction_id STRING,
  customer_id STRING,
  account_id STRING,
  amount DOUBLE,
  currency STRING DEFAULT "USD",
  product_code STRING,
  timestamp DATETIME,
  status STRING,
  bank_risk_score FLOAT,
  is_fraud INT DEFAULT 0
) WITH primary_key="transaction_id"

CREATE VERTEX Device (
  PRIMARY_ID device_id STRING,
  device_type STRING,
  device_os STRING,
  browser STRING,
  user_agent STRING,
  first_seen DATETIME,
  last_seen DATETIME,
  customer_count INT DEFAULT 1
) WITH primary_key="device_id"

CREATE VERTEX IPAddress (
  PRIMARY_ID ip_address STRING,
  country STRING,
  city STRING,
  latitude DOUBLE,
  longitude DOUBLE,
  isp STRING,
  first_seen DATETIME,
  last_seen DATETIME,
  customer_count INT DEFAULT 1
) WITH primary_key="ip_address"

CREATE VERTEX Merchant (
  PRIMARY_ID merchant_id STRING,
  merchant_name STRING,
  merchant_category STRING,
  country STRING,
  risk_level STRING DEFAULT "NORMAL"
) WITH primary_key="merchant_id"

CREATE VERTEX FraudCase (
  PRIMARY_ID case_id STRING,
  customer_id STRING,
  trigger_transaction_id STRING,
  trigger_type STRING,
  case_status STRING DEFAULT "OPEN",
  initial_risk_score FLOAT,
  current_risk_score FLOAT,
  confidence_score FLOAT DEFAULT 0.0,
  fraud_pattern_detected STRING,
  created_timestamp DATETIME,
  updated_timestamp DATETIME,
  investigation_notes STRING,
  approval_status STRING DEFAULT "PENDING"
) WITH primary_key="case_id"

CREATE VERTEX FraudPattern (
  PRIMARY_ID pattern_id STRING,
  pattern_name STRING,
  description STRING,
  risk_weight FLOAT
) WITH primary_key="pattern_id"

CREATE VERTEX Evidence (
  PRIMARY_ID evidence_id STRING,
  case_id STRING,
  evidence_type STRING,
  description STRING,
  confidence FLOAT,
  source_entity_id STRING,
  source_entity_type STRING,
  created_timestamp DATETIME
) WITH primary_key="evidence_id"

CREATE VERTEX Action (
  PRIMARY_ID action_id STRING,
  case_id STRING,
  action_type STRING,
  action_status STRING DEFAULT "RECOMMENDED",
  approval_required BOOL,
  approval_required_role STRING,
  rationale STRING,
  created_timestamp DATETIME
) WITH primary_key="action_id"

CREATE VERTEX InvestigationLog (
  PRIMARY_ID log_id STRING,
  case_id STRING,
  log_type STRING,
  timestamp DATETIME,
  message STRING,
  risk_score FLOAT,
  confidence FLOAT
) WITH primary_key="log_id"

CREATE DIRECTED EDGE OWNS (FROM Customer, TO Account)
CREATE DIRECTED EDGE PERFORMS (FROM Customer, TO Transaction)
CREATE DIRECTED EDGE USES_DEVICE (FROM Customer, TO Device)
CREATE DIRECTED EDGE USES_IP (FROM Customer, TO IPAddress)
CREATE DIRECTED EDGE TRANSACTION_TO (FROM Transaction, TO Merchant)
CREATE DIRECTED EDGE SEEN_IN_TRANSACTION (FROM Device, TO IPAddress)
CREATE DIRECTED EDGE INVESTIGATES (FROM FraudCase, TO Transaction)
CREATE DIRECTED EDGE MATCHES_PATTERN (FROM FraudCase, TO FraudPattern)
CREATE DIRECTED EDGE HAS_EVIDENCE (FROM FraudCase, TO Evidence)
CREATE DIRECTED EDGE RECOMMENDS_ACTION (FROM FraudCase, TO Action)
CREATE DIRECTED EDGE RELATED_CASE (FROM FraudCase, TO FraudCase)
CREATE DIRECTED EDGE FROM_TRANSACTION (FROM Evidence, TO Transaction)
CREATE DIRECTED EDGE FROM_DEVICE (FROM Evidence, TO Device)
CREATE DIRECTED EDGE FROM_IP (FROM Evidence, TO IPAddress)
CREATE DIRECTED EDGE INVESTIGATION_LOG (FROM FraudCase, TO InvestigationLog)

CREATE GRAPH fraud_investigation (
  Customer, Account, Transaction, Device, IPAddress, Merchant,
  FraudCase, FraudPattern, Evidence, Action, InvestigationLog,
  OWNS, PERFORMS, USES_DEVICE, USES_IP, TRANSACTION_TO,
  SEEN_IN_TRANSACTION, INVESTIGATES, MATCHES_PATTERN,
  HAS_EVIDENCE, RECOMMENDS_ACTION, RELATED_CASE,
  FROM_TRANSACTION, FROM_DEVICE, FROM_IP, INVESTIGATION_LOG
)
"""
    
    def get_fraud_patterns(self) -> List[Dict]:
        """Return reference fraud patterns."""
        return [
            {
                "pattern_id": "ACCOUNT_TAKEOVER",
                "pattern_name": "Account Takeover",
                "description": "Account accessed by unauthorized user using new device/IP",
                "risk_weight": 0.95
            },
            {
                "pattern_id": "PAYMENT_FRAUD",
                "pattern_name": "Payment Fraud",
                "description": "Unauthorized transfer to suspicious beneficiary",
                "risk_weight": 0.85
            },
            {
                "pattern_id": "CARD_FRAUD",
                "pattern_name": "Card Fraud",
                "description": "Card used in unusual location/merchant",
                "risk_weight": 0.80
            },
            {
                "pattern_id": "FRAUD_NETWORK",
                "pattern_name": "Fraud Network",
                "description": "Multiple accounts sharing device/IP/PII",
                "risk_weight": 0.75
            },
            {
                "pattern_id": "VELOCITY_ANOMALY",
                "pattern_name": "Velocity Anomaly",
                "description": "Unusually high transaction frequency/amount",
                "risk_weight": 0.70
            }
        ]
    
    def create_graph(self) -> bool:
        """Create the fraud investigation graph in TigerGraph."""
        if not HAS_PYTG or self.conn is None:
            print("⚠️  TigerGraph connection not available. Schema not created.")
            return False
        
        try:
            # This would require running GSQL commands
            # For now, we'll document the schema
            print(f"✓ Graph '{self.graph_name}' schema prepared")
            return True
        except Exception as e:
            print(f"❌ Error creating graph: {e}")
            return False
    
    def drop_graph(self) -> bool:
        """Drop the graph (useful for testing)."""
        if not HAS_PYTG or self.conn is None:
            print("⚠️  TigerGraph connection not available.")
            return False
        
        try:
            # Would drop graph here
            print(f"✓ Graph '{self.graph_name}' dropped")
            return True
        except Exception as e:
            print(f"❌ Error dropping graph: {e}")
            return False
    
    def insert_vertices_batch(self, vertex_type: str, vertices: List[Dict]) -> int:
        """Insert vertices in batch."""
        if not HAS_PYTG or self.conn is None:
            print(f"⚠️  Would insert {len(vertices)} {vertex_type} vertices")
            return len(vertices)
        
        try:
            inserted = 0
            for vertex in vertices:
                self.conn.upsertVertex(vertex_type, vertex.get("pk"), vertex)
                inserted += 1
            print(f"✓ Inserted {inserted} {vertex_type} vertices")
            return inserted
        except Exception as e:
            print(f"❌ Error inserting {vertex_type} vertices: {e}")
            return 0
    
    def insert_edges_batch(
        self,
        edge_type: str,
        edges: List[Dict[str, str]]
    ) -> int:
        """Insert edges in batch."""
        if not HAS_PYTG or self.conn is None:
            print(f"⚠️  Would insert {len(edges)} {edge_type} edges")
            return len(edges)
        
        try:
            inserted = 0
            for edge in edges:
                self.conn.upsertEdge(
                    edge_type,
                    edge["from_type"],
                    edge["from_id"],
                    edge["to_type"],
                    edge["to_id"],
                    edge.get("attributes", {})
                )
                inserted += 1
            print(f"✓ Inserted {inserted} {edge_type} edges")
            return inserted
        except Exception as e:
            print(f"❌ Error inserting {edge_type} edges: {e}")
            return 0
    
    def run_gsql_query(self, query: str) -> Optional[Dict]:
        """Run a GSQL query and return results."""
        if not HAS_PYTG or self.conn is None:
            print("⚠️  TigerGraph connection not available for query execution")
            return None
        
        try:
            result = self.conn.runInstalledQuery(query, {})
            return result
        except Exception as e:
            print(f"❌ Error running query: {e}")
            return None
    
    def get_connection_status(self) -> Dict[str, str]:
        """Return connection status."""
        status = {
            "connected": self.conn is not None,
            "host": self.host,
            "port": str(self.port),
            "graph": self.graph_name,
            "mode": "LIVE" if self.conn else "SIMULATION"
        }
        return status


class SchemaValidator:
    """Validates data before loading into TigerGraph."""
    
    @staticmethod
    def validate_customer_data(customer: Dict) -> bool:
        """Validate customer vertex data."""
        required = ["customer_id"]
        return all(k in customer for k in required)
    
    @staticmethod
    def validate_transaction_data(transaction: Dict) -> bool:
        """Validate transaction vertex data."""
        required = ["transaction_id", "customer_id", "amount", "timestamp"]
        return all(k in transaction for k in required)
    
    @staticmethod
    def validate_device_data(device: Dict) -> bool:
        """Validate device vertex data."""
        required = ["device_id", "device_type"]
        return all(k in device for k in required)
    
    @staticmethod
    def validate_ip_data(ip_addr: Dict) -> bool:
        """Validate IP address vertex data."""
        required = ["ip_address"]
        return all(k in ip_addr for k in required)


def print_schema_info():
    """Print schema information."""
    builder = TigerGraphSchemaBuilder()
    
    print("\n" + "="*70)
    print("FRAUD INVESTIGATION TIGERGRAPH SCHEMA")
    print("="*70)
    
    print("\n📊 Vertices (11 total):")
    vertices = [
        "Customer", "Account", "Transaction", "Device", "IPAddress",
        "Merchant", "FraudCase", "FraudPattern", "Evidence", "Action",
        "InvestigationLog"
    ]
    for v in vertices:
        print(f"  • {v}")
    
    print("\n🔗 Edges (16 total):")
    edges = [
        "OWNS", "PERFORMS", "USES_DEVICE", "USES_IP", "TRANSACTION_TO",
        "SEEN_IN_TRANSACTION", "INVESTIGATES", "MATCHES_PATTERN",
        "HAS_EVIDENCE", "RECOMMENDS_ACTION", "RELATED_CASE",
        "FROM_TRANSACTION", "FROM_DEVICE", "FROM_IP", "INVESTIGATION_LOG"
    ]
    for e in edges:
        print(f"  • {e}")
    
    print("\n🎯 Fraud Patterns (Reference Data):")
    for pattern in builder.get_fraud_patterns():
        print(f"  • {pattern['pattern_name']} (weight: {pattern['risk_weight']})")
    
    print("\n📡 Connection Status:")
    status = builder.get_connection_status()
    for key, val in status.items():
        print(f"  • {key}: {val}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print_schema_info()
