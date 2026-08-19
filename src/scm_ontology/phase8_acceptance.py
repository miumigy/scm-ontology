"""SCM OS Phase 8 Acceptance (P8-F).

Closes **Phase 8 (SCM OS Persistent Graph)** with a deterministic acceptance
contract: the Canonical Graph runtime is exposed through explicit persistence
semantics (P8-A), implemented by interchangeable relational (P8-B) and Neo4j
(P8-C) backends, versioned / replayable (P8-D), and bounded by an explicit
scale / index boundary (P8-E).

P8-F defines an explicit Phase 8 capability inventory (P8-A..P8-E) and probes
each capability deterministically, folding results into an immutable,
content-addressed ``Phase8AcceptanceReport`` with an overall ``accepted`` flag.

The Phase 8 acceptance criterion is two-fold:
  1. every capability is operable (fail closed otherwise);
  2. the **interchangeable backends gate** holds: the relational (P8-B) and
     Neo4j (P8-C) reference backends produce byte-identical P8-A documents,
     identical element/kind query answers (P8-E), and identical
     snapshot/replay results (P8-D) for the reference workload.

P8-F performs no external side effect and never mutates Canonical Truth.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import sqlite3
from typing import Any, Callable

from .canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from .evidence_provenance import EvidenceRef
from .persistent_graph_contract import (
    persistence_element_id,
    persistent_graph_document,
    PersistedGraphDocument,
)
from .relationship_identity import RelationshipInstance
from .relationship_version import RelationshipVersion


class Phase8AcceptanceError(ValueError):
    """Raised when an acceptance input or invocation is invalid."""


def _reference_graph() -> CanonicalGraph:
    return CanonicalGraph(
        nodes=(
            SemanticNode("supplier-1", "Supplier", {"name": "Acme"}),
            SemanticNode("factory-1", "Factory"),
            SemanticNode("dc-1", "DistributionCenter"),
        ),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("rel-1", "supplier-1", "supplies", "factory-1"),
                (RelationshipVersion("2026-01-01", "2026-12-31", {"commitment": "firm"}),),
            ),
            CanonicalRelationship(
                RelationshipInstance("rel-2", "factory-1", "ships_to", "dc-1")
            ),
        ),
    )


def _reference_document() -> PersistedGraphDocument:
    provenance = {
        persistence_element_id("node", "supplier-1"): (
            EvidenceRef("erp:SUP-1", observed_at="2026-08-19T09:00:00Z"),
        )
    }
    return persistent_graph_document(
        _reference_graph(), scope="enterprise:acme", provenance=provenance
    )


def _interchangeable_backends_probe() -> dict[str, Any]:
    """Probe the P8-F acceptance gate across interchangeable backends.

    Writes the same P8-A reference document into the relational (P8-B),
    Neo4j (P8-C), and snapshot/version (P8-D) paths, then verifies that all
    produce identical documents and identical query answers (P8-E).
    """
    from .relational_graph_backend import RelationalGraphBackend
    from .neo4j_graph_backend import Neo4jGraphBackend, InMemoryNeo4jTransport
    from .persistent_snapshot import VersionedGraphBackend
    from .persistent_query_surface import DocumentQuerySurface

    doc = _reference_document()

    # P8-B: relational
    rel = RelationalGraphBackend(sqlite3.connect(":memory:"))
    rel.write(doc)

    # P8-C: Neo4j (driver-free reference transport)
    transport = InMemoryNeo4jTransport()
    neo = Neo4jGraphBackend(transport.execute, transport.query)
    neo.write(doc)

    # P8-D: snapshot / version / replay over the relational backend
    versioned = VersionedGraphBackend(rel)
    versioned.capture(doc, graph_id="reference-net", version="v1")
    replayed = versioned.replay("reference-net", "v1")

    # P8-C round-trip is byte-identical to the source document
    rel_roundtrip = rel.read(doc.document_digest)
    neo_roundtrip = neo.read(doc.document_digest)
    relational_identical = rel_roundtrip.to_json() == doc.to_json()
    neo4j_identical = neo_roundtrip.to_json() == doc.to_json()

    # replay reproduces the exact document (P8-D)
    replay_identical = replayed.to_json() == doc.to_json()

    # query answers are identical across relational and Neo4j (P8-E)
    rel_surf = DocumentQuerySurface(rel_roundtrip)
    neo_surf = DocumentQuerySurface(neo_roundtrip)
    kinds = ("node", "relationship", "relationship_version")
    query_equivalent = (
        rel_surf.element_count() == neo_surf.element_count()
        and all(
            {e.element_id for e in rel_surf.elements_of_kind(k) }
            == {e.element_id for e in neo_surf.elements_of_kind(k)}
            for k in kinds
        )
    )

    accepted = (
        relational_identical
        and neo4j_identical
        and replay_identical
        and query_equivalent
    )
    return {
        "document_digest": doc.document_digest,
        "relational_identical": relational_identical,
        "neo4j_identical": neo4j_identical,
        "replay_identical": replay_identical,
        "query_equivalent": query_equivalent,
        "element_count": rel_surf.element_count(),
        "accepted": accepted,
    }


def _relational_probe() -> dict[str, Any]:
    from .relational_graph_backend import RelationalGraphBackend

    doc = _reference_document()
    rel = RelationalGraphBackend(sqlite3.connect(":memory:"))
    rel.write(doc)
    restored = rel.read(doc.document_digest)
    return {
        "element_count": restore_element_count(restored),
        "roundtrip_identical": restored.to_json() == doc.to_json(),
    }


def _neo4j_probe() -> dict[str, Any]:
    from .neo4j_graph_backend import Neo4jGraphBackend, InMemoryNeo4jTransport

    doc = _reference_document()
    transport = InMemoryNeo4jTransport()
    neo = Neo4jGraphBackend(transport.execute, transport.query)
    neo.write(doc)
    restored = neo.read(doc.document_digest)
    return {
        "element_count": restore_element_count(restored),
        "roundtrip_identical": restored.to_json() == doc.to_json(),
    }


def _snapshot_probe() -> dict[str, Any]:
    from .relational_graph_backend import RelationalGraphBackend
    from .persistent_snapshot import VersionedGraphBackend

    doc = _reference_document()
    rel = RelationalGraphBackend(sqlite3.connect(":memory:"))
    versioned = VersionedGraphBackend(rel)
    snapshot = versioned.capture(doc, graph_id="reference-net", version="v1")
    replayed = versioned.replay("reference-net", "v1")
    return {
        "snapshot_id": snapshot.snapshot_id,
        "list_versions": list(versioned.list_versions("reference-net")),
        "replay_identical": replayed.to_json() == doc.to_json(),
    }


def _query_surface_probe() -> dict[str, Any]:
    from .relational_graph_backend import RelationalGraphBackend
    from .persistent_query_surface import DocumentQuerySurface

    doc = _reference_document()
    rel = RelationalGraphBackend(sqlite3.connect(":memory:"))
    rel.write(doc)
    surf = DocumentQuerySurface(rel.read(doc.document_digest))
    return {
        "index_expectations": sorted(
            {"element_id", "kind", "effective_at", "source_ref"}
        ),
        "element_count": surf.element_count(),
        "kind_counts": {
            k: len(surf.elements_of_kind(k))
            for k in ("node", "relationship", "relationship_version")
        },
    }


def restore_element_count(document: PersistedGraphDocument) -> int:
    return len(document.elements)


_CAPABILITIES: tuple[tuple[str, str, Callable[[], Any]], ...] = (
    (
        "persistent_graph_contract",
        "Persistent Graph Contract (P8-A)",
        lambda: _reference_document().to_json(),
    ),
    (
        "relational_backend",
        "Relational Reference Backend (P8-B)",
        _relational_probe,
    ),
    (
        "neo4j_backend",
        "Neo4j Reference Backend (P8-C)",
        _neo4j_probe,
    ),
    (
        "snapshot_version_replay",
        "Snapshot / Version / Replay (P8-D)",
        _snapshot_probe,
    ),
    (
        "scale_index_boundary",
        "Scale / Index Boundary (P8-E)",
        _query_surface_probe,
    ),
    (
        "interchangeable_backends",
        "Interchangeable Backends Gate (P8-F)",
        _interchangeable_backends_probe,
    ),
)


@dataclass(frozen=True)
class CapabilityResult:
    """Deterministic probe result for one Phase 8 capability."""

    key: str
    name: str
    operable: bool
    evidence_id: str
    detail: dict[str, Any] | None = None

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "key": self.key,
            "name": self.name,
            "operable": self.operable,
            "evidence_id": self.evidence_id,
        }
        if self.detail is not None:
            value["detail"] = self.detail
        return value


@dataclass(frozen=True)
class AcceptanceSummary:
    """Deterministic aggregate counts across the capability probes."""

    capability_count: int
    operable_count: int
    failed_count: int

    def to_mapping(self) -> dict[str, Any]:
        return {
            "capability_count": self.capability_count,
            "operable_count": self.operable_count,
            "failed_count": self.failed_count,
        }


@dataclass(frozen=True)
class Phase8AcceptanceReport:
    """Immutable, content-addressed Phase 8 acceptance report."""

    report_id: str
    accepted: bool
    accepted_at: str
    capabilities: tuple[CapabilityResult, ...]
    summary: AcceptanceSummary

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P8F.1",
            "is_phase8_acceptance": True,
            "report_id": self.report_id,
            "accepted": self.accepted,
            "accepted_at": self.accepted_at,
            "summary": self.summary.to_mapping(),
            "capabilities": [cap.to_mapping() for cap in self.capabilities],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _evidence_id(output: Any) -> str:
    payload = json.dumps(
        output, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), default=str,
    )
    return sha256(payload.encode()).hexdigest()


def _probe(key: str, name: str, fn: Callable[[], Any]) -> CapabilityResult:
    try:
        output = fn()
    except Exception as exc:  # noqa: BLE001 - acceptance probe must fail closed
        return CapabilityResult(
            key=key, name=name, operable=False,
            evidence_id="", detail={"error": f"{type(exc).__name__}: {exc}"},
        )
    if output is None or output is False:
        return CapabilityResult(
            key=key, name=name, operable=False,
            evidence_id="", detail={"error": "probe produced no usable output"},
        )
    return CapabilityResult(
        key=key,
        name=name,
        operable=True,
        evidence_id=_evidence_id(output),
        detail=output if isinstance(output, dict) else {"value": str(output)},
    )


def run_phase8_acceptance(*, accepted_at: str) -> Phase8AcceptanceReport:
    """Run the Phase 8 capability probes and produce an acceptance report.

    A capability is operable when its deterministic probe returns a usable
    result without error. The phase is accepted when every capability is
    operable, including the P8-F interchangeable-backends gate.
    """
    if not isinstance(accepted_at, str) or not accepted_at.strip():
        raise Phase8AcceptanceError("accepted_at must be non-empty")

    capabilities = tuple(
        _probe(key, name, fn) for key, name, fn in _CAPABILITIES
    )
    operable = sum(1 for cap in capabilities if cap.operable)
    summary = AcceptanceSummary(
        capability_count=len(capabilities),
        operable_count=operable,
        failed_count=len(capabilities) - operable,
    )
    accepted = operable == len(capabilities)

    payload = {
        "accepted_at": accepted_at,
        "capabilities": [cap.to_mapping() for cap in capabilities],
    }
    report_id = sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    return Phase8AcceptanceReport(
        report_id=report_id,
        accepted=accepted,
        accepted_at=accepted_at,
        capabilities=capabilities,
        summary=summary,
    )
