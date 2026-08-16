from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .auditable_reasoning import AuditableReasoningResult, build_reasoning_result
from .canonical_graph import CanonicalGraph, SemanticNode
from .constraint_reasoning import PathConstraint, evaluate_path
from .graph_consistency import validate_graph_consistency
from .semantic_query import SemanticSupplyChainPath


class ReasoningQueryError(ValueError):
    pass


@dataclass(frozen=True)
class NodeQuery:
    node_type: str | None = None
    node_id: str | None = None


def query_nodes(graph: CanonicalGraph, query: NodeQuery = NodeQuery()) -> tuple[SemanticNode, ...]:
    """Return canonical graph nodes matching an explicit reasoning query."""
    validate_graph_consistency(graph)
    if query.node_type is None and query.node_id is None:
        raise ReasoningQueryError("at least one query constraint is required")
    return tuple(
        node
        for node in graph.nodes
        if (query.node_type is None or node.node_type == query.node_type)
        and (query.node_id is None or node.node_id == query.node_id)
    )


@dataclass(frozen=True)
class ReasoningQuery:
    at: str
    path: SemanticSupplyChainPath
    constraint: PathConstraint


class ReasoningQueryRuntime:
    """Evaluate a semantic path and expose a stable auditable result contract."""

    def execute(self, query: ReasoningQuery) -> AuditableReasoningResult:
        if query.path.at != query.at:
            raise ReasoningQueryError("query timestamp must match semantic path timestamp")
        return build_reasoning_result(evaluate_path(query.path, query.constraint))


def reasoning_result_to_mapping(result: AuditableReasoningResult) -> dict[str, Any]:
    """Return a JSON-compatible representation for APIs and agents."""
    return {
        "result_id": result.result_id,
        "status": result.status,
        "at": result.at,
        "node_ids": list(result.node_ids),
        "checks": [dict(check) for check in result.checks],
        "evidence": [
            {
                "relationship_id": item.relationship_id,
                "predicate": item.predicate,
                "from_id": item.from_id,
                "to_id": item.to_id,
                "qualifiers": dict(item.qualifiers),
            }
            for item in result.evidence
        ],
    }
