"""
HHGOA_IEEE Fraud Investigation System - Configuration
Real TigerGraph + MCP + GraphRAG + LangGraph Integration
"""

from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class TigerGraphConfig(BaseModel):
    """TigerGraph Connection Configuration"""
    host: str = os.getenv("TG_HOST", "")
    username: str = os.getenv("TG_USERNAME", "")
    password: str = os.getenv("TG_PASSWORD", "")
    api_token: str = (
        os.getenv("TG_API_TOKEN")
        or os.getenv("TG_TOKEN")
        or os.getenv("TIGERGRAPH_API_KEY")
        or os.getenv("TIGERGRAPH_API_TOKEN", "")
        or ""
    )
    jwt_token: str = os.getenv("TG_JWT_TOKEN", "")
    graph_name: str = os.getenv("TG_GRAPH", "FraudInvestigation")
    rest_port: int = int(os.getenv("TG_REST_PORT", "443"))
    gsql_port: int = int(os.getenv("TG_GS_PORT", "14240"))


class MCPConfig(BaseModel):
    """TigerGraph MCP Configuration"""
    enabled: bool = os.getenv("MCP_ENABLED", "true").lower() == "true"
    host: str = os.getenv("MCP_HOST", "localhost")
    port: int = int(os.getenv("MCP_PORT", "3000"))


class GraphRAGConfig(BaseModel):
    """GraphRAG Vector Search Configuration"""
    enabled: bool = os.getenv("GRAPHRAG_ENABLED", "true").lower() == "true"
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    vector_dim: int = int(os.getenv("VECTOR_DIM", "384"))
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    max_results: int = int(os.getenv("MAX_RESULTS", "5"))


class LLMConfig(BaseModel):
    """LLM Configuration (OpenAI)"""
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.0"))
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))


class AgentConfig(BaseModel):
    """LangGraph Agent Configuration"""
    max_iterations: int = int(os.getenv("AGENT_MAX_ITER", "6"))
    uncertainty_threshold: float = float(os.getenv("UNCERTAINTY_THRESHOLD", "0.4"))
    evidence_required: int = int(os.getenv("EVIDENCE_REQUIRED", "3"))
    timeout_seconds: int = int(os.getenv("AGENT_TIMEOUT", "300"))


class DataConfig(BaseModel):
    """Data Loading Configuration"""
    data_dir: str = os.getenv("DATA_DIR", "./data")
    transaction_file: str = os.getenv("TRANS_FILE", "train_transaction.csv")
    identity_file: str = os.getenv("IDENTITY_FILE", "train_identity.csv")
    closed_cases_file: str = os.getenv("CLOSED_CASES_FILE", "closed_cases.csv")
    policies_file: str = os.getenv("POLICIES_FILE", "fraud_policies.md")
    patterns_file: str = os.getenv("PATTERNS_FILE", "known_patterns.json")
    benchmark_file: str = os.getenv("BENCHMARK_FILE", "benchmark_cases.json")
    max_samples: int = int(os.getenv("MAX_SAMPLES", "10000"))


class AppSettings(BaseModel):
    """Main Application Settings"""
    app_name: str = "FraudInvest Agent - HHGOA_IEEE"
    api_version: str = "v2"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Sub-configurations
    tigergraph: TigerGraphConfig = TigerGraphConfig()
    mcp: MCPConfig = MCPConfig()
    graphrag: GraphRAGConfig = GraphRAGConfig()
    llm: LLMConfig = LLMConfig()
    agent: AgentConfig = AgentConfig()
    data: DataConfig = DataConfig()


# Global settings instance
settings = AppSettings()


# Validation
def validate_settings():
    """Validate critical settings"""
    if settings.llm.api_key and not settings.llm.api_key.startswith("sk-"):
        raise ValueError("Invalid OpenAI API key format")
    
    if settings.agent.uncertainty_threshold < 0 or settings.agent.uncertainty_threshold > 1:
        raise ValueError("Uncertainty threshold must be between 0 and 1")
    
    return True
