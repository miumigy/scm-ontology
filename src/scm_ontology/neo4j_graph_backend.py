"""P8-C Neo4j Reference Backend (Phase 8, SCM OS Persistent Graph).

P8-C is the *graph-backed* sibling of the P8-B relational backend. It implements
the same interchangeable ``PersistentGraphBackend`` interface over the P8-A
``PersistedGraphDocument`` contract, so P8-F can prove that InMemory, relational,
and graph backends produce equivalent canonical/query semantics.

The semantic core does **not** import the Neo4j driver. The application injects
two transport callables -- ``execute`` for writes (MERGE statements) and
``query`` for reads (RETURN statements) -- so driver/session/transaction
lifecycle stays outside the ontology (a test double provides an in-memory
"Neo4j" for deterministic tests).

Neo4j data model (graph-shaped, provenance as relationships):

    (:CanonicalPersistenceDocument {document_digest, scope, canonical_digest})
    (:CanonicalPersistenceElement {document_digest, position, element_id,
                                   kind, payload, effective_at, valid_to,
                                   observed_at})
    (:CanonicalPersistenceElement)-[:HAS_PROVENANCE {observed_at, metadata}]->(:CanonicalProvenance {source_ref})

Guarantees mirror P8-B: deterministic, content-addressed, idempotent write,
fail-closed digest validation, and byte-identical ``write -> read`` round-trip.
"""
from __future__ import annotations

from typing import Any, Callable, Mapping

from .persistent_graph_contract import (
    PersistedElement,
    PersistedGraphDocument,
    document_from_mapping,
)
from .relational_graph_backend import PersistentGraphBackendError


class Neo4jGraphBackendError(PersistentGraphBackendError):
    """Raised when a Neo4j persistence operation cannot complete safely."""
    pass


StatementExecutor = Callable[[str, Mapping[str, Any]], None]
RowQuery = Callable[[str, Mapping[str, Any]], tuple[tuple[Any, ...], ...]]


