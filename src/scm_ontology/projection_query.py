"""Governed read-only query boundary for materialized projections.

S325 accepts an already-materialized projection and exposes it only when its
identity, contract, and Canonical Graph dependency are current.  The query
boundary never refreshes, persists, authorizes, or mutates Canonical Truth.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical_graph import CanonicalGraph
from .projection_lifecycle import ProjectionLifecycle, assess_projection_freshness
from .projection_runtime import (
    PROTOCOL_VERSION,
    ProjectionDefinition,
    ProjectionResult,
    projection_to_mapping,
)


@dataclass(frozen=True)
class ProjectionQueryRequest:
    projection_id: str
    projection_version: str
    contract_version: str = PROTOCOL_VERSION


@dataclass(frozen=True)
class ProjectionQueryResponse:
    contract_version: str
    status: str
    projection: dict[str, Any] | None = None
    lifecycle: dict[str, Any] | None = None
    error: str | None = None


def _lifecycle_mapping(lifecycle: ProjectionLifecycle) -> dict[str, Any]:
    return {
        "state": lifecycle.state,
        "reason": lifecycle.reason,
        "contract_version": lifecycle.contract_version,
        "projection_id": lifecycle.projection_id,
        "projection_version": lifecycle.projection_version,
        "source_digest": lifecycle.source_digest,
    }


def execute_projection_query(
    request: ProjectionQueryRequest,
    *,
    graph: CanonicalGraph,
    definition: ProjectionDefinition,
    result: ProjectionResult,
) -> ProjectionQueryResponse:
    """Resolve a projection only when its governed lifecycle state is current."""
    if request.contract_version != PROTOCOL_VERSION:
        return ProjectionQueryResponse(
            PROTOCOL_VERSION,
            "contract_version_mismatch",
            error=request.contract_version,
        )
    if request.projection_id != definition.projection_id:
        return ProjectionQueryResponse(
            PROTOCOL_VERSION,
            "projection_mismatch",
            error=request.projection_id,
        )
    if request.projection_version != definition.version:
        return ProjectionQueryResponse(
            PROTOCOL_VERSION,
            "projection_mismatch",
            error=request.projection_version,
        )

    lifecycle = assess_projection_freshness(graph, definition, result)
    if lifecycle.state != "current":
        return ProjectionQueryResponse(
            PROTOCOL_VERSION,
            lifecycle.state,
            lifecycle=_lifecycle_mapping(lifecycle),
            error=lifecycle.reason,
        )

    return ProjectionQueryResponse(
        PROTOCOL_VERSION,
        "resolved",
        projection=projection_to_mapping(result),
        lifecycle=_lifecycle_mapping(lifecycle),
    )


def query_response_to_mapping(response: ProjectionQueryResponse) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "contract_version": response.contract_version,
        "status": response.status,
    }
    if response.projection is not None:
        payload["projection"] = response.projection
    if response.lifecycle is not None:
        payload["lifecycle"] = response.lifecycle
    if response.error is not None:
        payload["error"] = response.error
    return payload
