"""Optional Neo4j graph-store adapter boundary.

The semantic core does not import the Neo4j driver. The application injects a
transaction callable, while this adapter enforces the same authorization and
graph-digest invariants as the transport-neutral reference store.
"""
from __future__ import annotations

from hashlib import sha256
from typing import Any, Callable

from .canonical_graph import CanonicalGraph
from .graph_persistence import PersistencePlan
from .graph_store import GraphStoreWriteResult


class Neo4jGraphStoreAdapter:
    """Execute a governed persistence plan through an injected Neo4j transaction."""

    def __init__(self, execute: Callable[[str, dict[str, Any]], None]) -> None:
        self._execute = execute

    def apply(self, graph: CanonicalGraph, plan: PersistencePlan) -> GraphStoreWriteResult:
        if plan.outcome != "planned":
            raise ValueError("only an authorized planned persistence intent may be applied")

        serialized = graph.to_json()
        digest = sha256(serialized.encode("utf-8")).hexdigest()
        if digest != plan.graph_digest:
            raise ValueError("graph digest does not match persistence plan")

        payload = graph.to_mapping()
        params = {
            "plan_id": plan.plan_id,
            "graph_digest": plan.graph_digest,
            "decision_id": plan.decision_id,
            "actor": plan.actor,
            "scope": plan.scope,
            "reason": plan.reason,
            "nodes": payload["nodes"],
            "relationships": payload["relationships"],
        }
        self._execute(
            """
            MERGE (p:CanonicalPersistencePlan {plan_id: $plan_id})
            SET p.graph_digest = $graph_digest,
                p.decision_id = $decision_id,
                p.actor = $actor,
                p.scope = $scope,
                p.reason = $reason
            CALL {
                WITH p
                UNWIND $nodes AS node
                MERGE (n:CanonicalNode {id: node.id})
                SET n.type = node.type, n.properties = node.properties
                RETURN count(n) AS node_count
            }
            CALL {
                WITH p
                UNWIND $relationships AS rel
                MATCH (a:CanonicalNode {id: rel.from})
                MATCH (b:CanonicalNode {id: rel.to})
                MERGE (a)-[r:CANONICAL_RELATIONSHIP {id: rel.id}]->(b)
                SET r.predicate = rel.predicate, r.versions = rel.versions
                RETURN count(r) AS relationship_count
            }
            RETURN p.plan_id AS plan_id
            """,
            params,
        )
        return GraphStoreWriteResult(plan.plan_id, digest, "applied")
