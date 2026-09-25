"""
TigerGraph Client - Wrapper for pyTigerGraph
Handles all graph operations and queries
"""

import logging
import json
from typing import Any, Dict, List, Optional
from pyTigerGraph import TigerGraphConnection
from backend.config import settings

logger = logging.getLogger(__name__)


class TigerGraphClient:
    """
    TigerGraph connection wrapper with convenience methods
    """

    def __init__(self, config=None):
        """Initialize TigerGraph client"""
        self.config = config or settings.tigergraph
        self.conn: Optional[TigerGraphConnection] = None
        self._connect()

    def _connect(self):
        """Establish connection to TigerGraph"""
        try:
            if not self.config.host:
                raise ValueError("TG_HOST is required. Set it to your Savanna Cloud endpoint.")

            conn_kwargs = {
                "host": self.config.host,
                "graphname": self.config.graph_name,
                "restppPort": self.config.rest_port,
            }

            if self.config.username and self.config.password:
                conn_kwargs["username"] = self.config.username
                conn_kwargs["password"] = self.config.password

            if self.config.api_token:
                conn_kwargs["apiToken"] = self.config.api_token

            if self.config.jwt_token:
                conn_kwargs["jwtToken"] = self.config.jwt_token

            self.conn = TigerGraphConnection(**conn_kwargs)
            logger.info(f"✓ Connected to TigerGraph: {self.config.host}/{self.config.graph_name}")
        except Exception as e:
            logger.error(f"✗ Failed to connect to TigerGraph: {str(e)}")
            raise

    def health_check(self) -> bool:
        """Check if TigerGraph is healthy"""
        try:
            result = self.conn.getVcount()
            logger.info(f"✓ TigerGraph health check passed. Vertex count: {result}")
            return True
        except Exception as e:
            logger.error(f"✗ TigerGraph health check failed: {str(e)}")
            return False

    def graph_exists(self) -> bool:
        """Check if graph exists"""
        try:
            graphs = self.conn.getGraphs()
            return self.config.graph_name in graphs
        except Exception as e:
            logger.error(f"✗ Error checking graph existence: {str(e)}")
            return False

    def run_gsql(self, gsql_query: str) -> Dict[str, Any]:
        """Run GSQL query"""
        try:
            result = self.conn.runInterpretedQuery(gsql_query)
            logger.debug(f"GSQL query executed: {gsql_query[:100]}")
            return result
        except Exception as e:
            logger.error(f"✗ GSQL query failed: {str(e)}")
            raise

    def run_rest_query(self, query_name: str, params: Dict = None) -> Dict[str, Any]:
        """Run REST query"""
        try:
            params = params or {}
            result = self.conn.runInstalledQuery(query_name, params)
            logger.debug(f"REST query executed: {query_name}")
            return result
        except Exception as e:
            logger.error(f"✗ REST query failed: {str(e)}")
            raise

    def upsert_vertex(self, vertex_type: str, vertex_id: str, attributes: Dict) -> bool:
        """Insert or update vertex"""
        try:
            self.conn.upsertVertex(vertex_type, vertex_id, attributes)
            logger.debug(f"Upserted {vertex_type}:{vertex_id}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to upsert vertex: {str(e)}")
            raise

    def upsert_edge(
        self,
        edge_type: str,
        from_vertex_type: str,
        from_vertex_id: str,
        to_vertex_type: str,
        to_vertex_id: str,
        attributes: Dict = None,
    ) -> bool:
        """Insert or update edge"""
        try:
            attributes = attributes or {}
            self.conn.upsertEdge(
                edge_type,
                from_vertex_type,
                from_vertex_id,
                to_vertex_type,
                to_vertex_id,
                attributes,
            )
            logger.debug(f"Upserted edge {edge_type}: {from_vertex_id} -> {to_vertex_id}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to upsert edge: {str(e)}")
            raise

    def get_vertex(self, vertex_type: str, vertex_id: str) -> Dict[str, Any]:
        """Get vertex by ID"""
        try:
            result = self.conn.getVertex(vertex_type, vertex_id)
            return result
        except Exception as e:
            logger.error(f"✗ Failed to get vertex: {str(e)}")
            raise

    def get_edge(
        self,
        edge_type: str,
        from_vertex_type: str,
        from_vertex_id: str,
        to_vertex_type: str,
        to_vertex_id: str,
    ) -> Dict[str, Any]:
        """Get edge by vertices"""
        try:
            result = self.conn.getEdge(
                edge_type, from_vertex_type, from_vertex_id, to_vertex_type, to_vertex_id
            )
            return result
        except Exception as e:
            logger.error(f"✗ Failed to get edge: {str(e)}")
            raise

    def delete_vertex(self, vertex_type: str, vertex_id: str) -> bool:
        """Delete vertex"""
        try:
            self.conn.delVertex(vertex_type, vertex_id)
            logger.debug(f"Deleted vertex {vertex_type}:{vertex_id}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to delete vertex: {str(e)}")
            raise

    def query_vertices_by_type(self, vertex_type: str, limit: int = 100) -> List[Dict]:
        """Query vertices by type"""
        try:
            result = self.conn.getVertices(vertex_type, limit=limit)
            return result
        except Exception as e:
            logger.error(f"✗ Failed to query vertices: {str(e)}")
            raise

    def get_neighbors(
        self, vertex_type: str, vertex_id: str, edge_type: str = None, max_depth: int = 1
    ) -> Dict[str, Any]:
        """Get neighboring vertices"""
        try:
            result = self.conn.getNeighbors(
                vertex_type, vertex_id, edgeType=edge_type, maxDepth=max_depth
            )
            return result
        except Exception as e:
            logger.error(f"✗ Failed to get neighbors: {str(e)}")
            raise

    def batch_insert_vertices(self, vertex_type: str, vertices: List[Dict]) -> bool:
        """Batch insert vertices"""
        try:
            for vertex in vertices:
                vertex_id = vertex.pop("PRIMARY_ID", None) or vertex.pop("id")
                self.upsert_vertex(vertex_type, vertex_id, vertex)
            logger.info(f"Inserted {len(vertices)} vertices of type {vertex_type}")
            return True
        except Exception as e:
            logger.error(f"✗ Batch insert failed: {str(e)}")
            raise

    def batch_insert_edges(self, edges: List[Dict]) -> bool:
        """Batch insert edges"""
        try:
            for edge in edges:
                self.upsert_edge(
                    edge_type=edge["edge_type"],
                    from_vertex_type=edge["from_type"],
                    from_vertex_id=edge["from_id"],
                    to_vertex_type=edge["to_type"],
                    to_vertex_id=edge["to_id"],
                    attributes=edge.get("attributes", {}),
                )
            logger.info(f"Inserted {len(edges)} edges")
            return True
        except Exception as e:
            logger.error(f"✗ Batch edge insert failed: {str(e)}")
            raise

    def get_graph_stats(self) -> Dict[str, Any]:
        """Get graph statistics"""
        try:
            stats = {
                "vertex_count": self.conn.getVcount(),
                "edge_count": self.conn.getEcount(),
                "graph_name": self.config.graph_name,
            }
            logger.info(f"Graph stats: {stats}")
            return stats
        except Exception as e:
            logger.error(f"✗ Failed to get graph stats: {str(e)}")
            raise

    def clear_graph(self) -> bool:
        """Clear all data from graph (use with caution)"""
        try:
            self.conn.clearGraph()
            logger.warning("✗ Graph cleared!")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to clear graph: {str(e)}")
            raise

    def close(self):
        """Close connection"""
        if self.conn:
            self.conn = None
            logger.info("✓ TigerGraph connection closed")


# Singleton instance
_client: Optional[TigerGraphClient] = None


def get_client() -> TigerGraphClient:
    """Get or create TigerGraph client"""
    global _client
    if _client is None:
        _client = TigerGraphClient()
    return _client


def close_client():
    """Close client"""
    global _client
    if _client:
        _client.close()
        _client = None
