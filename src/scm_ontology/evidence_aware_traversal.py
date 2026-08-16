"""Evidence-aware traversal over the governed temporal semantic query surface.

S321 keeps evidence resolution outside Canonical Truth while making it possible
to require and expose supporting evidence for every relationship traversed by a
read-only semantic query.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .temporal_semantic_query import (
    PROTOCOL_VERSION,
    TemporalSemanticQueryRequest,
    execute_temporal_semantic_query,
)
from .canonical_graph import CanonicalGraph
from .scm_graph import SCMGraph


class EvidenceAwareTraversalError(ValueError):
    """Raised when evidence-aware traversal inputs are invalid."""


class EvidenceMissing(EvidenceAwareTraversalError):
    """Raised when a traversed relationship has no required evidence."""


@dataclass(frozen=True)
class EvidenceAwareTraversalRequest:
    """Temporal semantic query plus an explicit evidence requirement."""

    query: TemporalSemanticQueryRequest
    require_evidence: bool = True


@dataclass(frozen=True)
class EvidenceAwareStep:
    """A traversed relationship with its externally supplied evidence IDs."""

    relationship_id: str
    predicate: str
    from_id: str
    to_id: str
    qualifiers: Mapping[str, Any]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class EvidenceAwarePath:
    """A semantic path whose every relationship is evidence-accounted."""

    at: str
    node_ids: tuple[str, ...]
    steps: tuple[EvidenceAwareStep, ...]


@dataclass(frozen=True)
class EvidenceAwareTraversalResponse:
    """Versioned, deterministic evidence-aware traversal result."""

    contract_version: str
    status: str
    query: EvidenceAwareTraversalRequest
    paths: tuple[EvidenceAwarePath, ...]
    graph_digest: str


def _normalize_evidence_ids(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, (tuple, list, set, frozenset)):
        ids = tuple(str(item) for item in value)
        if any(not item for item in ids):
            raise EvidenceAwareTraversalError("evidence IDs must be non-empty")
        return tuple(sorted(set(ids)))
    raise EvidenceAwareTraversalError("evidence mapping values must be evidence IDs or iterables of IDs")


def execute_evidence_aware_traversal(
    graph: CanonicalGraph | SCMGraph,
    request: EvidenceAwareTraversalRequest,
    *,
    evidence_ids_by_relationship_id: Mapping[str, object],
) -> EvidenceAwareTraversalResponse:
    """Resolve temporal paths and attach externally governed evidence IDs.

    Evidence is deliberately supplied separately from the graph. This prevents
    traversal from silently turning provenance metadata into Canonical Truth.
    When ``require_evidence`` is true, a path is returned only if every step has
    at least one known evidence ID; otherwise ``EvidenceMissing`` fails closed.
    """
    query_result = execute_temporal_semantic_query(graph, request.query)
    paths: list[EvidenceAwarePath] = []
    for path in query_result.paths:
        steps: list[EvidenceAwareStep] = []
        for step in path.steps:
            evidence_ids = _normalize_evidence_ids(
                evidence_ids_by_relationship_id.get(step.relationship_id, ())
            )
            if request.require_evidence and not evidence_ids:
                raise EvidenceMissing(step.relationship_id)
            steps.append(
                EvidenceAwareStep(
                    step.relationship_id,
                    step.predicate,
                    step.from_id,
                    step.to_id,
                    dict(step.qualifiers),
                    evidence_ids,
                )
            )
        paths.append(EvidenceAwarePath(path.at, path.node_ids, tuple(steps)))

    return EvidenceAwareTraversalResponse(
        PROTOCOL_VERSION,
        "resolved" if paths else query_result.status,
        request,
        tuple(paths),
        query_result.graph_digest,
    )


def evidence_aware_traversal_to_mapping(
    result: EvidenceAwareTraversalResponse,
) -> dict[str, Any]:
    """Return a JSON-safe deterministic mapping."""
    return {
        "contract_version": result.contract_version,
        "status": result.status,
        "query": {
            "at": result.query.query.at,
            "from_id": result.query.query.from_id,
            "to_id": result.query.query.to_id,
            "predicates": list(result.query.query.predicates)
            if result.query.query.predicates is not None else None,
            "max_hops": result.query.query.max_hops,
            "require_evidence": result.query.require_evidence,
        },
        "graph_digest": result.graph_digest,
        "paths": [
            {
                "at": path.at,
                "node_ids": list(path.node_ids),
                "steps": [
                    {
                        "relationship_id": step.relationship_id,
                        "predicate": step.predicate,
                        "from_id": step.from_id,
                        "to_id": step.to_id,
                        "qualifiers": dict(step.qualifiers),
                        "evidence_ids": list(step.evidence_ids),
                    }
                    for step in path.steps
                ],
            }
            for path in result.paths
        ],
    }
