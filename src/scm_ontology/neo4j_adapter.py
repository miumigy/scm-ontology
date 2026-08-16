"""Optional Neo4j graph-store adapter boundary."""
from __future__ import annotations

from typing import Any, Callable

from .canonical_graph import CanonicalGraph
from .graph_persistence import PersistencePlan
from .graph_store import GraphStoreWriteResult


class Neo4jGraphStoreAdapter:
    """Execute a governed persistence plan through an injected transaction callable."""

    def __init__(self, execute: Callable[[str, dict[str, Any]], None]) -> None:
        self._execute = execute

    def apply(self, graph: CanonicalGraph, plan: PersistencePlan) -> GraphStoreWriteResult:
        if plan.outcome != "planned":
            raise ValueError("only an authorized planned persistence intent may be applied")

        payload = graph.to_mapping()
        self._execute(
            """
            UNWIND $nodes AS node
            MERGE (n:CanonicalNode {id: node.id})
            SET n.type = node.type, n.properties = node.properties
            WITH 1 AS ignored
            UNWIND $relationships AS rel
            MATCH (a:CanonicalNode {id: rel.from})
            MATCH (b:CanonicalNode {id: rel.to})
            MERGE (a)-[r:CANONICAL_RELATIONSHIP {id: rel.id}]->(b)
            SET r.predicate = rel.predicate, r.versions = rel.versions
            """,
            {"nodes": payload["nodes"], "relationships": payload["relationships"]},
        )
        return GraphStoreWriteResult(plan.plan_id, plan.graph_digest, "applied")
