"""
TigerGraph MCP Server - Expose tools to LLM via Model Context Protocol
Implements stdio transport for claude integration
"""

import logging
import json
from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod

from backend.mcp.tools import TigerGraphTools
from backend.config import settings

logger = logging.getLogger(__name__)


class MCPServer:
    """
    MCP Server for TigerGraph tools
    Exposes query and analysis functions to LLM agents
    """

    def __init__(self, tools=None):
        """Initialize MCP server"""
        self.tools = tools or TigerGraphTools()
        self.tools_registry = self._register_tools()

    def _register_tools(self) -> Dict[str, Dict[str, Any]]:
        """Register all available tools"""
        return {
            "query_user_profile": {
                "description": "Query user profile and risk indicators from TigerGraph",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "User ID to query",
                        },
                    },
                    "required": ["user_id"],
                },
                "function": self.tools.query_user_profile,
            },
            "query_transaction_details": {
                "description": "Query transaction details and relationships",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "transaction_id": {
                            "type": "string",
                            "description": "Transaction ID to query",
                        },
                    },
                    "required": ["transaction_id"],
                },
                "function": self.tools.query_transaction_details,
            },
            "query_card_details": {
                "description": "Query card profile and transaction history",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "card_id": {
                            "type": "string",
                            "description": "Card ID to query",
                        },
                    },
                    "required": ["card_id"],
                },
                "function": self.tools.query_card_details,
            },
            "query_device_details": {
                "description": "Query device profile and usage history",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {
                            "type": "string",
                            "description": "Device ID to query",
                        },
                    },
                    "required": ["device_id"],
                },
                "function": self.tools.query_device_details,
            },
            "query_merchant_profile": {
                "description": "Query merchant profile and risk category",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "merchant_id": {
                            "type": "string",
                            "description": "Merchant ID to query",
                        },
                    },
                    "required": ["merchant_id"],
                },
                "function": self.tools.query_merchant_profile,
            },
            "query_ip_address_risk": {
                "description": "Query IP address risk assessment and geolocation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ip_address": {
                            "type": "string",
                            "description": "IP address to query (e.g., 192.168.1.1)",
                        },
                    },
                    "required": ["ip_address"],
                },
                "function": self.tools.query_ip_address_risk,
            },
            "search_fraud_patterns": {
                "description": "Search for fraud pattern definitions and risk levels",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern_name": {
                            "type": "string",
                            "description": "Fraud pattern name to search (e.g., velocity_attack)",
                        },
                    },
                    "required": ["pattern_name"],
                },
                "function": self.tools.search_fraud_patterns,
            },
            "retrieve_evidence": {
                "description": "Retrieve evidence for fraud investigation using GraphRAG",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "case_context": {
                            "type": "object",
                            "description": "Case context with user_id, indicators, merchant, amount, etc.",
                            "properties": {
                                "user_id": {"type": "string"},
                                "indicators": {"type": "array", "items": {"type": "string"}},
                                "merchant": {"type": "string"},
                                "amount": {"type": "number"},
                            },
                        },
                    },
                    "required": ["case_context"],
                },
                "function": self.tools.retrieve_evidence,
            },
            "check_policies": {
                "description": "Check which fraud policies are violated by case context",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "case_context": {
                            "type": "object",
                            "description": "Case context with indicators to check",
                            "properties": {
                                "indicators": {"type": "array", "items": {"type": "string"}},
                            },
                        },
                    },
                    "required": ["case_context"],
                },
                "function": self.tools.check_policies,
            },
            "query_case_history": {
                "description": "Query case history and related information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "case_id": {
                            "type": "string",
                            "description": "Case ID to query",
                        },
                    },
                    "required": ["case_id"],
                },
                "function": self.tools.query_case_history,
            },
            "create_fraud_case": {
                "description": "Create a new fraud case in the graph",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "initiator": {
                            "type": "string",
                            "description": "Who initiated the investigation",
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User ID involved in case",
                        },
                        "transaction_id": {
                            "type": "string",
                            "description": "Transaction ID that triggered investigation",
                        },
                        "risk_level": {
                            "type": "string",
                            "description": "Initial risk level (LOW, MEDIUM, HIGH, CRITICAL)",
                        },
                        "indicators": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of fraud indicators detected",
                        },
                    },
                    "required": ["initiator", "user_id", "transaction_id", "risk_level"],
                },
                "function": self.tools.create_fraud_case,
            },
            "update_case_status": {
                "description": "Update case status and findings",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "case_id": {
                            "type": "string",
                            "description": "Case ID to update",
                        },
                        "status": {
                            "type": "string",
                            "description": "New status (OPEN, INVESTIGATING, RESOLVED)",
                        },
                        "next_action": {
                            "type": "string",
                            "description": "Recommended next action",
                        },
                        "findings": {
                            "type": "string",
                            "description": "Investigation findings",
                        },
                    },
                    "required": ["case_id", "status"],
                },
                "function": self.tools.update_case_status,
            },
            "add_case_evidence": {
                "description": "Add evidence to a case",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "case_id": {
                            "type": "string",
                            "description": "Case ID",
                        },
                        "evidence_text": {
                            "type": "string",
                            "description": "Evidence description",
                        },
                        "evidence_type": {
                            "type": "string",
                            "description": "Type of evidence (general, pattern, policy, etc.)",
                        },
                    },
                    "required": ["case_id", "evidence_text"],
                },
                "function": self.tools.add_case_evidence,
            },
            "get_graph_stats": {
                "description": "Get overall graph statistics",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
                "function": self.tools.get_graph_stats,
            },
        }

    def get_tools_list(self) -> List[Dict[str, Any]]:
        """Get list of tools for MCP discovery"""
        tools_list = []
        for tool_name, tool_info in self.tools_registry.items():
            tools_list.append(
                {
                    "name": tool_name,
                    "description": tool_info["description"],
                    "inputSchema": tool_info["parameters"],
                }
            )
        return tools_list

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool with arguments"""
        if tool_name not in self.tools_registry:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}

        try:
            tool_info = self.tools_registry[tool_name]
            func = tool_info["function"]

            # Call function with arguments
            result = func(**arguments)
            return result

        except Exception as e:
            logger.error(f"Tool execution failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP protocol request"""
        request_type = request.get("type")

        if request_type == "list":
            return {"type": "list_response", "tools": self.get_tools_list()}

        elif request_type == "call":
            tool_name = request.get("name")
            arguments = request.get("arguments", {})
            result = self.call_tool(tool_name, arguments)
            return {"type": "call_response", "result": result}

        else:
            return {"type": "error", "error": f"Unknown request type: {request_type}"}


def create_mcp_server() -> MCPServer:
    """Create and configure MCP server"""
    logger.info("Creating TigerGraph MCP Server...")
    server = MCPServer()
    logger.info(f"✓ MCP Server created with {len(server.tools_registry)} tools")
    return server


# Singleton instance
_server: Optional[MCPServer] = None


def get_mcp_server() -> MCPServer:
    """Get or create MCP server"""
    global _server
    if _server is None:
        _server = create_mcp_server()
    return _server