class Neo4jGraphBackend:
    """Graph-backed reference backend conforming to the P8-B interchange contract.

    ``execute`` issues Cypher writes; ``query`` returns a tuple of rows for read
    statements. Both are injected so no database driver is imported by the
    semantic core.
    """

    def __init__(self, execute: StatementExecutor, query: RowQuery) -> None:
        self._execute = execute
        self._query = query

    # ---- writes ----------------------------------------------------------

    def write(self, document: PersistedGraphDocument) -> PersistedGraphDocument:
        if not isinstance(document, PersistedGraphDocument):
            raise Neo4jGraphBackendError("document must be a PersistedGraphDocument")
        if not document.document_digest:
            raise Neo4jGraphBackendError("document_digest must be non-empty")

        # content-addressed integrity: recompute the document digest (deterministic)
        recomputed = document_from_mapping(document.to_mapping())
        if recomputed.document_digest != document.document_digest:
            raise Neo4jGraphBackendError("document digest mismatch")

        if self.contains(document.document_digest):
            return self.read(document.document_digest)

        self._execute(
            """
            MERGE (d:CanonicalDocument {document_digest: $digest})
            SET d.scope = $scope, d.canonical_digest = $canonical_digest
            """,
            {"digest": document.document_digest, "scope": document.scope,
             "canonical_digest": document.canonical_digest},
        )
        for position, el in enumerate(document.elements):
            self._execute(
                """MERGE (e:CanonicalElement {document_digest: $digest, element_id: $element_id})
                   SET e.position = $position, e.kind = $kind, e.payload = $payload,
                       e.effective_at = $effective_at, e.valid_to = $valid_to, e.observed_at = $observed_at
                """,
                {"digest": document.document_digest, "element_id": el.element_id,
                 "position": position, "kind": el.kind, "payload": _dumps(el.payload),
                 "effective_at": el.effective_at, "valid_to": el.valid_to, "observed_at": el.observed_at},
            )
            for ref in el.provenance:
                self._execute(
                    """MATCH (e:CanonicalElement {document_digest: $digest, element_id: $element_id})
                       MERGE (p:CanonicalProvenance {source_ref: $source_ref})
                       SET p.observed_at = $observed_at, p.metadata = $metadata
                       MERGE (e)-[hp:HAS_PROVENANCE]->(p)
                       SET hp.observed_at = $observed_at, hp.source_ref = $source_ref, hp.metadata = $metadata
                    """,
                    {"digest": document.document_digest, "element_id": el.element_id,
                     "source_ref": ref.source_ref, "observed_at": ref.observed_at,
                     "metadata": _dumps(ref.metadata) if ref.metadata else None},
                )
        return self.read(document.document_digest)

    # ---- reads -----------------------------------------------------------

    def read(self, document_digest: str) -> PersistedGraphDocument:
        doc_rows = self._query(
            "MATCH (d:CanonicalDocument {document_digest: $digest}) "
            "RETURN d.scope, d.canonical_digest",
            {"digest": document_digest},
        )
        if not doc_rows:
            raise Neo4jGraphBackendError("document_digest not found")
        if len(doc_rows) > 1:
            raise Neo4jGraphBackendError("duplicate document present in backend")
        scope, canonical_digest = doc_rows[0]

        el_rows = self._query(
            "MATCH (e:CanonicalElement {document_digest: $digest}) "
            "RETURN e.element_id, e.kind, e.payload, e.effective_at, e.valid_to, e.observed_at "
            "ORDER BY e.position",
            {"digest": document_digest},
        )
        prov_rows = self._query(
            "MATCH (e:CanonicalElement {document_digest: $digest})-[hp:HAS_PROVENANCE]->(p:CanonicalProvenance) "
            "RETURN e.element_id, hp.source_ref, hp.observed_at, hp.metadata "
            "ORDER BY e.element_id, hp.source_ref",
            {"digest": document_digest},
        )
        provenance_by_element: dict[str, list[dict[str, Any]]] = {}
        for element_id, source_ref, observed_at, metadata in prov_rows:
            provenance_by_element.setdefault(element_id, []).append(
                {"source_ref": source_ref, "observed_at": observed_at, "metadata": metadata}
            )

        elements: list[PersistedElement] = []
        for element_id, kind, payload, effective_at, valid_to, observed_at in el_rows:
            elements.append(
                PersistedElement(
                    kind=kind,
                    element_id=element_id,
                    payload=_loads(payload),
                    effective_at=effective_at,
                    valid_to=valid_to,
                    observed_at=observed_at,
                    provenance=_refs(provenance_by_element.get(element_id, [])),
                )
            )

        mapping = {
            "scope": scope,
            "canonical_digest": canonical_digest,
            "elements": [_el_mapping(el) for el in elements],
        }
        return document_from_mapping(mapping)

    # ---- queries ---------------------------------------------------------

    def contains(self, document_digest: str) -> bool:
        rows = self._query(
            "MATCH (d:CanonicalDocument {document_digest: $digest}) RETURN d.document_digest",
            {"digest": document_digest},
        )
        return bool(rows)

    def list_document_digests(self) -> tuple[str, ...]:
        rows = self._query(
            "MATCH (d:CanonicalDocument) RETURN d.document_digest ORDER BY d.document_digest",
            {},
        )
        return tuple(row[0] for row in rows)

    def element_count(self, document_digest: str) -> int:
        rows = self._query(
            "MATCH (e:CanonicalElement {document_digest: $digest}) RETURN count(e)",
            {"digest": document_digest},
        )
        return int(rows[0][0]) if rows else 0

    def elements_of_kind(self, document_digest: str, kind: str) -> tuple[PersistedElement, ...]:
        el_rows = self._query(
            "MATCH (e:CanonicalElement {document_digest: $digest, kind: $kind}) "
            "RETURN e.element_id, e.kind, e.payload, e.effective_at, e.valid_to, e.observed_at "
            "ORDER BY e.position",
            {"digest": document_digest, "kind": kind},
        )
        if not el_rows:
            return ()
        prov_rows = self._query(
            "MATCH (e:CanonicalElement {document_digest: $digest, kind: $kind})-[hp:HAS_PROVENANCE]->(p:CanonicalProvenance) "
            "RETURN e.element_id, hp.source_ref, hp.observed_at, hp.metadata "
            "ORDER BY e.element_id, hp.source_ref",
            {"digest": document_digest, "kind": kind},
        )
        provenance_by_element: dict[str, list[dict[str, Any]]] = {}
        for element_id, source_ref, observed_at, metadata in prov_rows:
            provenance_by_element.setdefault(element_id, []).append(
                {"source_ref": source_ref, "observed_at": observed_at, "metadata": metadata}
            )
        return tuple(
            PersistedElement(
                kind=kind,
                element_id=element_id,
                payload=_loads(payload),
                effective_at=effective_at,
                valid_to=valid_to,
                observed_at=observed_at,
                provenance=_refs(provenance_by_element.get(element_id, [])),
            )
            for element_id, kind, payload, effective_at, valid_to, observed_at in el_rows
        )

    # ---- P8-E index-backed query surface ---------------------------------

    def element_by_id(self, document_digest: str, element_id: str) -> PersistedElement | None:
        rows = self._query(
            "MATCH (e:CanonicalElement {document_digest: $digest, element_id: $element_id}) "
            "RETURN e.element_id, e.kind, e.payload, e.effective_at, e.valid_to, e.observed_at",
            {"digest": document_digest, "element_id": element_id},
        )
        if not rows:
            return None
        eid, kind, payload, effective_at, valid_to, observed_at = rows[0]
        return self._element_with_provenance(document_digest, eid, kind, payload,
                                             effective_at, valid_to, observed_at)

    def elements_effective_at(self, document_digest: str, effective_at: str) -> tuple[PersistedElement, ...]:
        rows = self._query(
            "MATCH (e:CanonicalElement {document_digest: $digest}) "
            "WHERE e.effective_at = $effective_at OR e.observed_at = $effective_at "
            "RETURN e.element_id, e.kind, e.payload, e.effective_at, e.valid_to, e.observed_at "
            "ORDER BY e.position",
            {"digest": document_digest, "effective_at": effective_at},
        )
        return tuple(self._element_with_provenance(document_digest, e, k, p, a, t, o)
                     for e, k, p, a, t, o in rows)

    def elements_with_provenance(self, document_digest: str, source_ref: str) -> tuple[PersistedElement, ...]:
        rows = self._query(
            "MATCH (e:CanonicalElement {document_digest: $digest})-[:HAS_PROVENANCE]->(p:CanonicalProvenance {source_ref: $source_ref}) "
            "RETURN DISTINCT e.element_id, e.kind, e.payload, e.effective_at, e.valid_to, e.observed_at "
            "ORDER BY e.position",
            {"digest": document_digest, "source_ref": source_ref},
        )
        return tuple(self._element_with_provenance(document_digest, e, k, p, a, t, o)
                     for e, k, p, a, t, o in rows)

    def _element_with_provenance(self, document_digest, element_id, kind, payload,
                                 effective_at, valid_to, observed_at) -> PersistedElement:
        prov_rows = self._query(
            "MATCH (e:CanonicalElement {document_digest: $digest, element_id: $element_id})-[hp:HAS_PROVENANCE]->(p:CanonicalProvenance) "
            "RETURN p.source_ref, hp.observed_at, hp.metadata ORDER BY p.source_ref",
            {"digest": document_digest, "element_id": element_id},
        )
        provenance = tuple(
            _ref_from_row(source_ref, observed_at, metadata)
            for source_ref, observed_at, metadata in prov_rows
        )
        return PersistedElement(
            kind=kind,
            element_id=element_id,
            payload=_loads(payload),
            effective_at=effective_at,
            valid_to=valid_to,
            observed_at=observed_at,
            provenance=provenance,
        )


