from __future__ import annotations

from dataclasses import dataclass

from .canonical_graph import CanonicalGraph
from .path_constraints import PathEndsAt, evaluate_path_ends_at
from .path_evidence import PathEvidence, evidence_from_sources
from .path_reasoning_result import PathReasoningResult
from .relation_path_query import RelationPathQuery, query_relation_paths


class MultiHopReasoningError(ValueError):
    pass


@dataclass(frozen=True)
class MultiHopReasoningRequest:
    query: RelationPathQuery
    end_node_id: str | None = None
    source_refs: tuple[str, ...] = ()


def reason_over_paths(
    graph: CanonicalGraph,
    request: MultiHopReasoningRequest,
) -> PathReasoningResult:
    """Compose existing path query, constraint, and provenance into one result."""
    matches = (
        evaluate_path_ends_at(graph, request.query, PathEndsAt(request.end_node_id))
        if request.end_node_id is not None
        else query_relation_paths(graph, request.query)
    )
    evidenced: list[PathEvidence] = [
        evidence_from_sources(match, request.source_refs) for match in matches
    ]
    status = "matched" if evidenced else "no_match"
    return PathReasoningResult(
        result_ref=f"path-reasoning:{request.query.start_node_id}",
        status=status,
        paths=tuple(evidenced),
    )
