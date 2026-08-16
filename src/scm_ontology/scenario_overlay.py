"""Governed what-if overlays over CanonicalGraph.

S320 defines a deliberately narrow scenario boundary: hypothetical relationship
changes are applied to an immutable derived graph view and can then be evaluated
by the existing temporal semantic query contract. The overlay never mutates
Canonical Truth and does not perform identity resolution, inference,
optimization, allocation, or execution.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any

from .canonical_graph import CanonicalGraph, CanonicalRelationship
from .temporal_semantic_query import (
    TemporalSemanticQueryRequest,
    TemporalSemanticQueryResponse,
    execute_temporal_semantic_query,
    temporal_semantic_query_to_mapping,
)


PROTOCOL_VERSION = "1.0.0"


class ScenarioOverlayError(ValueError):
    """Raised when a scenario overlay is invalid."""


@dataclass(frozen=True)
class ScenarioOperation:
    """One explicit hypothetical relationship mutation."""

    operation: str
    relationship: CanonicalRelationship

    def __post_init__(self) -> None:
        if self.operation not in {"add", "remove", "replace"}:
            raise ScenarioOverlayError("operation must be add, remove, or replace")


@dataclass(frozen=True)
class ScenarioOverlay:
    """Immutable, deterministic hypothetical view over a canonical graph."""

    scenario_id: str
    operations: tuple[ScenarioOperation, ...]

    def __post_init__(self) -> None:
        if not self.scenario_id.strip():
            raise ScenarioOverlayError("scenario_id must be non-empty")
        ids = [operation.relationship.instance.relationship_id for operation in self.operations]
        if len(ids) != len(set(ids)):
            raise ScenarioOverlayError("each relationship_id may occur in only one operation")

    def apply(self, graph: CanonicalGraph) -> CanonicalGraph:
        """Return a derived graph without changing the supplied graph."""
        relationships = {rel.instance.relationship_id: rel for rel in graph.relationships}
        for operation in self.operations:
            relationship_id = operation.relationship.instance.relationship_id
            exists = relationship_id in relationships
            if operation.operation == "add":
                if exists:
                    raise ScenarioOverlayError(f"cannot add existing relationship: {relationship_id}")
                relationships[relationship_id] = operation.relationship
            elif operation.operation == "remove":
                if not exists:
                    raise ScenarioOverlayError(f"cannot remove missing relationship: {relationship_id}")
                del relationships[relationship_id]
            else:
                if not exists:
                    raise ScenarioOverlayError(f"cannot replace missing relationship: {relationship_id}")
                relationships[relationship_id] = operation.relationship
        return CanonicalGraph(
            nodes=graph.nodes,
            relationships=tuple(sorted(relationships.values(), key=lambda rel: rel.instance.relationship_id)),
        )

    def digest(self) -> str:
        """Return a deterministic identity for the scenario definition."""
        payload = {
            "scenario_id": self.scenario_id,
            "operations": [
                {
                    "operation": operation.operation,
                    "relationship": operation.relationship.to_mapping(),
                }
                for operation in self.operations
            ],
        }
        import json
        encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return sha256(encoded.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ScenarioQueryResponse:
    """Versioned scenario result with base and scenario provenance."""

    contract_version: str
    scenario_id: str
    scenario_digest: str
    base_graph_digest: str
    query: TemporalSemanticQueryRequest
    result: TemporalSemanticQueryResponse


def execute_scenario_query(
    graph: CanonicalGraph,
    scenario: ScenarioOverlay,
    request: TemporalSemanticQueryRequest,
) -> ScenarioQueryResponse:
    """Evaluate a temporal semantic query against a hypothetical graph view."""
    base_digest = sha256(graph.to_json().encode("utf-8")).hexdigest()
    derived = scenario.apply(graph)
    result = execute_temporal_semantic_query(derived, request)
    return ScenarioQueryResponse(
        PROTOCOL_VERSION,
        scenario.scenario_id,
        scenario.digest(),
        base_digest,
        request,
        result,
    )


def scenario_query_to_mapping(response: ScenarioQueryResponse) -> dict[str, Any]:
    """Return a JSON-safe deterministic scenario response."""
    return {
        "contract_version": response.contract_version,
        "scenario_id": response.scenario_id,
        "scenario_digest": response.scenario_digest,
        "base_graph_digest": response.base_graph_digest,
        "query_result": temporal_semantic_query_to_mapping(response.result),
    }
