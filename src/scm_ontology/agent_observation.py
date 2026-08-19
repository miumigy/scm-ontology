"""P10-A — Agent Observation Boundary.

Agents receive scoped, evidence-aware observations rather than unrestricted
graph mutation access. This slice composes the existing S337 graph projection,
S338 graph query, and S339 graph-to-reasoning observation boundaries into an
explicit read-only ``AgentObservation`` envelope bound to an agent scope.

An ``AgentObservation`` is immutable, content-addressed, carries the exact
scope (query filters), the evidence/provenance that produced it, and exposes no
write/mutate path. It never re-interprets canonical facts: the observation
payload is exactly the deterministic graph query projection, projected through
the existing graph-to-reasoning boundary.

P10-A introduces no new canonical semantics and performs no mutation. It is
purely a read boundary that makes the agent surface explicit, scoped, and
auditable before reasoning begins.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

from .graph_projection import GraphProjection
from .graph_query import query_nodes, query_relationships
from .graph_reasoning_projection import GraphReasoningObservation


class AgentObservationError(ValueError):
    """Raised when an agent observation violates the P10-A contract."""


@dataclass(frozen=True)
class AgentScope:
    """Explicit, bounded read scope granted to one agent for one question."""

    question_id: str
    agent_id: str
    node_type: str | None = None
    node_id: str | None = None
    relationship_type: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.question_id, str) or not self.question_id.strip():
            raise AgentObservationError("question_id must be non-empty")
        if not isinstance(self.agent_id, str) or not self.agent_id.strip():
            raise AgentObservationError("agent_id must be non-empty")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "question_id": self.question_id,
            "agent_id": self.agent_id,
            "node_type": self.node_type,
            "node_id": self.node_id,
            "relationship_type": self.relationship_type,
        }


@dataclass(frozen=True)
class AgentObservation:
    """Immutable, scoped, evidence-aware observation delivered to one agent."""

    scope: AgentScope
    observation: GraphReasoningObservation
    observation_id: str

    @property
    def can_write(self) -> bool:
        """Agents never receive a mutation surface through this boundary."""
        return False

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P10A.1",
            "observation_id": self.observation_id,
            "can_write": False,
            "scope": self.scope.to_mapping(),
            "observation": {
                "question_id": self.observation.question_id,
                "value": self.observation.value,
                "evidence_ids": list(self.observation.evidence_ids),
                "provenance_ids": list(self.observation.provenance_ids),
            },
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _observation_id(scope: AgentScope, observation: GraphReasoningObservation) -> str:
    payload = json.dumps(
        {
            "scope": scope.to_mapping(),
            "observation": {
                "question_id": observation.question_id,
                "value": observation.value,
                "evidence_ids": list(observation.evidence_ids),
                "provenance_ids": list(observation.provenance_ids),
            },
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return sha256(payload.encode()).hexdigest()


def build_agent_observation(
    projection: GraphProjection,
    *,
    question_id: str,
    agent_id: str,
    node_type: str | None = None,
    node_id: str | None = None,
    relationship_type: str | None = None,
    evidence_ids: tuple[str, ...] = (),
) -> AgentObservation:
    """Construct a scoped, read-only, evidence-aware agent observation.

    The observation is always a deterministic projection of an
    already-validated canonical graph projection and carries no write path.
    Mutating the canonical graph remains outside an agent's reach — an agent
    can request a scoped read, never a graph mutation.
    """
    if not isinstance(projection, GraphProjection):
        raise AgentObservationError("projection must be a GraphProjection")
    if not isinstance(question_id, str) or not question_id.strip():
        raise AgentObservationError("question_id must be non-empty")
    if not isinstance(agent_id, str) or not agent_id.strip():
        raise AgentObservationError("agent_id must be non-empty")

    scope = AgentScope(
        question_id=question_id,
        agent_id=agent_id,
        node_type=node_type,
        node_id=node_id,
        relationship_type=relationship_type,
    )

    # Apply the exact scope as a deterministic graph query.
    result = query_nodes(
        projection,
        node_type=node_type,
        node_id=node_id,
    )
    if relationship_type is not None:
        result = query_relationships(
            projection,
            relationship_type=relationship_type,
            node_id=node_id,
        )

    observation = GraphReasoningObservation(
        question_id=question_id,
        value={
            "nodes": [node.to_mapping() for node in result.nodes],
            "relationships": [rel.to_mapping() for rel in result.relationships],
        },
        evidence_ids=evidence_ids,
        provenance_ids=result.provenance_ids,
    )
    return AgentObservation(
        scope=scope,
        observation=observation,
        observation_id=_observation_id(scope, observation),
    )
