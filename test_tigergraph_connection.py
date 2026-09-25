"""
TigerGraph Cloud Connection Test Script
Tests connection with new secret token
"""

import pyTigerGraph as tg
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test TigerGraph Cloud connection with different URL formats"""
    
    secret = os.getenv('TG_SECRET', 'jgc09m44bal797ovbosd667slpnpmrvu')
    graphname = os.getenv('TG_GRAPHNAME', 'FraudInvestigation')
    
    print("=" * 60)
    print("🔗 TigerGraph Cloud Connection Test")
    print("=" * 60)
    print(f"Secret: {secret[:10]}...{secret[-10:]}")
    print(f"Graph: {graphname}")
    print()
    
    # Test different URL formats
    test_urls = [
        # Format 1: Instance ID as subdomain
        "https://48373791-572d-43f4-8d89-96e876777d88.i.tgcloud.io",
        
        # Format 2: Workgroup URL
        "https://a64afea1-3279-42c6-ac22-96882437db91.i.tgcloud.io",
        
        # Format 3: You need to provide your actual workspace URL from TigerGraph Cloud dashboard
        # It should look like: https://xxxx.i.tgcloud.io or https://xxxx.tgcloud.io
    ]
    
    for idx, host in enumerate(test_urls, 1):
        print(f"\n📍 Test {idx}: {host}")
        print("-" * 60)
        
        try:
            print("   Connecting...")
            
            conn = tg.TigerGraphConnection(
                host=host,
                graphname=graphname,
                username="tigergraph",
                password=secret,  # Try secret as password first
                useCert=True
            )
            
            # Test basic connection
            try:
                version = conn.getVersion()
                print(f"   ✅ SUCCESS! TigerGraph Version: {version}")
                print(f"   🎯 Use this URL: {host}")
                
                # Get available graphs
                graphs = conn.getGraphs()
                print(f"   📊 Available Graphs: {graphs}")
                
                return host, True
                
            except Exception as version_error:
                print(f"   ⚠️  Connected but version check failed: {version_error}")
                
                # Try with API token authentication instead
                print("   🔄 Trying with secret as API token...")
                conn = tg.TigerGraphConnection(
                    host=host,
                    graphname=graphname,
                    username="tigergraph",
                    apiToken=secret,
                    useCert=True
                )
                
                version = conn.getVersion()
                print(f"   ✅ SUCCESS with API token! Version: {version}")
                print(f"   🎯 Use this URL: {host}")
                print(f"   💡 Use TG_SECRET as TG_API_TOKEN in .env")
                
                return host, True
                
        except Exception as e:
            print(f"   ❌ Failed: {str(e)[:100]}")
            continue
    
    print("\n" + "=" * 60)
    print("❌ All connection attempts failed")
    print("\n📝 Next Steps:")
    print("1. Log into https://tgcloud.io/")
    print("2. Go to your workspace/cluster")
    print("3. Find the 'Connection' or 'REST API' section")
    print("4. Copy the exact hostname (e.g., https://xxxx.i.tgcloud.io)")
    print("5. Update TG_HOST in .env file")
    print("6. Run this script again")
    print("=" * 60)
    
    return None, False


def test_graph_queries(host):
    """Test basic graph queries"""
    secret = os.getenv('TG_SECRET')
    graphname = os.getenv('TG_GRAPHNAME', 'FraudInvestigation')
    
    print("\n" + "=" * 60)
    print("🧪 Testing Graph Queries")
    print("=" * 60)
    
    try:
        conn = tg.TigerGraphConnection(
            host=host,
            graphname=graphname,
            username="tigergraph",
            apiToken=secret,
            useCert=True
        )
        
        # Test 1: Get vertex types
        print("\n1️⃣  Getting vertex types...")
        vertex_types = conn.getVertexTypes()
        print(f"   ✅ Vertex Types: {vertex_types}")
        
        # Test 2: Get edge types
        print("\n2️⃣  Getting edge types...")
        edge_types = conn.getEdgeTypes()
        print(f"   ✅ Edge Types: {edge_types}")
        
        # Test 3: Get schema
        print("\n3️⃣  Getting schema...")
        schema = conn.getSchema()
        print(f"   ✅ Schema retrieved successfully")
        
        # Test 4: Count vertices
        if vertex_types:
            print("\n4️⃣  Counting vertices...")
            for vtype in vertex_types[:3]:  # First 3 types
                try:
                    count = conn.getVertexCount(vtype)
                    print(f"   ✅ {vtype}: {count} vertices")
                except Exception as e:
                    print(f"   ⚠️  {vtype}: {e}")
        
        print("\n" + "=" * 60)
        print("✅ Graph queries working!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Query test failed: {e}")
        return False


if __name__ == "__main__":
    # Test connection
    successful_host, connected = test_connection()
    
    # If connected, test queries
    if connected and successful_host:
        test_graph_queries(successful_host)
    else:
        print("\n💡 Tip: Your TigerGraph Cloud workspace URL should be provided")
        print("   It's typically in the format: https://[workspace-id].i.tgcloud.io")
        print("   You can find it in your TigerGraph Cloud dashboard under 'Connection Details'")
