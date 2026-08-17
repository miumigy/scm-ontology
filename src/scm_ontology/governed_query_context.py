"""Immutable, auditable context for graph query results."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Mapping

from .canonical_graph import CanonicalGraph
from .execution_trace import ExecutionTrace
from .execution_trace_graph_validation import ExecutionTraceGraphValidation
from .graph_query import GraphQueryResult


class GovernedQueryContextError(ValueError):
    """Raised when a governed query context cannot be constructed safely."""


@dataclass(frozen=True)
class GraphQuerySpec:
    """Exact query intent captured before a result is consumed."""

    operation: str
    node_type: str | None = None
    node_id: str | None = None
    relationship_type: str | None = None

    def __post_init__(self) -> None:
        if not self.operation.strip():
            raise GovernedQueryContextError("operation must be non-empty")
        for name in ("node_type", "node_id", "relationship_type"):
            value = getattr(self, name)
            if value is not None and not value.strip():
                raise GovernedQueryContextError(f"{name} must be non-empty when supplied")

    def to_mapping(self) -> dict[str, str]:
        return {
            key: value
            for key, value in {
                "operation": self.operation,
                "node_type": self.node_type,
                "node_id": self.node_id,
                "relationship_type": self.relationship_type,
            }.items()
            if value is not None
        }


@dataclass(frozen=True)
class GovernedQueryContext:
    """Immutable evidence boundary between graph query and reasoning."""

    contract_version: str
    context_id: str
    graph_identity: str
    query: GraphQuerySpec
    node_ids: tuple[str, ...]
    relationship_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]

    def to_mapping(self) -> dict[str, object]:
        return {
            "contract_version": self.contract_version,
            "context_id": self.context_id,
            "graph_identity": self.graph_identity,
            "query": self.query.to_mapping(),
            "node_ids": list(self.node_ids),
            "relationship_ids": list(self.relationship_ids),
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


def build_governed_query_context(
    trace: ExecutionTrace,
    graph: CanonicalGraph,
    result: GraphQueryResult,
    validation: ExecutionTraceGraphValidation,
    *,
    query: GraphQuerySpec,
) -> GovernedQueryContext:
    """Create a reasoning-ready query context only from a valid trace graph."""
    if not isinstance(trace, ExecutionTrace):
        raise GovernedQueryContextError("trace must be an ExecutionTrace")
    if not isinstance(graph, CanonicalGraph):
        raise GovernedQueryContextError("graph must be a CanonicalGraph")
    if not isinstance(result, GraphQueryResult):
        raise GovernedQueryContextError("result must be a GraphQueryResult")
    if not isinstance(validation, ExecutionTraceGraphValidation):
        raise GovernedQueryContextError("validation must be an ExecutionTraceGraphValidation")
    if not validation.valid:
        raise GovernedQueryContextError("cannot build governed query context from an invalid graph")
    if not isinstance(query, GraphQuerySpec):
        raise GovernedQueryContextError("query must be a GraphQuerySpec")

    graph_identity = "sha256:" + sha256(graph.to_json().encode("utf-8")).hexdigest()
    node_ids = tuple(sorted(n.node_id for n in result.nodes))
    relationship_ids = tuple(sorted(r.relationship_id for r in result.relationships))
    return GovernedQueryContext(
        contract_version="S357.1",
        context_id=trace.context_id,
        graph_identity=graph_identity,
        query=query,
        node_ids=node_ids,
        relationship_ids=relationship_ids,
        evidence_ids=tuple(sorted(set(trace.evidence_ids))),
        provenance_ids=tuple(sorted(set(trace.provenance_ids))),
    )
