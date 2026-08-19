"""P8-B Relational Reference Backend (Phase 8, SCM OS Persistent Graph).

P8-B implements the P8-A ``PersistedGraphDocument`` contract on a durable,
normalized relational store. It is the *relational* sibling of the in-memory
reference store and the Neo4j adapter (P8-C), and it is what P8-F uses to prove
that interchangeable backends produce equivalent canonical/query semantics.

The backend is stdlib-only: it operates against an injected ``sqlite3``
connection (or a :memory: connection for deterministic tests) so that no
external database driver or service is required, and the semantic core stays
backend-neutral.

Relational schema (normalized, element-indexed):

    documents(document_digest PK, scope, canonical_digest)
    elements(document_digest, element_id, kind,
             payload_json, effective_at, valid_to, observed_at,
             PRIMARY KEY (document_digest, element_id))
    element_provenance(document_digest, element_id, source_ref,
                       observed_at, metadata_json,
                       PRIMARY KEY (document_digest, element_id, source_ref))

Each P8-A element (node / relationship / relationship_version) is a row in
``elements``; provenance attachments are rows in ``element_provenance``. Because
element_id / kind are first-class columns, a relational store can later index
and scale without leaking backend concepts into the ontology (P8-E).

Guarantees:
  - durable (committed transaction); write is atomic across all rows;
  - content-addressed: ``document_digest`` is the immutable primary key;
  - idempotent: re-writing the same digest does not duplicate data;
  - fail closed: a digest that does not match the supplied document is rejected;
  - round-trip faithful: write -> read reproduces an identical
    ``PersistedGraphDocument`` (payload, temporal fields, and provenance).
"""
from __future__ import annotations

import json
import sqlite3
from typing import Any, Mapping, Protocol, Protocol

from .persistent_graph_contract import (
    PersistedElement,
    PersistedGraphDocument,
    PersistentGraphContractError,
    document_from_mapping,
    persistence_element_id,
    persistent_graph_document,
)


class PersistentGraphBackendError(ValueError):
    """Base error for a Phase 8 persistence backend."""
    pass


class RelationalGraphBackendError(PersistentGraphBackendError):
    """Raised when a relational persistence operation cannot complete safely."""
    pass


class PersistentGraphBackend(Protocol):
    """Interchangeable Phase 8 persistent-graph backend contract.

    Both the relational (P8-B) and Neo4j (P8-C) reference backends implement
    this interface so P8-F can prove that interchangeable backends produce
    equivalent canonical/query semantics over identical P8-A documents.
    """

    def write(self, document: PersistedGraphDocument) -> PersistedGraphDocument: ...
    def read(self, document_digest: str) -> PersistedGraphDocument: ...
    def contains(self, document_digest: str) -> bool: ...
    def list_document_digests(self) -> tuple[str, ...]: ...
    def element_count(self, document_digest: str) -> int: ...
    def elements_of_kind(self, document_digest: str, kind: str) -> tuple[PersistedElement, ...]: ...
    def element_by_id(self, document_digest: str, element_id: str) -> PersistedElement | None: ...
    def elements_effective_at(self, document_digest: str, effective_at: str) -> tuple[PersistedElement, ...]: ...
    def elements_with_provenance(self, document_digest: str, source_ref: str) -> tuple[PersistedElement, ...]: ...


class ConnectionProvider(Protocol):
    """Backend-neutral connection/cursor provider."""

    def connect(self) -> Any:
        ...


