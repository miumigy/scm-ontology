"""Governed temporal semantic queries over the canonical SCM graph.

S319 is a read-only query boundary. It resolves explicitly represented
relationship paths at an instant, preserves relationship qualifiers, and
returns a deterministic graph digest for query-level provenance.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any, Mapping

from .canonical_graph import CanonicalGraph
from .scm_graph import SCMGraph
from .semantic_query import SemanticSupplyChainPath, semantic_supply_chain_paths


PROTOCOL_VERSION = "1.0.0"


class TemporalSemanticQueryError(ValueError):
    """Raised when a temporal semantic query violates its contract."""


@dataclass(frozen=True)
class TemporalSemanticQueryRequest:
    """Explicit inputs for a deterministic, read-only semantic query."""

    at: str
    from_id: str
    to_id: str
    predicates: tuple[str, ...] | None = None
    max_hops: int = 8

    def __post_init__(self) -> None:
        if not self.at:
            raise TemporalSemanticQueryError("at is required")
        if not self.from_id or not self.to_id:
            raise TemporalSemanticQueryError("from_id and to_id are required")
        if self.max_hops < 1:
            raise TemporalSemanticQueryError("max_hops must be >= 1")
        if self.predicates is not None:
            if any(not predicate for predicate in self.predicates):
                raise TemporalSemanticQueryError("predicates must not contain empty values")
            if tuple(sorted(set(self.predicates))) != self.predicates:
                raise TemporalSemanticQueryError("predicates must be sorted and unique")


@dataclass(frozen=True)
class TemporalSemanticQueryResponse:
    """Versioned query result with explicit snapshot provenance."""

    contract_version: str
    status: str
    query: TemporalSemanticQueryRequest
    paths: tuple[SemanticSupplyChainPath, ...]
    graph_digest: str


def _canonical_digest(graph: CanonicalGraph) -> str:
    return sha256(graph.to_json().encode("utf-8")).hexdigest()


def _canonical_graph(graph: CanonicalGraph | SCMGraph) -> CanonicalGraph:
    return graph.canonical if isinstance(graph, SCMGraph) else graph


def execute_temporal_semantic_query(
    graph: CanonicalGraph | SCMGraph,
    request: TemporalSemanticQueryRequest,
) -> TemporalSemanticQueryResponse:
    """Resolve a temporal semantic path without mutating the graph."""
    canonical = _canonical_graph(graph)
    predicates = set(request.predicates) if request.predicates is not None else None
    paths = semantic_supply_chain_paths(
        canonical,
        request.at,
        from_id=request.from_id,
        to_id=request.to_id,
        predicates=predicates,
        max_hops=request.max_hops,
    )
    paths = tuple(sorted(paths, key=lambda path: (path.node_ids, tuple(step.relationship_id for step in path.steps))))
    return TemporalSemanticQueryResponse(
        PROTOCOL_VERSION,
        "resolved" if paths else "not_found",
        request,
        paths,
        _canonical_digest(canonical),
    )


def _path_mapping(path: SemanticSupplyChainPath, graph_digest: str) -> dict[str, Any]:
    relationship_ids = tuple(step.relationship_id for step in path.steps)
    return {
        "at": path.at,
        "node_ids": list(path.node_ids),
        "steps": [
            {
                "relationship_id": step.relationship_id,
                "predicate": step.predicate,
                "from_id": step.from_id,
                "to_id": step.to_id,
                "qualifiers": dict(step.qualifiers),
            }
            for step in path.steps
        ],
        "provenance": {
            "graph_digest": graph_digest,
            "relationship_ids": list(relationship_ids),
        },
    }


def temporal_semantic_query_to_mapping(result: TemporalSemanticQueryResponse) -> dict[str, Any]:
    """Return a JSON-safe, deterministic mapping for the query contract."""
    return {
        "contract_version": result.contract_version,
        "status": result.status,
        "query": {
            "at": result.query.at,
            "from_id": result.query.from_id,
            "to_id": result.query.to_id,
            "predicates": list(result.query.predicates) if result.query.predicates is not None else None,
            "max_hops": result.query.max_hops,
        },
        "graph_digest": result.graph_digest,
        "paths": [_path_mapping(path, result.graph_digest) for path in result.paths],
    }
