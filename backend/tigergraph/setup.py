"""
TigerGraph Setup Script
Initialize graph, load schema, and populate data
"""

import logging
import sys
from pathlib import Path
from backend.tigergraph.client import get_client, close_client
from backend.tigergraph.loader import load_data
from backend.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main setup workflow"""
    logger.info("=" * 70)
    logger.info("HHGOA_IEEE TigerGraph Setup - Phase 1")
    logger.info("=" * 70)

    try:
        # Step 1: Connect to TigerGraph
        logger.info("\n[Step 1] Connecting to TigerGraph...")
        client = get_client()
        
        if not client.health_check():
            logger.error("✗ TigerGraph is not running or not accessible")
            logger.error(f"  Host: {settings.tigergraph.host}")
            logger.error(f"  Graph: {settings.tigergraph.graph_name}")
            logger.error("\nTo start TigerGraph:")
            logger.error("  Community Edition:")
            logger.error("    docker run -d -p 14240:14240 tigergraph/tigergraph")
            logger.error("  OR Savanna Cloud:")
            logger.error("    Visit https://savanna.tgcloud.io/")
            return False

        logger.info("✓ Connected to TigerGraph")

        # Step 2: Check/create graph
        logger.info("\n[Step 2] Checking graph existence...")
        if not client.graph_exists():
            logger.warning(f"⚠ Graph '{settings.tigergraph.graph_name}' does not exist")
            logger.info("   You need to create it using GSQL:")
            logger.info(f"   CREATE GRAPH {settings.tigergraph.graph_name}();")
            logger.info("\n   Schema file: backend/tigergraph/schema.gsql")
            logger.info("   Installation instructions in SETUP_PHASE1.md")
            return False
        
        logger.info(f"✓ Graph '{settings.tigergraph.graph_name}' exists")

        # Step 3: Get graph stats
        logger.info("\n[Step 3] Current graph statistics...")
        stats = client.get_graph_stats()
        logger.info(f"  Vertices: {stats.get('vertex_count', 0)}")
        logger.info(f"  Edges: {stats.get('edge_count', 0)}")

        # Step 4: Load data
        logger.info("\n[Step 4] Loading data into TigerGraph...")
        load_stats = load_data()
        logger.info(f"✓ Data load complete: {load_stats}")

        # Step 5: Final stats
        logger.info("\n[Step 5] Final graph statistics...")
        final_stats = client.get_graph_stats()
        logger.info(f"  Vertices: {final_stats.get('vertex_count', 0)}")
        logger.info(f"  Edges: {final_stats.get('edge_count', 0)}")

        logger.info("\n" + "=" * 70)
        logger.info("✓ Phase 1 Complete: TigerGraph ready for agent operations")
        logger.info("=" * 70)
        logger.info("\nNext: Phase 2 - GraphRAG Implementation")

        return True

    except Exception as e:
        logger.error(f"\n✗ Setup failed: {str(e)}")
        logger.exception("Full traceback:")
        return False

    finally:
        close_client()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
