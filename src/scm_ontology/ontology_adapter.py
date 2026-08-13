"""Adapter between canonical ontology fixtures and simulation state.

The adapter preserves canonical entity identity and keeps relationship-scoped
properties separate from entity state. It is intentionally independent of
Neo4j and does not create new canonical ontology entities.
"""
from __future__ import annotations

from typing import Any, Mapping

from scm_ontology.simulation import State


class OntologyAdapterError(ValueError):
    """Raised when canonical data cannot be projected unambiguously."""


def project_canonical_state(dataset: Mapping[str, Any], *, state_id: str, effective_at: int = 0) -> State:
    """Project a canonical YAML-like dataset into a simulation State."""
    entities: dict[str, dict[str, Any]] = {}
    for node in dataset.get("nodes", []):
        node_id = node["id"]
        if node_id in entities:
            raise OntologyAdapterError(f"duplicate canonical node id: {node_id}")
        properties = dict(node.get("properties", {}))
        entities[node_id] = {"entityType": node["type"], **properties}

    relationship_states: dict[str, dict[str, Any]] = {}
    for edge in dataset.get("edges", []):
        from_id = edge["from"]
        to_id = edge["to"]
        if from_id not in entities or to_id not in entities:
            raise OntologyAdapterError(
                f"relationship endpoint not found: {edge['type']} {from_id} -> {to_id}"
            )
        properties = dict(edge.get("properties", {}))
        if not properties:
            continue
        relationship_id = relationship_state_id(edge["type"], from_id, to_id)
        if relationship_id in relationship_states:
            raise OntologyAdapterError(f"duplicate relationship projection: {relationship_id}")
        relationship_states[relationship_id] = {
            "relationshipType": edge["type"],
            "from": from_id,
            "to": to_id,
            **properties,
        }

    return State(
        state_id=state_id,
        effective_at=effective_at,
        entities=entities,
        relationship_states=relationship_states,
    )


def relationship_state_id(relationship_type: str, from_id: str, to_id: str) -> str:
    """Return a deterministic identity for a canonical relationship projection."""
    return f"REL:{relationship_type}:{from_id}:{to_id}"


def find_relationship_state(
    state: State, relationship_type: str, from_id: str, to_id: str
) -> Mapping[str, Any]:
    """Return one relationship projection without creating a new ontology entity."""
    return state.relationship_states[relationship_state_id(relationship_type, from_id, to_id)]
