"""Deterministic, read-only projection runtime over Canonical Graph.

A projection is derived state, never Canonical Truth.  The runtime deliberately
keeps the contract small: a named projection definition, a deterministic
source digest, and a materialized JSON-safe payload with explicit lineage.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Callable, Mapping

from .canonical_graph import CanonicalGraph

PROTOCOL_VERSION = "1.0.0"


class ProjectionError(ValueError):
    """Raised when a projection contract is invalid or cannot be materialized."""


@dataclass(frozen=True)
class ProjectionDefinition:
    projection_id: str
    version: str
    projector: Callable[[CanonicalGraph], Mapping[str, Any]]

    def __post_init__(self) -> None:
        if not self.projection_id.strip():
            raise ProjectionError("projection_id must be non-empty")
        if not self.version.strip():
            raise ProjectionError("version must be non-empty")
        if not callable(self.projector):
            raise ProjectionError("projector must be callable")


@dataclass(frozen=True)
class ProjectionLineage:
    source_digest: str
    projection_id: str
    projection_version: str


@dataclass(frozen=True)
class ProjectionResult:
    contract_version: str
    status: str
    projection_id: str
    projection_version: str
    source_digest: str
    value: Mapping[str, Any]
    lineage: ProjectionLineage


def graph_digest(graph: CanonicalGraph) -> str:
    """Return the canonical SHA-256 digest used as projection lineage."""
    return hashlib.sha256(graph.to_json().encode("utf-8")).hexdigest()


def materialize_projection(graph: CanonicalGraph, definition: ProjectionDefinition) -> ProjectionResult:
    """Materialize a projection without mutating the supplied graph."""
    source_digest = graph_digest(graph)
    try:
        value = definition.projector(graph)
    except Exception as exc:  # noqa: BLE001 - normalize projector failures at boundary
        raise ProjectionError(f"projection failed: {exc}") from exc
    if not isinstance(value, Mapping):
        raise ProjectionError("projector must return a mapping")
    try:
        json.dumps(value, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ProjectionError(f"projection value is not JSON-serializable: {exc}") from exc
    lineage = ProjectionLineage(source_digest, definition.projection_id, definition.version)
    return ProjectionResult(PROTOCOL_VERSION, "materialized", definition.projection_id, definition.version, source_digest, dict(value), lineage)


def projection_to_mapping(result: ProjectionResult) -> dict[str, Any]:
    return {
        "contract_version": result.contract_version,
        "status": result.status,
        "projection_id": result.projection_id,
        "projection_version": result.projection_version,
        "source_digest": result.source_digest,
        "value": dict(result.value),
        "lineage": {
            "source_digest": result.lineage.source_digest,
            "projection_id": result.lineage.projection_id,
            "projection_version": result.lineage.projection_version,
        },
    }


def projection_to_json(result: ProjectionResult) -> str:
    return json.dumps(projection_to_mapping(result), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