def _dumps(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


_SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    document_digest TEXT PRIMARY KEY,
    scope TEXT NOT NULL,
    canonical_digest TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS elements (
    document_digest TEXT NOT NULL,
    position INTEGER NOT NULL,
    element_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    effective_at TEXT,
    valid_to TEXT,
    observed_at TEXT,
    PRIMARY KEY (document_digest, element_id),
    FOREIGN KEY (document_digest) REFERENCES documents(document_digest)
);
CREATE INDEX IF NOT EXISTS idx_elements_kind ON elements(kind);
CREATE INDEX IF NOT EXISTS idx_elements_element_id ON elements(element_id);
CREATE TABLE IF NOT EXISTS element_provenance (
    document_digest TEXT NOT NULL,
    element_id TEXT NOT NULL,
    source_ref TEXT NOT NULL,
    observed_at TEXT,
    metadata_json TEXT,
    PRIMARY KEY (document_digest, element_id, source_ref),
    FOREIGN KEY (document_digest, element_id)
        REFERENCES elements(document_digest, element_id)
);
"""


class RelationalGraphBackend:
    """Durable SQL-backed reference backend conforming to the P8-A contract.

    ``conn`` is an open ``sqlite3.Connection``. The backend owns its schema and
    writes atomically within a transaction on the supplied connection.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    # ---- writes ----------------------------------------------------------

    def write(self, document: PersistedGraphDocument) -> PersistedGraphDocument:
        """Persist a P8-A document atomically and content-addressed.

        Idempotent: writing the same ``document_digest`` again is a no-op and
        returns the existing stored document. A digest that does not match the
        supplied document (tampering / mismatch) is rejected.
        """
        if not isinstance(document, PersistedGraphDocument):
            raise RelationalGraphBackendError("document must be a PersistedGraphDocument")
        if not document.document_digest:
            raise RelationalGraphBackendError("document_digest must be non-empty")

        # content-addressed integrity: recompute the document digest from the
        # document's own mapping representation (deterministic, per P8-A).
        recomputed = document_from_mapping(document.to_mapping())
        if recomputed.document_digest != document.document_digest:
            raise RelationalGraphBackendError("document digest mismatch")

        try:
            cur = self._conn.execute(
                "SELECT scope, canonical_digest FROM documents WHERE document_digest = ?",
                (document.document_digest,),
            )
            row = cur.fetchone()
            if row is not None:
                return self.read(document.document_digest)

            self._conn.execute(
                "INSERT INTO documents (document_digest, scope, canonical_digest) VALUES (?, ?, ?)",
                (document.document_digest, document.scope, document.canonical_digest),
            )
            for position, el in enumerate(document.elements):
                self._conn.execute(
                    "INSERT INTO elements (document_digest, position, element_id, kind, payload_json, effective_at, valid_to, observed_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        document.document_digest,
                        position,
                        el.element_id,
                        el.kind,
                        _dumps(el.payload),
                        el.effective_at,
                        el.valid_to,
                        el.observed_at,
                    ),
                )
                for ref in el.provenance:
                    self._conn.execute(
                        "INSERT INTO element_provenance (document_digest, element_id, source_ref, observed_at, metadata_json) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (
                            document.document_digest,
                            el.element_id,
                            ref.source_ref,
                            ref.observed_at,
                            _dumps(ref.metadata) if ref.metadata else None,
                        ),
                    )
            self._conn.commit()
        except sqlite3.IntegrityError as exc:
            self._conn.rollback()
            raise RelationalGraphBackendError(f"relational backend integrity failure: {exc}") from exc

        return self.read(document.document_digest)

    # ---- reads -----------------------------------------------------------

    def read(self, document_digest: str) -> PersistedGraphDocument:
        """Reconstruct a P8-A document from relational rows."""
        cur = self._conn.execute(
            "SELECT scope, canonical_digest FROM documents WHERE document_digest = ?",
            (document_digest,),
        )
        doc_row = cur.fetchone()
        if doc_row is None:
            raise RelationalGraphBackendError("document_digest not found")

        scope, canonical_digest = doc_row
        cur = self._conn.execute(
            "SELECT element_id, kind, payload_json, effective_at, valid_to, observed_at "
            "FROM elements WHERE document_digest = ? ORDER BY position",
            (document_digest,),
        )
        elements: list[PersistedElement] = []
        for element_id, kind, payload_json, effective_at, valid_to, observed_at in cur:
            prov_cur = self._conn.execute(
                "SELECT source_ref, observed_at, metadata_json "
                "FROM element_provenance WHERE document_digest = ? AND element_id = ? ORDER BY source_ref",
                (document_digest, element_id),
            )
            provenance = tuple(
                _evidence_ref(source_ref, observed_at, metadata_json)
                for source_ref, observed_at, metadata_json in prov_cur
            )
            elements.append(
                PersistedElement(
                    kind=kind,
                    element_id=element_id,
                    payload=json.loads(payload_json),
                    effective_at=effective_at,
                    valid_to=valid_to,
                    observed_at=observed_at,
                    provenance=provenance,
                )
            )

        mapping = {
            "scope": scope,
            "canonical_digest": canonical_digest,
            "elements": [dict(el.to_mapping() if hasattr(el, "to_mapping") else _el_mapping(el)) for el in elements],
        }
        return document_from_mapping(mapping)

    # ---- queries ---------------------------------------------------------

    def contains(self, document_digest: str) -> bool:
        cur = self._conn.execute(
            "SELECT 1 FROM documents WHERE document_digest = ?", (document_digest,)
        )
        return cur.fetchone() is not None

    def list_document_digests(self) -> tuple[str, ...]:
        cur = self._conn.execute("SELECT document_digest FROM documents ORDER BY document_digest")
        return tuple(row[0] for row in cur)

    def element_count(self, document_digest: str) -> int:
        cur = self._conn.execute(
            "SELECT COUNT(*) FROM elements WHERE document_digest = ?", (document_digest,)
        )
        return int(cur.fetchone()[0])

    def elements_of_kind(self, document_digest: str, kind: str) -> tuple[PersistedElement, ...]:
        cur = self._conn.execute(
            "SELECT element_id, kind, payload_json, effective_at, valid_to, observed_at "
            "FROM elements WHERE document_digest = ? AND kind = ? ORDER BY element_id",
            (document_digest, kind),
        )
        result: list[PersistedElement] = []
        for element_id, k, payload_json, effective_at, valid_to, observed_at in cur:
            prov_cur = self._conn.execute(
                "SELECT source_ref, observed_at, metadata_json "
                "FROM element_provenance WHERE document_digest = ? AND element_id = ? ORDER BY source_ref",
                (document_digest, element_id),
            )
            provenance = tuple(
                _evidence_ref(source_ref, observed_at, metadata_json)
                for source_ref, observed_at, metadata_json in prov_cur
            )
            result.append(
                PersistedElement(
                    kind=k,
                    element_id=element_id,
                    payload=json.loads(payload_json),
                    effective_at=effective_at,
                    valid_to=valid_to,
                    observed_at=observed_at,
                    provenance=provenance,
                )
            )
        return tuple(result)

    def element_by_id(self, document_digest: str, element_id: str) -> PersistedElement | None:
        cur = self._conn.execute(
            "SELECT element_id, kind, payload_json, effective_at, valid_to, observed_at "
            "FROM elements WHERE document_digest = ? AND element_id = ?",
            (document_digest, element_id),
        )
        row = cur.fetchone()
        if row is None:
            return None
        element_id, kind, payload_json, effective_at, valid_to, observed_at = row
        return self._element_with_provenance(document_digest, element_id, kind, payload_json, effective_at, valid_to, observed_at)

    def elements_effective_at(self, document_digest: str, effective_at: str) -> tuple[PersistedElement, ...]:
        cur = self._conn.execute(
            "SELECT element_id, kind, payload_json, effective_at, valid_to, observed_at "
            "FROM elements WHERE document_digest = ? AND (effective_at = ? OR observed_at = ?) ORDER BY position",
            (document_digest, effective_at, effective_at),
        )
        return tuple(self._element_with_provenance(document_digest, e, k, p, a, t, o)
                     for e, k, p, a, t, o in cur)

    def elements_with_provenance(self, document_digest: str, source_ref: str) -> tuple[PersistedElement, ...]:
        cur = self._conn.execute(
            "SELECT DISTINCT e.element_id, e.kind, e.payload_json, e.effective_at, e.valid_to, e.observed_at "
            "FROM elements e JOIN element_provenance p ON p.document_digest = e.document_digest AND p.element_id = e.element_id "
            "WHERE e.document_digest = ? AND p.source_ref = ? ORDER BY e.position",
            (document_digest, source_ref),
        )
        return tuple(self._element_with_provenance(document_digest, e, k, p, a, t, o)
                     for e, k, p, a, t, o in cur)

    def _element_with_provenance(self, document_digest, element_id, kind, payload_json, effective_at, valid_to, observed_at) -> PersistedElement:
        prov_cur = self._conn.execute(
            "SELECT source_ref, observed_at, metadata_json "
            "FROM element_provenance WHERE document_digest = ? AND element_id = ? ORDER BY source_ref",
            (document_digest, element_id),
        )
        provenance = tuple(
            _evidence_ref(source_ref, observed_at, metadata_json)
            for source_ref, observed_at, metadata_json in prov_cur
        )
        return PersistedElement(
            kind=kind,
            element_id=element_id,
            payload=json.loads(payload_json),
            effective_at=effective_at,
            valid_to=valid_to,
            observed_at=observed_at,
            provenance=provenance,
        )


def _el_mapping(el: PersistedElement) -> dict[str, Any]:
    result: dict[str, Any] = {"kind": el.kind, "element_id": el.element_id, "payload": dict(el.payload)}
    if el.effective_at is not None:
        result["effective_at"] = el.effective_at
    if el.valid_to is not None:
        result["valid_to"] = el.valid_to
    if el.observed_at is not None:
        result["observed_at"] = el.observed_at
    if el.provenance:
        result["provenance"] = [
            dict({"source_ref": ref.source_ref}, **({"observed_at": ref.observed_at} if ref.observed_at is not None else {}), **({"metadata": dict(ref.metadata)} if ref.metadata else {}))
            for ref in el.provenance
        ]
    return result


def _evidence_ref(source_ref: str, observed_at: str | None, metadata_json: str | None):
    from .evidence_provenance import EvidenceRef

    return EvidenceRef(
        source_ref=source_ref,
        observed_at=observed_at,
        metadata=json.loads(metadata_json) if metadata_json else {},
    )
