"""Persistence boundary for versioned, transport-neutral canonical graphs."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol

from .canonical_graph import CanonicalGraph, CanonicalGraphError


class CanonicalGraphPersistenceError(ValueError):
    """Raised when a graph cannot be safely persisted or restored."""


@dataclass(frozen=True)
class StoredCanonicalGraph:
    """An immutable persisted graph snapshot with deterministic integrity metadata."""
    graph_id: str
    document: str
    graph_version: str = "1"
    schema_version: str = "1"
    canonical_identity: str = ""
    payload_integrity: str = ""


class CanonicalGraphStore(Protocol):
    def save(self, graph_id: str, graph: CanonicalGraph, *, graph_version: str = "1", schema_version: str = "1") -> StoredCanonicalGraph: ...
    def load(self, graph_id: str, *, graph_version: str | None = None) -> CanonicalGraph: ...
    def list_graph_ids(self) -> tuple[str, ...]: ...
    def list_versions(self, graph_id: str) -> tuple[str, ...]: ...
    def list_snapshots(self, graph_id: str) -> tuple[StoredCanonicalGraph, ...]: ...
    def latest_version(self, graph_id: str) -> str: ...


class InMemoryCanonicalGraphStore:
    """Reference store with immutable versioned snapshots."""
    def __init__(self) -> None:
        self._documents: dict[tuple[str, str], StoredCanonicalGraph] = {}

    def save(self, graph_id: str, graph: CanonicalGraph, *, graph_version: str = "1", schema_version: str = "1") -> StoredCanonicalGraph:
        _require_identifier(graph_id, "graph_id")
        _require_identifier(graph_version, "graph_version")
        _require_identifier(schema_version, "schema_version")
        if not isinstance(graph, CanonicalGraph):
            raise CanonicalGraphPersistenceError("graph must be a CanonicalGraph")
        try:
            document = graph.to_json()
        except CanonicalGraphError as exc:
            raise CanonicalGraphPersistenceError(str(exc)) from exc
        identity = graph_identity(graph)
        stored = StoredCanonicalGraph(graph_id, document, graph_version, schema_version, identity, identity)
        key = (graph_id, graph_version)
        existing = self._documents.get(key)
        if existing is not None:
            if existing == stored:
                return existing
            raise CanonicalGraphPersistenceError("graph version collision: existing snapshot differs")
        self._documents[key] = stored
        return stored

    def load(self, graph_id: str, *, graph_version: str | None = None) -> CanonicalGraph:
        _require_identifier(graph_id, "graph_id")
        if graph_version is not None:
            _require_identifier(graph_version, "graph_version")
            key = (graph_id, graph_version)
        else:
            key = (graph_id, self.latest_version(graph_id))
        try:
            stored = self._documents[key]
        except KeyError as exc:
            raise CanonicalGraphPersistenceError("graph version not found") from exc
        return _restore(stored)

    def list_graph_ids(self) -> tuple[str, ...]:
        return tuple(sorted({graph_id for graph_id, _ in self._documents}))

    def list_versions(self, graph_id: str) -> tuple[str, ...]:
        _require_identifier(graph_id, "graph_id")
        versions = tuple(sorted(
            (version for gid, version in self._documents if gid == graph_id),
            key=_version_sort_key,
            reverse=True,
        ))
        if not versions:
            raise CanonicalGraphPersistenceError("graph_id not found")
        return versions

    def list_snapshots(self, graph_id: str) -> tuple[StoredCanonicalGraph, ...]:
        versions = self.list_versions(graph_id)
        return tuple(self._documents[(graph_id, version)] for version in versions)

    def latest_version(self, graph_id: str) -> str:
        return self.list_versions(graph_id)[0]


def graph_identity(graph: CanonicalGraph) -> str:
    return sha256(graph.to_json().encode("utf-8")).hexdigest()


def _version_sort_key(version: str) -> tuple[tuple[int, object], ...]:
    """Sort versions naturally while remaining deterministic for arbitrary strings."""
    return tuple(
        (0, int(part)) if part.isdigit() else (1, part)
        for part in re.findall(r"\d+|\D+", version)
    )


def _restore(stored: StoredCanonicalGraph) -> CanonicalGraph:
    try:
        actual = sha256(stored.document.encode("utf-8")).hexdigest()
        if actual != stored.payload_integrity:
            raise CanonicalGraphPersistenceError("stored payload integrity mismatch")
        if actual != stored.canonical_identity:
            raise CanonicalGraphPersistenceError("stored graph identity mismatch")
        graph = CanonicalGraph.from_mapping(json.loads(stored.document))
        if graph_identity(graph) != stored.canonical_identity:
            raise CanonicalGraphPersistenceError("stored graph identity mismatch")
        return graph
    except CanonicalGraphPersistenceError:
        raise
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        raise CanonicalGraphPersistenceError("stored graph is invalid") from exc


def _require_identifier(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise CanonicalGraphPersistenceError(f"{field} must be non-empty")
