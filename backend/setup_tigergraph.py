"""
TigerGraph Savana Cloud Setup Script
Sets up the fraud investigation graph schema and loads initial data
"""

import pyTigerGraph as tg
import json
import os
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

# Savana Cloud Configuration
SAVANA_HOST = os.getenv("TG_HOST", "https://savana.i.tgcloud.io")
API_TOKEN = os.getenv("TG_API_TOKEN", "D3noyFE9ClZFmX7Ctais-2s1NBnwiSEUFBB6.0I5")
GRAPH_NAME = os.getenv("TG_GRAPH", "FraudInvestigation")
USERNAME = os.getenv("TG_USERNAME", "tigergraph")


def connect_to_tigergraph():
    """Connect to TigerGraph Savana Cloud"""
    print(f"🔗 Connecting to TigerGraph Savana Cloud...")
    print(f"   Host: {SAVANA_HOST}")
    print(f"   Graph: {GRAPH_NAME}")
    
    try:
        conn = tg.TigerGraphConnection(
            host=SAVANA_HOST,
            graphname=GRAPH_NAME,
            username=USERNAME,
            apiToken=API_TOKEN,
            useCert=True
        )
        
        # Test connection
        version = conn.getVersion()
        print(f"✅ Connected to TigerGraph {version}")
        return conn
    
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None


def clear_existing_data(conn):
    """Clear existing graph data (if any)"""
    print("\n🗑️  Clearing existing data...")
    
    try:
        # Check if graph exists
        graphs = conn.getGraphs()
        print(f"   Existing graphs: {graphs}")
        
        if GRAPH_NAME in graphs:
            print(f"   Graph '{GRAPH_NAME}' exists")
            # Try to drop the graph
            try:
                conn.gsql(f"DROP GRAPH {GRAPH_NAME} CASCADE")
                print(f"✅ Dropped graph '{GRAPH_NAME}'")
            except Exception as e:
                print(f"⚠️  Could not drop graph: {e}")
        else:
            print(f"   Graph '{GRAPH_NAME}' does not exist yet")
        
        return True
    
    except Exception as e:
        print(f"⚠️  Error during cleanup: {e}")
        return False


def create_schema(conn):
    """Create fraud investigation graph schema"""
    print("\n📊 Creating graph schema...")
    
    schema_gsql = f"""
CREATE GRAPH {GRAPH_NAME}()

USE GRAPH {GRAPH_NAME}

# ===================================
# Vertex Types
# ===================================

CREATE VERTEX Transaction (
    PRIMARY_ID transaction_id STRING,
    amount DOUBLE,
    timestamp DATETIME,
    transaction_type STRING,
    status STRING DEFAULT "pending",
    risk_score DOUBLE DEFAULT 0.0,
    is_fraud BOOL DEFAULT FALSE,
    location STRING,
    device_id STRING,
    ip_address STRING,
    merchant_id STRING,
    created_at DATETIME DEFAULT NOW()
) WITH PRIMARY_ID_AS_ATTRIBUTE="TRUE"

CREATE VERTEX User (
    PRIMARY_ID user_id STRING,
    email STRING,
    phone STRING,
    account_created DATETIME,
    kyc_status STRING DEFAULT "pending",
    risk_level STRING DEFAULT "low",
    total_transactions INT DEFAULT 0,
    total_amount DOUBLE DEFAULT 0.0
) WITH PRIMARY_ID_AS_ATTRIBUTE="TRUE"

CREATE VERTEX Device (
    PRIMARY_ID device_id STRING,
    device_type STRING,
    os STRING,
    browser STRING,
    first_seen DATETIME,
    last_seen DATETIME,
    is_suspicious BOOL DEFAULT FALSE
) WITH PRIMARY_ID_AS_ATTRIBUTE="TRUE"

CREATE VERTEX IPAddress (
    PRIMARY_ID ip_address STRING,
    country STRING,
    city STRING,
    is_vpn BOOL DEFAULT FALSE,
    is_proxy BOOL DEFAULT FALSE,
    risk_score DOUBLE DEFAULT 0.0,
    first_seen DATETIME,
    last_seen DATETIME
) WITH PRIMARY_ID_AS_ATTRIBUTE="TRUE"

CREATE VERTEX Merchant (
    PRIMARY_ID merchant_id STRING,
    merchant_name STRING,
    category STRING,
    country STRING,
    risk_level STRING DEFAULT "low"
) WITH PRIMARY_ID_AS_ATTRIBUTE="TRUE"

CREATE VERTEX FraudCase (
    PRIMARY_ID case_id STRING,
    status STRING DEFAULT "open",
    priority STRING DEFAULT "medium",
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    assigned_to STRING,
    resolution STRING,
    notes STRING
) WITH PRIMARY_ID_AS_ATTRIBUTE="TRUE"

# ===================================
# Edge Types
# ===================================

CREATE DIRECTED EDGE PERFORMED (
    FROM User,
    TO Transaction,
    timestamp DATETIME DEFAULT NOW()
)

CREATE DIRECTED EDGE USED_DEVICE (
    FROM Transaction,
    TO Device,
    timestamp DATETIME DEFAULT NOW()
)

CREATE DIRECTED EDGE FROM_IP (
    FROM Transaction,
    TO IPAddress,
    timestamp DATETIME DEFAULT NOW()
)

CREATE DIRECTED EDGE AT_MERCHANT (
    FROM Transaction,
    TO Merchant,
    timestamp DATETIME DEFAULT NOW()
)

CREATE DIRECTED EDGE SIMILAR_TO (
    FROM Transaction,
    TO Transaction,
    similarity_score DOUBLE DEFAULT 0.0,
    reason STRING
)

CREATE DIRECTED EDGE RELATED_CASE (
    FROM Transaction,
    TO FraudCase,
    flagged_at DATETIME DEFAULT NOW()
)

CREATE DIRECTED EDGE OWNS_DEVICE (
    FROM User,
    TO Device,
    first_used DATETIME DEFAULT NOW()
)

CREATE DIRECTED EDGE SHARED_DEVICE (
    FROM User,
    TO Device,
    shared_count INT DEFAULT 1
)

# ===================================
# Install Schema
# ===================================

INSTALL QUERY ALL
"""
    
    try:
        result = conn.gsql(schema_gsql)
        print("✅ Schema created successfully")
        return True
    
    except Exception as e:
        print(f"❌ Schema creation failed: {e}")
        return False


