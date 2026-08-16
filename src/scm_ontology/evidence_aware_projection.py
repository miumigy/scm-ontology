"""Evidence-aware projection runtime over the governed Canonical Graph.

S323 extends the deterministic S322 projection boundary without moving
provenance into Canonical Truth. Projection code receives an explicit evidence
context and must ask that context for evidence when it depends on a canonical
relationship. The runtime records exactly which relationship evidence was
consulted and preserves that mapping as derived projection lineage.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Callable, Mapping

from .canonical_graph import CanonicalGraph
from .projection_runtime import PROTOCOL_VERSION, ProjectionError, graph_digest


class EvidenceAwareProjectionError(ProjectionError):
    """Raised when an evidence-aware projection contract is invalid."""


class ProjectionEvidenceMissing(EvidenceAwareProjectionError):
    """Raised when a projection requests evidence that is not supplied."""


def _normalize_evidence_ids(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        if not value:
            raise EvidenceAwareProjectionError("evidence IDs must be non-empty")
        return (value,)
    if isinstance(value, (tuple, list, set, frozenset)):
        ids = tuple(str(item) for item in value)
        if any(not item for item in ids):
            raise EvidenceAwareProjectionError("evidence IDs must be non-empty")
        return tuple(sorted(set(ids)))
    raise EvidenceAwareProjectionError(
        "evidence mapping values must be evidence IDs or iterables of IDs"
    )


@dataclass
class EvidenceProjectionContext:
    """Explicit, read-only access to externally governed relationship evidence."""

    evidence_ids_by_relationship_id: Mapping[str, object]
    require_evidence: bool = True
    _accessed: set[str] = field(default_factory=set, init=False, repr=False)

    def evidence_ids(self, relationship_id: str) -> tuple[str, ...]:
        if not isinstance(relationship_id, str) or not relationship_id.strip():
            raise EvidenceAwareProjectionError("relationship_id must be non-empty")
        self._accessed.add(relationship_id)
        evidence_ids = _normalize_evidence_ids(
            self.evidence_ids_by_relationship_id.get(relationship_id, ())
        )
        if self.require_evidence and not evidence_ids:
            raise ProjectionEvidenceMissing(relationship_id)
        return evidence_ids

    @property
    def accessed_relationship_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._accessed))

    def accessed_evidence(self) -> dict[str, tuple[str, ...]]:
        return {
            relationship_id: self.evidence_ids(relationship_id)
            for relationship_id in self.accessed_relationship_ids
        }


@dataclass(frozen=True)
class EvidenceAwareProjectionDefinition:
    """Versioned projection definition with explicit evidence access."""

    projection_id: str
    version: str
    projector: Callable[[CanonicalGraph, EvidenceProjectionContext], Mapping[str, Any]]

    def __post_init__(self) -> None:
        if not self.projection_id.strip():
            raise EvidenceAwareProjectionError("projection_id must be non-empty")
        if not self.version.strip():
            raise EvidenceAwareProjectionError("version must be non-empty")
        if not callable(self.projector):
            raise EvidenceAwareProjectionError("projector must be callable")


@dataclass(frozen=True)
class EvidenceAwareProjectionLineage:
    source_digest: str
    projection_id: str
    projection_version: str
    evidence_by_relationship_id: Mapping[str, tuple[str, ...]]


@dataclass(frozen=True)
class EvidenceAwareProjectionResult:
    contract_version: str
    status: str
    projection_id: str
    projection_version: str
    source_digest: str
    value: Mapping[str, Any]
    evidence_by_relationship_id: Mapping[str, tuple[str, ...]]
    lineage: EvidenceAwareProjectionLineage


def materialize_evidence_aware_projection(
    graph: CanonicalGraph,
    definition: EvidenceAwareProjectionDefinition,
    *,
    evidence_ids_by_relationship_id: Mapping[str, object],
    require_evidence: bool = True,
) -> EvidenceAwareProjectionResult:
    """Materialize an evidence-aware projection without mutating Canonical Truth."""
    source_digest = graph_digest(graph)
    context = EvidenceProjectionContext(evidence_ids_by_relationship_id, require_evidence)
    try:
        value = definition.projector(graph, context)
    except ProjectionError:
        raise
    except Exception as exc:  # noqa: BLE001 - normalize projector failures at boundary
        raise EvidenceAwareProjectionError(f"projection failed: {exc}") from exc
    if not isinstance(value, Mapping):
        raise EvidenceAwareProjectionError("projector must return a mapping")

    evidence = context.accessed_evidence()
    try:
        json.dumps(value, ensure_ascii=False, sort_keys=True)
        json.dumps(evidence, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise EvidenceAwareProjectionError(
            f"projection result is not JSON-serializable: {exc}"
        ) from exc

    lineage = EvidenceAwareProjectionLineage(
        source_digest,
        definition.projection_id,
        definition.version,
        evidence,
    )
    return EvidenceAwareProjectionResult(
        PROTOCOL_VERSION,
        "materialized",
        definition.projection_id,
        definition.version,
        source_digest,
        dict(value),
        evidence,
        lineage,
    )


def evidence_aware_projection_to_mapping(
    result: EvidenceAwareProjectionResult,
) -> dict[str, Any]:
    """Return a deterministic JSON-safe mapping for the projection contract."""
    evidence = {
        key: list(value)
        for key, value in sorted(result.evidence_by_relationship_id.items())
    }
    return {
        "contract_version": result.contract_version,
        "status": result.status,
        "projection_id": result.projection_id,
        "projection_version": result.projection_version,
        "source_digest": result.source_digest,
        "value": dict(result.value),
        "evidence_by_relationship_id": evidence,
        "lineage": {
            "source_digest": result.lineage.source_digest,
            "projection_id": result.lineage.projection_id,
            "projection_version": result.lineage.projection_version,
            "evidence_by_relationship_id": {
                key: list(value)
                for key, value in sorted(result.lineage.evidence_by_relationship_id.items())
            },
        },
    }


def evidence_aware_projection_to_json(
    result: EvidenceAwareProjectionResult,
) -> str:
    return json.dumps(
        evidence_aware_projection_to_mapping(result),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
