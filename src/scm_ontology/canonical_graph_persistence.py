"""Persistence boundary for the transport-neutral canonical graph contract."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol

from .canonical_graph import CanonicalGraph, CanonicalGraphError


class CanonicalGraphPersistenceError(ValueError):
    """Raised when a graph cannot be safely persisted or restored."""


@dataclass(frozen=True)
class StoredCanonicalGraph:
    """A persisted graph document with its canonical content identity."""

    graph_id: str
    document: str


class CanonicalGraphStore(Protocol):
    """Minimal storage contract; implementations may use any backend."""

    def save(self, graph_id: str, graph: CanonicalGraph) -> StoredCanonicalGraph: ...

    def load(self, graph_id: str) -> CanonicalGraph: ...


class InMemoryCanonicalGraphStore:
    """Reference store used for tests and lightweight applications."""

    def __init__(self) -> None:
        self._documents: dict[str, StoredCanonicalGraph] = {}

    def save(self, graph_id: str, graph: CanonicalGraph) -> StoredCanonicalGraph:
        if not isinstance(graph_id, str) or not graph_id.strip():
            raise CanonicalGraphPersistenceError("graph_id must be non-empty")
        if not isinstance(graph, CanonicalGraph):
            raise CanonicalGraphPersistenceError("graph must be a CanonicalGraph")
        try:
            document = graph.to_json()
        except CanonicalGraphError as exc:
            raise CanonicalGraphPersistenceError(str(exc)) from exc
        stored = StoredCanonicalGraph(graph_id=graph_id, document=document)
        self._documents[graph_id] = stored
        return stored

    def load(self, graph_id: str) -> CanonicalGraph:
        if not isinstance(graph_id, str) or not graph_id.strip():
            raise CanonicalGraphPersistenceError("graph_id must be non-empty")
        try:
            stored = self._documents[graph_id]
        except KeyError as exc:
            raise CanonicalGraphPersistenceError("graph_id not found") from exc
        try:
            import json

            value = json.loads(stored.document)
            graph = CanonicalGraph.from_mapping(value)
            if graph_identity(graph) != sha256(stored.document.encode("utf-8")).hexdigest():
                raise CanonicalGraphPersistenceError("stored graph identity mismatch")
            return graph
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            raise CanonicalGraphPersistenceError("stored graph is invalid") from exc


def graph_identity(graph: CanonicalGraph) -> str:
    """Return the deterministic SHA-256 identity of a canonical graph."""
    return sha256(graph.to_json().encode("utf-8")).hexdigest()
