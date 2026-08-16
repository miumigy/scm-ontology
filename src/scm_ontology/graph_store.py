"""Transport-neutral graph-store adapter and deterministic reference store.

The adapter consumes an authorized PersistencePlan and a CanonicalGraph. It is
independent of any database vendor and preserves the explicit planned/applied
mutation boundary.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol

from .canonical_graph import CanonicalGraph
from .graph_persistence import PersistencePlan


@dataclass(frozen=True)
class GraphStoreWriteResult:
    """Auditable outcome of a graph-store execution."""

    plan_id: str
    graph_digest: str
    outcome: str
    replayed: bool = False


class GraphStoreAdapter(Protocol):
    """Minimal transport-neutral graph-store contract."""

    def apply(self, graph: CanonicalGraph, plan: PersistencePlan) -> GraphStoreWriteResult:
        ...


class InMemoryGraphStore:
    """Reference implementation used for deterministic tests and dry runs."""

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
