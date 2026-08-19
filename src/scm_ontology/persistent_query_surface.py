"""P8-E Scale / Index Boundary (Phase 8, SCM OS Persistent Graph).

P8-E makes the query/index expectations of the persistent graph explicit and
backend-neutral, so that scale and indexing do not leak backend-specific
concepts into the ontology. It defines the exact query surface that any
backend (in-memory, relational P8-B, Neo4j P8-C) must satisfy, and proves that
the document-level surface and the backend-level surface produce identical
results for identical P8-A documents.

The query surface is intentionally small and semantic:

  - element_by_id(element_id)          -- stable identity lookup
  - elements_of_kind(kind)             -- node / relationship / version
  - elements_effective_at(effective_at)-- temporal-validity lookup
  - elements_with_provenance(source_ref)-- provenance / evidence lookup
  - element_count()                     -- cardinality

INDEX_EXPECTATIONS records exactly which predicates a conforming backend may
index (element_id, kind, effective_at, provenance source_ref) -- the boundary
beyond which backend-specific storage is *not* part of the ontology.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .persistent_graph_contract import PersistedElement, PersistedGraphDocument

# Index expectations: a conforming backend is *allowed* to index these
# predicates; anything else is backend-specific and not part of the ontology.
INDEX_EXPECTATIONS: dict[str, str] = {
    "element_id": "stable element identity (node / relationship / version)",
    "kind": "element kind: node | relationship | relationship_version",
    "effective_at": "semantic validity time (relationship_version validity)",
    "source_ref": "provenance / evidence source reference",
}


class PersistentQuerySurfaceError(ValueError):
    """Raised when a query cannot be answered from the persistence view."""
    pass


class PersistentQuerySurface(Protocol):
    """Backend-neutral query contract every persistent backend must satisfy."""

    def element_by_id(self, element_id: str) -> PersistedElement | None: ...
    def elements_of_kind(self, kind: str) -> tuple[PersistedElement, ...]: ...
    def elements_effective_at(self, effective_at: str) -> tuple[PersistedElement, ...]: ...
    def elements_with_provenance(self, source_ref: str) -> tuple[PersistedElement, ...]: ...
    def element_count(self) -> int: ...


class DocumentQuerySurface:
    """Reference query surface over a P8-A ``PersistedGraphDocument``.

    This is the backend-independent baseline: given the same document, the same
    query answers the same way regardless of what stored it.
    """

    def __init__(self, document: PersistedGraphDocument) -> None:
        self._document = document

    def element_by_id(self, element_id: str) -> PersistedElement | None:
        for el in self._document.elements:
            if el.element_id == element_id:
                return el
        return None

    def elements_of_kind(self, kind: str) -> tuple[PersistedElement, ...]:
        return tuple(el for el in self._document.elements if el.kind == kind)

    def elements_effective_at(self, effective_at: str) -> tuple[PersistedElement, ...]:
        return tuple(
            el for el in self._document.elements
            if el.effective_at == effective_at or el.observed_at == effective_at
        )

    def elements_with_provenance(self, source_ref: str) -> tuple[PersistedElement, ...]:
        return tuple(
            el for el in self._document.elements
            if any(ref.source_ref == source_ref for ref in el.provenance)
        )

    def element_count(self) -> int:
        return len(self._document.elements)


class BackedQuerySurface:
    """Query surface driven through an interchangeable persistent backend.

    This consumes the backend's own ``read`` / ``elements_of_kind`` /
    ``element_by_id`` where available, exercising the backend's index rather
    than the in-memory document. For methods a backend may not expose, it falls
    back to the document reconstructed from ``read``.
    """

    def __init__(self, backend: Any, document_digest: str) -> None:
        self._backend = backend
        self._document_digest = document_digest
        self._document = backend.read(document_digest)

    def element_by_id(self, element_id: str) -> PersistedElement | None:
        if hasattr(self._backend, "element_by_id"):
            return self._backend.element_by_id(self._document_digest, element_id)
        return DocumentQuerySurface(self._document).element_by_id(element_id)

    def elements_of_kind(self, kind: str) -> tuple[PersistedElement, ...]:
        if hasattr(self._backend, "elements_of_kind"):
            return self._backend.elements_of_kind(self._document_digest, kind)
        return DocumentQuerySurface(self._document).elements_of_kind(kind)

    def elements_effective_at(self, effective_at: str) -> tuple[PersistedElement, ...]:
        if hasattr(self._backend, "elements_effective_at"):
            return self._backend.elements_effective_at(self._document_digest, effective_at)
        return DocumentQuerySurface(self._document).elements_effective_at(effective_at)

    def elements_with_provenance(self, source_ref: str) -> tuple[PersistedElement, ...]:
        if hasattr(self._backend, "elements_with_provenance"):
            return self._backend.elements_with_provenance(self._document_digest, source_ref)
        return DocumentQuerySurface(self._document).elements_with_provenance(source_ref)

    def element_count(self) -> int:
        if hasattr(self._backend, "element_count"):
            return self._backend.element_count(self._document_digest)
        return len(self._document.elements)


@dataclass(frozen=True)
class QueryEquivalenceReport:
    """Deterministic result of comparing query surfaces across backends."""

    query: str
    expected: tuple[str, ...]
    observed: tuple[tuple[str, ...], ...]
    equivalent: bool


def _serialize_elements(elements: tuple[PersistedElement, ...]) -> tuple[str, ...]:
    return tuple(el.element_id for el in elements)


def element_by_id(backend: Any, digest: str, element_id: str) -> PersistedElement | None:
    """Convenience factory: element lookup over a backed query surface."""
    return BackedQuerySurface(backend, digest).element_by_id(element_id)


QUERIES = (
    ("element_count",),
    ("elements_of_kind", "node"),
    ("elements_of_kind", "relationship"),
    ("elements_of_kind", "relationship_version"),
)
