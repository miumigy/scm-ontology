"""Transport-neutral graph-store adapter with a deterministic in-memory reference implementation.

The adapter consumes an authorized PersistencePlan and a CanonicalGraph. It is
intentionally independent of Neo4j or any other graph database. The in-memory
implementation is suitable for tests and dry-run integration while preserving
idempotency and the explicit planned/applied boundary.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol

from .canonical_graph import CanonicalGraph
from .graph_persistence import PersistencePlan


@dataclass(frozen=True)
class GraphStoreWriteResult:
    """Outcome of a graph-store adapter execution."""

    plan_id: str
    graph_digest: str
    outcome: str
    replayed: bool = False


class GraphStoreAdapter(Protocol):
    """Minimal adapter contract for a concrete graph store."""

    def apply(self, graph: CanonicalGraph, plan: PersistencePlan) -> GraphStoreWriteResult:
        ...


class InMemoryGraphStore:
    """Reference adapter used to prove the execution boundary without a database."""

    def __init__(self) -> None:
        self._graphs: dict[str, str] = {}
        self._plans: dict[str, str] = {}

    def apply(self, graph: CanonicalGraph, plan: PersistencePlan) -> GraphStoreWriteResult:
        if plan.outcome != "planned":
            raise ValueError("only an authorized planned persistence intent may be applied")

        serialized = graph.to_json()
        digest = sha256(serialized.encode("utf-8")).hexdigest()
        if digest != plan.graph_digest:
            raise ValueError("graph digest does not match persistence plan")

        existing = self._plans.get(plan.plan_id)
        if existing is not None:
            if existing != digest:
                raise ValueError("idempotency key reused for a different graph")
            return GraphStoreWriteResult(plan.plan_id, digest, "applied", replayed=True)

        self._graphs[digest] = serialized
        self._plans[plan.plan_id] = digest
        return GraphStoreWriteResult(plan.plan_id, digest, "applied")

    def contains(self, graph_digest: str) -> bool:
        return graph_digest in self._graphs

    def graph_count(self) -> int:
        return len(self._graphs)
