"""Freshness and invalidation semantics for deterministic projections.

S324 makes the M8 projection lifecycle states observable without introducing
storage, scheduling, authorization, or Canonical Truth mutation.  Lifecycle
assessment is pure: it compares the materialized result with the current
Canonical Graph and projection definition.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from .canonical_graph import CanonicalGraph
from .projection_runtime import (
    PROTOCOL_VERSION,
    ProjectionDefinition,
    ProjectionResult,
    graph_digest,
    materialize_projection,
)

LIFECYCLE_STATES = frozenset(
    {"current", "stale", "rebuild_required", "failed", "invalid", "conflicted"}
)


class ProjectionLifecycleError(ValueError):
    """Raised when a projection lifecycle contract is invalid."""


@dataclass(frozen=True)
class ProjectionLifecycle:
    state: str
    reason: str
    contract_version: str
    projection_id: str
    projection_version: str
    source_digest: str

    def __post_init__(self) -> None:
        if self.state not in LIFECYCLE_STATES:
            raise ProjectionLifecycleError(f"unsupported lifecycle state: {self.state}")
        if not self.reason.strip():
            raise ProjectionLifecycleError("reason must be non-empty")
        if not self.projection_id.strip():
            raise ProjectionLifecycleError("projection_id must be non-empty")
        if not self.projection_version.strip():
            raise ProjectionLifecycleError("projection_version must be non-empty")
        if len(self.source_digest) != 64:
            raise ProjectionLifecycleError("source_digest must be a SHA-256 hex digest")


def assess_projection_freshness(
    graph: CanonicalGraph,
    definition: ProjectionDefinition,
    result: ProjectionResult,
) -> ProjectionLifecycle:
    """Classify a materialized projection against its current dependencies."""
    if result.contract_version != PROTOCOL_VERSION:
        return ProjectionLifecycle(
            "rebuild_required",
            "contract_version_mismatch",
            result.contract_version,
            result.projection_id,
            result.projection_version,
            result.source_digest,
        )
    if result.projection_id != definition.projection_id:
        return ProjectionLifecycle(
            "rebuild_required",
            "projection_id_mismatch",
            result.contract_version,
            result.projection_id,
            result.projection_version,
            result.source_digest,
        )
    if result.projection_version != definition.version:
        return ProjectionLifecycle(
            "rebuild_required",
            "projection_version_mismatch",
            result.contract_version,
            result.projection_id,
            result.projection_version,
            result.source_digest,
        )
    if result.status != "materialized":
        return ProjectionLifecycle(
            "invalid",
            "result_not_materialized",
            result.contract_version,
            result.projection_id,
            result.projection_version,
            result.source_digest,
        )

    current_digest = graph_digest(graph)
    if result.source_digest != current_digest:
        return ProjectionLifecycle(
            "stale",
            "source_digest_changed",
            result.contract_version,
            result.projection_id,
            result.projection_version,
            result.source_digest,
        )
    return ProjectionLifecycle(
        "current",
        "dependencies_match",
        result.contract_version,
        result.projection_id,
        result.projection_version,
        result.source_digest,
    )


def invalidate_projection(result: ProjectionResult, reason: str) -> ProjectionLifecycle:
    """Represent an explicit invalidation without mutating the result or graph."""
    return ProjectionLifecycle(
        "invalid",
        reason,
        result.contract_version,
        result.projection_id,
        result.projection_version,
        result.source_digest,
    )


def rebuild_projection(
    graph: CanonicalGraph, definition: ProjectionDefinition
) -> ProjectionResult:
    """Recompute a projection from Canonical Graph input.

    This is deliberately a pure recomputation primitive.  Authorization,
    persistence, scheduling, and governed recovery remain outside S324.
    """
    return materialize_projection(graph, definition)


def projection_lifecycle_to_mapping(result: ProjectionLifecycle) -> dict[str, Any]:
    return {
        "contract_version": result.contract_version,
        "state": result.state,
        "reason": result.reason,
        "projection_id": result.projection_id,
        "projection_version": result.projection_version,
        "source_digest": result.source_digest,
    }


def projection_lifecycle_to_json(result: ProjectionLifecycle) -> str:
    return json.dumps(
        projection_lifecycle_to_mapping(result),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
