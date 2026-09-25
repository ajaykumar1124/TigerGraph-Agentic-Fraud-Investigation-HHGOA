"""
TigerGraph MCP CLI - Command-line interface for MCP server
Implements stdio transport for claude integration
"""

import sys
import json
import logging
from typing import Any, Dict

from backend.mcp.server import create_mcp_server
from backend.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,  # Send logs to stderr to avoid interfering with stdio
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for MCP server"""
    logger.info("=" * 70)
    logger.info("TigerGraph MCP Server Starting")
    logger.info("=" * 70)

    try:
        # Create MCP server
        server = create_mcp_server()
        logger.info(f"✓ MCP Server initialized with {len(server.tools_registry)} tools")

        # MCP protocol handler
        def handle_mcp_protocol():
            """Handle MCP protocol messages from stdin"""
            for line in sys.stdin:
                try:
                    if line.strip():
                        request = json.loads(line)
                        response = server.handle_request(request)
                        # Send response to stdout
                        sys.stdout.write(json.dumps(response) + "\n")
                        sys.stdout.flush()
                except json.JSONDecodeError:
                    error_response = {"type": "error", "error": "Invalid JSON"}
                    sys.stdout.write(json.dumps(error_response) + "\n")
                    sys.stdout.flush()
                except Exception as e:
                    error_response = {"type": "error", "error": str(e)}
                    sys.stdout.write(json.dumps(error_response) + "\n")
                    sys.stdout.flush()

        logger.info("Starting MCP protocol handler...")
        handle_mcp_protocol()

    except KeyboardInterrupt:
        logger.info("✓ MCP Server stopped (keyboard interrupt)")
        sys.exit(0)

    except Exception as e:
        logger.error(f"✗ MCP Server failed: {str(e)}")
        logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()
