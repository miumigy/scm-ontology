"""Governed, transport-neutral persistence planning for CanonicalGraph.

This module deliberately stops before a graph-store write. It converts a
canonical graph into a deterministic persistence plan while requiring an
explicit authorization decision and scope. The plan is an intent artifact,
not Canonical Truth mutation.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Literal

from .canonical_graph import CanonicalGraph


PersistenceOutcome = Literal["planned", "rejected"]


@dataclass(frozen=True)
class PersistenceAuthorization:
    """Explicit authorization supplied by a caller outside the planner."""

    decision_id: str
    authorized: bool
    actor: str
    scope: str
    reason: str = ""

    def __post_init__(self) -> None:
        for name, value in (("decision_id", self.decision_id), ("actor", self.actor), ("scope", self.scope)):
            if not value.strip():
                raise ValueError(f"{name} must be non-empty")


@dataclass(frozen=True)
class PersistencePlan:
    """Deterministic, auditable intent to persist a canonical graph."""

    plan_id: str
    graph_digest: str
    decision_id: str
    actor: str
    scope: str
    outcome: PersistenceOutcome
    reason: str
    node_ids: tuple[str, ...]
    relationship_ids: tuple[str, ...]


class CanonicalGraphPersistencePlanner:
    """Build a persistence intent without mutating a graph store."""

    def plan(self, graph: CanonicalGraph, authorization: PersistenceAuthorization) -> PersistencePlan:
        graph_digest = sha256(graph.to_json().encode("utf-8")).hexdigest()
        payload = {
            "graph_digest": graph_digest,
            "decision_id": authorization.decision_id,
            "actor": authorization.actor,
            "scope": authorization.scope,
            "authorized": authorization.authorized,
        }
        plan_id = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        outcome: PersistenceOutcome = "planned" if authorization.authorized else "rejected"
        reason = authorization.reason or ("authorized" if authorization.authorized else "authorization rejected")
        return PersistencePlan(
            plan_id=plan_id,
            graph_digest=graph_digest,
            decision_id=authorization.decision_id,
            actor=authorization.actor,
            scope=authorization.scope,
            outcome=outcome,
            reason=reason,
            node_ids=tuple(node.node_id for node in graph.nodes),
            relationship_ids=tuple(rel.instance.relationship_id for rel in graph.relationships),
        )