def load_sample_data(conn):
    """Load sample fraud data"""
    print("\n📥 Loading sample data...")
    
    # Sample Users
    users = [
        {"user_id": "USR_1001", "email": "user1@example.com", "phone": "+91-9876543210", "kyc_status": "verified"},
        {"user_id": "USR_1002", "email": "user2@example.com", "phone": "+91-9876543211", "kyc_status": "verified"},
        {"user_id": "USR_1003", "email": "user3@example.com", "phone": "+91-9876543212", "kyc_status": "pending"},
    ]
    
    # Sample Transactions
    transactions = [
        {
            "transaction_id": "TXN_2026_001",
            "amount": 15000.0,
            "transaction_type": "card_payment",
            "status": "flagged",
            "risk_score": 0.92,
            "is_fraud": True,
            "location": "Mumbai",
            "device_id": "DEV_001",
            "ip_address": "192.168.1.100",
            "merchant_id": "MERCH_001"
        },
        {
            "transaction_id": "TXN_2026_002",
            "amount": 250.0,
            "transaction_type": "online_purchase",
            "status": "approved",
            "risk_score": 0.12,
            "is_fraud": False,
            "location": "Delhi",
            "device_id": "DEV_002",
            "ip_address": "192.168.1.101",
            "merchant_id": "MERCH_002"
        }
    ]
    
    try:
        # Upsert users
        for user in users:
            conn.upsertVertex("User", user["user_id"], attributes=user)
        print(f"✅ Loaded {len(users)} users")
        
        # Upsert transactions
        for txn in transactions:
            conn.upsertVertex("Transaction", txn["transaction_id"], attributes=txn)
        print(f"✅ Loaded {len(transactions)} transactions")
        
        # Create relationships
        conn.upsertEdge("User", "USR_1001", "PERFORMED", "Transaction", "TXN_2026_001")
        conn.upsertEdge("User", "USR_1002", "PERFORMED", "Transaction", "TXN_2026_002")
        print("✅ Created relationships")
        
        return True
    
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False


def verify_setup(conn):
    """Verify the setup"""
    print("\n✓ Verifying setup...")
    
    try:
        # Count vertices
        user_count = conn.getVertexCount("User")
        txn_count = conn.getVertexCount("Transaction")
        
        print(f"   Users: {user_count}")
        print(f"   Transactions: {txn_count}")
        
        if user_count > 0 and txn_count > 0:
            print("✅ Setup verification successful!")
            return True
        else:
            print("⚠️  Setup incomplete - no data found")
            return False
    
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False


def main():
    """Main setup process"""
    print("=" * 60)
    print("TigerGraph Savana Cloud Setup - Fraud Investigation System")
    print("=" * 60)
    
    # Step 1: Connect
    conn = connect_to_tigergraph()
    if not conn:
        print("\n❌ Setup failed - could not connect")
        return False
    
    # Step 2: Clear old data
    clear_existing_data(conn)
    
    # Step 3: Create schema
    if not create_schema(conn):
        print("\n❌ Setup failed - schema creation error")
        return False
    
    # Step 4: Load sample data
    if not load_sample_data(conn):
        print("\n❌ Setup failed - data loading error")
        return False
    
    # Step 5: Verify
    if not verify_setup(conn):
        print("\n⚠️  Setup completed with warnings")
        return False
    
    print("\n" + "=" * 60)
    print("✅ TigerGraph setup completed successfully!")
    print("=" * 60)
    print(f"\n📊 Graph Name: {GRAPH_NAME}")
    print(f"🔗 Host: {SAVANA_HOST}")
    print(f"🔑 API Token: {API_TOKEN[:20]}...")
    print("\n✨ You can now use the fraud investigation system!")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
