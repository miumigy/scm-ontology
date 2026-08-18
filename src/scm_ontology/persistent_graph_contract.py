"""P8-A Persistent Graph Contract (Phase 8, SCM OS Persistent Graph).

Phase 8 turns the Canonical Graph runtime into a persistence-independent
production reference architecture. P8-A defines the **explicit persistence
semantics** that every backend (in-memory, relational, graph) must preserve,
while remaining transport-neutral:

  - nodes,
  - relationships,
  - relationship temporal versions,
  - evidence / provenance attachments,
  - temporal semantics (semantic validity vs. observation time).

The D8 ``PersistedGraphDocument`` is a normalized, content-addressed
representation of those persistence semantics. It is **not** Canonical Truth,
and it does **not** replace ``CanonicalGraph`` -- it is the backend-neutral
persistence view that later slices (P8-B relational, P8-C Neo4j, P8-D
snapshot/replay, P8-E index/scale) conform to.

Design rules honored:
  - backend-neutral (no database driver, no vendor schema);
  - provenance / evidence are first-class persistence semantics;
  - temporal state is preserved, not collapsed into a current edge;
  - deterministic and content-addressed (identical input -> identical document);
  - fail closed on missing identity, dangling endpoints, or scope;
  - does not mutate Canonical Truth and is read-only.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Literal, Mapping

from .canonical_graph import CanonicalGraph
from .evidence_provenance import EvidenceRef

PersistenceElementKind = Literal["node", "relationship", "relationship_version"]
PersistenceElementKinds = ("node", "relationship", "relationship_version")


class PersistentGraphContractError(ValueError):
    """Raised when persistence semantics are violated."""
    pass


@dataclass(frozen=True)
class PersistedElement:
    """One element of the persistence view with explicit semantics.

    ``kind`` classifies the element (node, relationship, or temporal
    relationship version). ``element_id`` is the stable identity under which a
    backend stores it. ``effective_at`` and ``observed_at`` separate semantic
    validity from observation time so temporal state is never collapsed.
    ``provenance`` carries the explicit evidence references that back the
    element; it never implies Canonical Truth.
    """

    kind: PersistenceElementKind
    element_id: str
    payload: Mapping[str, Any]
    effective_at: str | None = None
    valid_to: str | None = None
    observed_at: str | None = None
    provenance: tuple[EvidenceRef, ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in PersistenceElementKinds:
            raise PersistentGraphContractError(f"unsupported persistence element kind: {self.kind}")
        if not self.element_id.strip():
            raise PersistentGraphContractError("element_id must be non-empty")
        if not isinstance(self.payload, Mapping):
            raise PersistentGraphContractError("payload must be a mapping")


@dataclass(frozen=True)
class PersistedGraphDocument:
    """The content-addressed, backend-neutral persistence document.

    ``scope`` is the governed persistence scope (per S311). ``canonical_digest``
    anchors the document to the source ``CanonicalGraph`` so a backend can verify
    it persists the intended graph. ``document_digest`` content-addresses this
    exact persistence view.
    """

    scope: str
    canonical_digest: str
    elements: tuple[PersistedElement, ...]
    document_digest: str = ""

    def to_mapping(self) -> Mapping[str, Any]:
        return {
            "scope": self.scope,
            "canonical_digest": self.canonical_digest,
            "elements": [
                {
                    "kind": el.kind,
                    "element_id": el.element_id,
                    "payload": dict(el.payload),
                    **({"effective_at": el.effective_at} if el.effective_at is not None else {}),
                    **({"valid_to": el.valid_to} if el.valid_to is not None else {}),
                    **({"observed_at": el.observed_at} if el.observed_at is not None else {}),
                    **(
                        {
                            "provenance": [
                                dict({"source_ref": ref.source_ref}, **({"observed_at": ref.observed_at} if ref.observed_at is not None else {}), **({"metadata": dict(ref.metadata)} if ref.metadata else {}))
                                for ref in el.provenance
                            ]
                        }
                        if el.provenance
                        else {}
                    ),
                }
                for el in self.elements
            ],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )


def _digest(payload: str) -> str:
    return sha256(payload.encode("utf-8")).hexdigest()


def persistent_graph_document(
    graph: CanonicalGraph,
    *,
    scope: str,
    provenance: Mapping[str, tuple[EvidenceRef, ...]] | None = None,
) -> PersistedGraphDocument:
    """Build the explicit persistence view of a canonical graph.

    ``scope`` is a required, non-empty governed persistence scope. Optional
    ``provenance`` attaches explicit ``EvidenceRef`` provenance keyed by the
    element identity returned by :func:`persistence_element_id`.
    """
    if not scope.strip():
        raise PersistentGraphContractError("scope must be non-empty")
    provenance = provenance or {}

    canonical_digest = _digest(graph.to_json())
    elements: list[PersistedElement] = []

    for node in graph.nodes:
        elements.append(
            PersistedElement(
                kind="node",
                element_id=persistence_element_id("node", node.node_id),
                payload={"node_id": node.node_id, "node_type": node.node_type, **({"properties": dict(node.properties)} if node.properties else {})},
                provenance=provenance.get(persistence_element_id("node", node.node_id), ()),
            )
        )

    for rel in graph.relationships:
        rel_id = rel.instance.relationship_id
        elements.append(
            PersistedElement(
                kind="relationship",
                element_id=persistence_element_id("relationship", rel_id),
                payload={
                    "relationship_id": rel.instance.relationship_id,
                    "from_id": rel.instance.from_id,
                    "predicate": rel.instance.predicate,
                    "to_id": rel.instance.to_id,
                },
                provenance=provenance.get(persistence_element_id("relationship", rel_id), ()),
            )
        )
        for version in rel.versions:
            v_id = f"{rel_id}#v:{version.valid_from}"
            elements.append(
                PersistedElement(
                    kind="relationship_version",
                    element_id=persistence_element_id("relationship_version", v_id),
                    payload={
                        "relationship_id": rel_id,
                        "valid_from": version.valid_from,
                        **({"valid_to": version.valid_to} if version.valid_to is not None else {}),
                        **({"qualifiers": dict(version.qualifiers)} if version.qualifiers is not None else {}),
                    },
                    effective_at=version.valid_from,
                    valid_to=version.valid_to,
                    provenance=provenance.get(persistence_element_id("relationship_version", v_id), ()),
                )
            )

    _validate_dangling_references(graph, elements)
    doc = PersistedGraphDocument(
        scope=scope,
        canonical_digest=canonical_digest,
        elements=tuple(elements),
    )
    digest = _digest(doc.to_json())
    return PersistedGraphDocument(
        scope=scope,
        canonical_digest=canonical_digest,
        elements=tuple(elements),
        document_digest=digest,
    )


def persistence_element_id(kind: PersistenceElementKind, identity: str) -> str:
    """Return the stable persistence identity for an element."""
    if kind not in PersistenceElementKinds:
        raise PersistentGraphContractError(f"unsupported persistence element kind: {kind}")
    if not identity.strip():
        raise PersistentGraphContractError("element identity must be non-empty")
    return f"{kind}:{identity}"


def document_from_mapping(value: Mapping[str, Any]) -> PersistedGraphDocument:
    """Restore a persisted graph document from its mapping representation.

    Recomputes and validates the content digest (fail closed on tampering or
    lossy serialization).
    """
    try:
        scope = value["scope"]
        canonical_digest = value["canonical_digest"]
        elements = tuple(
            PersistedElement(
                kind=el["kind"],
                element_id=el["element_id"],
                payload=el.get("payload", {}),
                effective_at=el.get("effective_at"),
                valid_to=el.get("valid_to"),
                observed_at=el.get("observed_at"),
                provenance=tuple(
                    EvidenceRef(
                        source_ref=ref["source_ref"],
                        observed_at=ref.get("observed_at"),
                        metadata=ref.get("metadata", {}),
                    )
                    for ref in el.get("provenance", ())
                ),
            )
            for el in value["elements"]
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise PersistentGraphContractError(f"invalid persisted graph document: {exc}") from exc

    doc = PersistedGraphDocument(scope=scope, canonical_digest=canonical_digest, elements=elements)
    recomputed = _digest(doc.to_json())
    supplied = value.get("document_digest", "")
    if supplied and supplied != recomputed:
        raise PersistentGraphContractError("document digest mismatch")
    return PersistedGraphDocument(
        scope=scope,
        canonical_digest=canonical_digest,
        elements=elements,
        document_digest=recomputed,
    )


def _validate_dangling_references(
    graph: CanonicalGraph, elements: list[PersistedElement]
) -> None:
    node_ids = {node.node_id for node in graph.nodes}
    for el in elements:
        if el.kind in ("relationship", "relationship_version"):
            from_id = el.payload.get("from_id")
            to_id = el.payload.get("to_id")
            for ref in (from_id, to_id):
                if ref is not None and ref not in node_ids:
                    raise PersistentGraphContractError(
                        f"relationship endpoint {ref!r} is not present in the graph"
                    )


def element_by_id(
    document: PersistedGraphDocument, element_id: str
) -> PersistedElement | None:
    """Return the persisted element with the given stable identity, if present."""
    for el in document.elements:
        if el.element_id == element_id:
            return el
    return None
