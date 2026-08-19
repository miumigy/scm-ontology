"""P8-D Snapshot / Version / Replay (Phase 8, SCM OS Persistent Graph).

P8-D adds deterministic, replayable versioning on top of any P8-A/P8-B/P8-C
persistent graph backend. A ``PersistentSnapshot`` capture is content-addressed
and immutable; the ``VersionedGraphBackend`` wraps an interchangeable
``PersistentGraphBackend`` and records, for each ``graph_id``, an append-only
sequence of versions that can be replayed to reproduce an exact
``PersistedGraphDocument`` (or the underlying ``CanonicalGraph``).

Guarantees:
  - deterministic: identical (document, graph_id, version) -> identical snapshot
    identity and replay output;
  - replayable: any recorded version reproduces the exact document;
  - immutable / append-only version index: recorded versions cannot be mutated;
  - fail closed: empty graph_id/version, version collisions with a different
    document, and missing versions are all rejected;
  - backend-neutral: works against the relational (P8-B), Neo4j (P8-C), or any
    ``PersistentGraphBackend`` implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Protocol

from .canonical_graph import CanonicalGraph
from .persistent_graph_contract import PersistedGraphDocument


class SnapshotError(ValueError):
    """Raised when a snapshot cannot be captured or replayed safely."""
    pass


@dataclass(frozen=True)
class PersistentSnapshot:
    """An immutable, content-addressed capture of one graph version."""

    snapshot_id: str
    graph_id: str
    version: str
    document_digest: str
    document_json: str
    created_at: str = ""

    def to_mapping(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "graph_id": self.graph_id,
            "version": self.version,
            "document_digest": self.document_digest,
            "created_at": self.created_at,
        }


class PersistentGraphBackend(Protocol):
    """The interchangeable Phase 8 backend interface (relational / Neo4j)."""

    def write(self, document: PersistedGraphDocument) -> PersistedGraphDocument: ...
    def read(self, document_digest: str) -> PersistedGraphDocument: ...
    def contains(self, document_digest: str) -> bool: ...
    def list_document_digests(self) -> tuple[str, ...]: ...
    def element_count(self, document_digest: str) -> int: ...
    def elements_of_kind(self, document_digest: str, kind: str) -> tuple: ...


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _snapshot_id(graph_id: str, version: str, document_digest: str, created_at: str = "") -> str:
    payload = _dumps(
        {"graph_id": graph_id, "version": version, "document_digest": document_digest, "created_at": created_at}
    )
    return sha256(payload.encode("utf-8")).hexdigest()


class VersionedGraphBackend:
    """Wrap a ``PersistentGraphBackend`` with immutable versioning + replay."""

    def __init__(self, backend: PersistentGraphBackend) -> None:
        self._backend = backend
        # graph_id -> ordered dict version -> snapshot_id
        self._version_index: dict[str, dict[str, str]] = {}
        self._snapshots: dict[str, PersistentSnapshot] = {}

    # ---- capture ---------------------------------------------------------

    def capture(
        self,
        document: PersistedGraphDocument,
        *,
        graph_id: str,
        version: str,
        created_at: str = "",
    ) -> PersistentSnapshot:
        """Persist a document version and record a deterministic snapshot."""
        _require_identifier(graph_id, "graph_id")
        _require_identifier(version, "version")
        if not isinstance(document, PersistedGraphDocument) or not document.document_digest:
            raise SnapshotError("document must be a non-empty PersistedGraphDocument")

        # persist through the underlying backend (idempotent / content-addressed)
        self._backend.write(document)

        sid = _snapshot_id(graph_id, version, document.document_digest, created_at)
        snapshot = PersistentSnapshot(
            snapshot_id=sid,
            graph_id=graph_id,
            version=version,
            document_digest=document.document_digest,
            document_json=document.to_json(),
            created_at=created_at,
        )

        # append-only version index; reject a version collision with a different document
        index = self._version_index.setdefault(graph_id, {})
        existing = index.get(version)
        if existing is not None and existing != sid:
            raise SnapshotError(
                f"version collision for graph {graph_id!r} version {version!r}: snapshot already recorded with a different document"
            )
        index[version] = sid
        self._snapshots[sid] = snapshot
        return snapshot

    # ---- replay ----------------------------------------------------------

    def replay(self, graph_id: str, version: str) -> PersistedGraphDocument:
        """Reproduce the exact persisted document for a recorded version."""
        _require_identifier(graph_id, "graph_id")
        _require_identifier(version, "version")
        index = self._version_index.get(graph_id)
        if index is None:
            raise SnapshotError(f"no versions recorded for graph {graph_id!r}")
        sid = index.get(version)
        if sid is None:
            raise SnapshotError(f"version {version!r} not found for graph {graph_id!r}")
        snapshot = self._snapshots[sid]
        return self._backend.read(snapshot.document_digest)

    def replay_graph(self, graph_id: str, version: str) -> CanonicalGraph:
        """Replay a version and reconstruct the underlying ``CanonicalGraph``."""
        doc = self.replay(graph_id, version)
        return CanonicalGraph.from_mapping(_graph_mapping(doc))

    # ---- queries ---------------------------------------------------------

    def list_versions(self, graph_id: str) -> tuple[str, ...]:
        _require_identifier(graph_id, "graph_id")
        index = self._version_index.get(graph_id)
        if not index:
            raise SnapshotError(f"no versions recorded for graph {graph_id!r}")
        return tuple(index)

    def latest_version(self, graph_id: str) -> str:
        versions = self.list_versions(graph_id)
        return versions[-1]

    def snapshot(self, graph_id: str, version: str) -> PersistentSnapshot | None:
        _require_identifier(graph_id, "graph_id")
        _require_identifier(version, "version")
        sid = self._version_index.get(graph_id, {}).get(version)
        return self._snapshots.get(sid) if sid is not None else None


def _require_identifier(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SnapshotError(f"{field} must be non-empty")


def _graph_mapping(document: PersistedGraphDocument) -> dict[str, Any]:
    """Reconstruct a canonical graph mapping from the persisted elements.

    Nodes became ``node`` elements; relationships and versions become
    ``relationship`` / ``relationship_version`` elements. This reproduces the
    canonical graph shape that a ``CanonicalGraph`` can parse.
    """
    nodes: list[dict[str, Any]] = []
    rels: dict[str, dict[str, Any]] = {}
    for el in document.elements:
        if el.kind == "node":
            nodes.append(
                {
                    "id": el.payload["node_id"],
                    "type": el.payload["node_type"],
                    **({"properties": dict(el.payload["properties"])} if "properties" in el.payload else {}),
                }
            )
        elif el.kind == "relationship":
            rels[el.payload["relationship_id"]] = {
                "id": el.payload["relationship_id"],
                "from": el.payload["from_id"],
                "predicate": el.payload["predicate"],
                "to": el.payload["to_id"],
                "versions": [],
            }
        elif el.kind == "relationship_version":
            rid = el.payload["relationship_id"]
            version_rec = {
                "valid_from": el.payload["valid_from"],
                **({"valid_to": el.payload["valid_to"]} if "valid_to" in el.payload else {}),
                **({"qualifiers": dict(el.payload["qualifiers"])} if "qualifiers" in el.payload else {}),
            }
            if rid not in rels:
                raise SnapshotError(f"relationship version references unknown relationship {rid!r}")
            rels[rid]["versions"].append(version_rec)
    return {"nodes": nodes, "relationships": list(rels.values())}
