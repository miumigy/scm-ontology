"""Optional Neo4j graph-store adapter boundary.

The semantic core remains independent of Neo4j. A transaction callable is
injected by the application layer, keeping the database driver out of the
ontology model.
"""
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

        self._execute(
            """
            UNWIND $nodes AS node
            MERGE (n:CanonicalNode {id: node.id})
            SET n.type = node.type, n.properties = node.properties
            """,
            {"nodes": graph.to_mapping()["nodes"]},
        )
        return GraphStoreWriteResult(plan.plan_id, plan.graph_digest, "applied")
