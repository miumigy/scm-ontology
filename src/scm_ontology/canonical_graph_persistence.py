"""Persistence boundary for versioned, transport-neutral canonical graphs."""
from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol

from .canonical_graph import CanonicalGraph, CanonicalGraphError


class CanonicalGraphPersistenceError(ValueError):
    """Raised when a graph cannot be safely persisted or restored."""


@dataclass(frozen=True)
class StoredCanonicalGraph:
    """A persisted graph snapshot with deterministic integrity metadata."""

    graph_id: str
    document: str
    graph_version: str = "1"
    schema_version: str = "1"
    canonical_identity: str = ""
    payload_integrity: str = ""


class CanonicalGraphStore(Protocol):
    """Minimal storage contract; implementations may use any backend."""

    def save(
        self,
        graph_id: str,
        graph: CanonicalGraph,
        *,
        graph_version: str = "1",
        schema_version: str = "1",
    ) -> StoredCanonicalGraph: ...

    def load(self, graph_id: str) -> CanonicalGraph: ...


class InMemoryCanonicalGraphStore:
    """Reference store used for tests and lightweight applications."""

    def __init__(self) -> None:
        self._documents: dict[str, StoredCanonicalGraph] = {}

    def save(
        self,
        graph_id: str,
        graph: CanonicalGraph,
        *,
        graph_version: str = "1",
        schema_version: str = "1",
    ) -> StoredCanonicalGraph:
        _require_identifier(graph_id, "graph_id")
        _require_identifier(graph_version, "graph_version")
        _require_identifier(schema_version, "schema_version")
        if not isinstance(graph, CanonicalGraph):
            raise CanonicalGraphPersistenceError("graph must be a CanonicalGraph")
        try:
            document = graph.to_json()
        except CanonicalGraphError as exc:
            raise CanonicalGraphPersistenceError(str(exc)) from exc
        identity = sha256(document.encode("utf-8")).hexdigest()
        stored = StoredCanonicalGraph(
            graph_id=graph_id,
            document=document,
            graph_version=graph_version,
            schema_version=schema_version,
            canonical_identity=identity,
            payload_integrity=sha256(document.encode("utf-8")).hexdigest(),
        )
        self._documents[graph_id] = stored
        return stored

    def load(self, graph_id: str) -> CanonicalGraph:
        _require_identifier(graph_id, "graph_id")
        try:
            stored = self._documents[graph_id]
        except KeyError as exc:
            raise CanonicalGraphPersistenceError("graph_id not found") from exc
        try:
            actual_integrity = sha256(stored.document.encode("utf-8")).hexdigest()
            if actual_integrity != stored.payload_integrity:
                raise CanonicalGraphPersistenceError("stored payload integrity mismatch")
            if actual_integrity != stored.canonical_identity:
                raise CanonicalGraphPersistenceError("stored graph identity mismatch")
            value = json.loads(stored.document)
            graph = CanonicalGraph.from_mapping(value)
            if graph_identity(graph) != stored.canonical_identity:
                raise CanonicalGraphPersistenceError("stored graph identity mismatch")
            return graph
        except CanonicalGraphPersistenceError:
            raise
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            raise CanonicalGraphPersistenceError("stored graph is invalid") from exc


def graph_identity(graph: CanonicalGraph) -> str:
    """Return the deterministic SHA-256 identity of a canonical graph."""
    return sha256(graph.to_json().encode("utf-8")).hexdigest()


def _require_identifier(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise CanonicalGraphPersistenceError(f"{field} must be non-empty")