def _ref_from_row(source_ref, observed_at, metadata):
    from .evidence_provenance import EvidenceRef

    return EvidenceRef(
        source_ref=source_ref,
        observed_at=observed_at,
        metadata=_loads(metadata) if metadata else {},
    )



def _dumps(value: Mapping[str, Any]) -> str:
    import json

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _loads(value: Any) -> Mapping[str, Any]:
    import json

    if isinstance(value, str):
        return json.loads(value)
    return dict(value)


def _refs(rows: list[dict[str, Any]]) -> tuple:
    from .evidence_provenance import EvidenceRef

    return tuple(
        EvidenceRef(
            source_ref=r["source_ref"],
            observed_at=r.get("observed_at"),
            metadata=_loads(r["metadata"]) if r.get("metadata") else {},
        )
        for r in rows
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


class InMemoryNeo4jTransport:
    """Deterministic in-memory 'Neo4j' reference transport.

    This interprets the statements emitted by :class:`Neo4jGraphBackend` and
    provides an ``execute`` / ``query`` pair, so tests and the P8-F acceptance
    path can exercise the graph backend without a real database or a driver.
    It is a reference transport, not a Cypher engine.
    """

    def __init__(self) -> None:
        self.documents: dict[str, dict] = {}
        self.elements: dict[str, dict[str, dict]] = {}
        self.provenance: dict[str, dict[str, list[tuple]]] = {}

    def execute(self, statement: str, params: Mapping[str, Any]) -> None:
        if "CanonicalDocument" in statement:
            self.documents[params["digest"]] = {
                "scope": params["scope"],
                "canonical_digest": params["canonical_digest"],
            }
        elif "CanonicalProvenance" in statement:
            self.provenance.setdefault(params["digest"], {}).setdefault(params["element_id"], []).append(
                (params["source_ref"], params.get("observed_at"), params.get("metadata"))
            )
        else:  # CanonicalElement
            self.elements.setdefault(params["digest"], {})[params["element_id"]] = {
                "position": params["position"],
                "kind": params["kind"],
                "payload": params["payload"],
                "effective_at": params.get("effective_at"),
                "valid_to": params.get("valid_to"),
                "observed_at": params.get("observed_at"),
            }

    def query(self, statement: str, params: Mapping[str, Any]) -> tuple[tuple[Any, ...], ...]:
        digest = params.get("digest")
        kind = params.get("kind")
        if "HAS_PROVENANCE" in statement and "hp.source_ref" in statement or "HAS_PROVENANCE" in statement and "p.source_ref" in statement:
            if digest not in self.provenance:
                return ()
            element_id_param = params.get("element_id")
            rows = []
            for element_id in sorted(self.provenance[digest]):
                if element_id_param is not None and element_id != element_id_param:
                    continue
                if kind is not None and self.elements.get(digest, {}).get(element_id, {}).get("kind") != kind:
                    continue
                for source_ref, observed_at, metadata in sorted(self.provenance[digest][element_id]):
                    rows.append((element_id, source_ref, observed_at, metadata))
            return tuple(rows)
        if "RETURN e.element_id, e.kind" in statement:
            els = self.elements.get(digest, {})
            if "element_id" in params:
                els = {k: v for k, v in els.items() if k == params["element_id"]}
            if kind is not None:
                els = {k: v for k, v in els.items() if v["kind"] == kind}
            ordered = sorted(els.items(), key=lambda kv: kv[1]["position"])
            return tuple(
                (element_id, props["kind"], props["payload"], props["effective_at"],
                 props["valid_to"], props["observed_at"])
                for element_id, props in ordered
            )
        if "count(" in statement and "CanonicalElement" in statement:
            els = self.elements.get(digest, {})
            if kind is not None:
                els = {k: v for k, v in els.items() if v["kind"] == kind}
            return ((len(els),),)
        if "RETURN d.scope" in statement:
            if digest not in self.documents:
                return ()
            d = self.documents[digest]
            return ((d["scope"], d["canonical_digest"]),)
        if "RETURN d.document_digest" in statement and "ORDER BY" not in statement and "CanonicalElement" not in statement:
            return ((digest,) if digest in self.documents else ())
        if "RETURN d.document_digest" in statement and "ORDER BY" in statement and "CanonicalElement" not in statement:
            return tuple((dg,) for dg in sorted(self.documents))
        if "WHERE e.effective_at" in statement or "e.effective_at = $effective_at" in statement:
            els = {k: v for k, v in self.elements.get(digest, {}).items()
                   if v.get("effective_at") == params.get("effective_at") or v.get("observed_at") == params.get("effective_at")}
            ordered = sorted(els.items(), key=lambda kv: kv[1]["position"])
            return tuple(
                (element_id, props["kind"], props["payload"], props["effective_at"],
                 props["valid_to"], props["observed_at"])
                for element_id, props in ordered
            )
        return ()
