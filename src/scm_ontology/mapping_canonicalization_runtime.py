"""P7-B Mapping / Canonicalization Runtime (Phase 7, SCM OS Real Data Plane).

Deterministic, configuration-driven source-to-canonical mapping that consumes
the ``SourceEvidence`` produced by the P7-A Reference Data Adapter and emits
explicit ``CanonicalizationResult`` records.

P7-B is the *mapping* side of the data plane. It DOES NOT:

  - resolve identity across source systems (that is P7-C);
  - run data-quality / freshness gates (P7-D);
  - mutate Canonical Truth or the Canonical Ontology (``canonical_mutation`` is
    always ``False`` here).

A mapping rule encodes *explicit* correspondence from a source system's
representations to existing canonical concepts. It never infers a mapping from
field names, spelling, similarity, or adapter success, and it never promotes a
source-system representation to canonical semantics by itself. A result is a
mapping decision, not a Canonical Fact.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Mapping, Sequence

from .reference_canonicalization import CanonicalizationError
from .reference_data_adapter import SourceDataset, SourceEvidence


class MappingRuntimeError(ValueError):
    """Raised when a mapping rule or invocation is invalid."""


class MappingState(str):
    """Explicit, non-null decision states (S261/S262 vocabulary)."""

    MAPPED = "mapped"
    AMBIGUOUS = "ambiguous"
    UNMAPPABLE = "unmappable"
    REJECTED = "rejected"
    UNSUPPORTED = "unsupported"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    CONFLICTING_SEMANTICS = "conflicting_semantics"


class SemanticGap(str):
    """Semantic-gap classification from the S255 boundary contract."""

    NONE = "none"
    NO_CANONICAL_TARGET = "no_canonical_target"
    AMBIGUOUS_MAPPING = "ambiguous_mapping"
    VENDOR_SPECIFIC_SEMANTICS = "vendor_specific_semantics"
    GRANULARITY_MISMATCH = "granularity_mismatch"
    TEMPORAL_MISMATCH = "temporal_mismatch"
    AUTHORITY_INSUFFICIENT = "authority_insufficient"


@dataclass(frozen=True)
class Transform:
    """Explicit representation normalization; never business-meaning invention.

    ``code_map`` translates source codes/units into canonical representations
    only when an explicit equivalence is declared. Unknown source codes are a
    gap, never silently promoted.
    """

    name: str
    kind: str
    code_map: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise MappingRuntimeError("transform name must be non-empty")
        if self.kind not in ("code", "unit"):
            raise MappingRuntimeError(f"unsupported transform kind: {self.kind}")
        if any(not str(key) or not str(value) for key, value in self.code_map.items()):
            raise MappingRuntimeError("transform code_map entries must be non-empty")

    @property
    def is_passthrough(self) -> bool:
        return not self.code_map

    def apply(self, value: Any) -> Any:
        if self.is_passthrough or value is None:
            return value
        if not isinstance(value, str):
            raise MappingRuntimeError(f"transform {self.name!r} requires a string value")
        mapped = self.code_map.get(value)
        if mapped is None:
            raise MappingRuntimeError(
                f"transform {self.name!r} has no mapping for source code {value!r}"
            )
        return mapped


@dataclass(frozen=True)
class AttributeMapping:
    """Explicit source field -> canonical attribute mapping (S257)."""

    source_field: str
    canonical_attribute: str
    transform: Transform | None = None
    mapping_confidence: float = 1.0

    def __post_init__(self) -> None:
        if not self.source_field.strip():
            raise MappingRuntimeError("source_field must be non-empty")
        if not self.canonical_attribute.strip():
            raise MappingRuntimeError("canonical_attribute must be non-empty")
        if not 0.0 <= self.mapping_confidence <= 1.0:
            raise MappingRuntimeError("mapping_confidence must be in [0,1]")


@dataclass(frozen=True)
class EntityMapping:
    """Explicit source entity type -> canonical entity type (S256)."""

    source_entity_type: str
    canonical_entity_type: str
    canonical_id_field: str | None = None

    def __post_init__(self) -> None:
        if not self.source_entity_type.strip():
            raise MappingRuntimeError("source_entity_type must be non-empty")
        if not self.canonical_entity_type.strip():
            raise MappingRuntimeError("canonical_entity_type must be non-empty")


@dataclass(frozen=True)
class PredicateMapping:
    """Explicit enterprise relation -> canonical predicate (S258)."""

    source_relation_type: str
    canonical_predicate: str
    source_subject_field: str
    source_target_field: str
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not self.source_relation_type.strip():
            raise MappingRuntimeError("source_relation_type must be non-empty")
        if not self.canonical_predicate.strip():
            raise MappingRuntimeError("canonical_predicate must be non-empty")
        if not self.source_subject_field.strip():
            raise MappingRuntimeError("source_subject_field must be non-empty")
        if not self.source_target_field.strip():
            raise MappingRuntimeError("source_target_field must be non-empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise MappingRuntimeError("predicate confidence must be in [0,1]")


@dataclass(frozen=True)
class MappingRule:
    """A versioned, explicit mapping rule for one source system."""

    source_system: str
    rule_id: str
    mapping_version: str
    entity: EntityMapping | None = None
    attributes: tuple[AttributeMapping, ...] = ()
    predicates: tuple[PredicateMapping, ...] = ()
    rejected_fields: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.source_system.strip():
            raise MappingRuntimeError("source_system must be non-empty")
        if not self.rule_id.strip():
            raise MappingRuntimeError("rule_id must be non-empty")
        if not self.mapping_version.strip():
            raise MappingRuntimeError("mapping_version must be non-empty")
        if self.entity is not None and self.entity.source_entity_type != self.source_system:
            raise MappingRuntimeError("entity.source_entity_type must equal rule.source_system")
        fields = [attr.source_field for attr in self.attributes]
        if len(fields) != len(set(fields)):
            raise MappingRuntimeError("attribute source fields must be unique")
        rejected = set(self.rejected_fields)
        for attr in self.attributes:
            if attr.source_field in rejected:
                raise MappingRuntimeError(
                    f"field {attr.source_field!r} is both mapped and rejected"
                )
        if self.entity and self.entity.canonical_id_field in rejected:
            raise MappingRuntimeError("entity.canonical_id_field cannot be rejected")


@dataclass(frozen=True)
class CanonicalizationResult:
    """S262-compatible result. A result is a *decision*, not a Canonical Fact."""

    result_id: str
    source_system: str
    source_location: str
    scope: str
    decision_state: str
    mapping_confidence: float | None
    provenance: str
    reason: str
    mapping_rule_id: str
    adapter_version: str
    canonical_type: str | None = None
    canonical_target: str | None = None
    canonical_attributes: Mapping[str, Any] = field(default_factory=dict)
    canonical_edges: tuple[tuple[str, str, str], ...] = ()
    semantic_gap: str = SemanticGap.NONE
    transformation_metadata: Mapping[str, Any] = field(default_factory=dict)
    canonical_mutation: bool = False

    def __post_init__(self) -> None:
        valid_states = {
            MappingState.MAPPED,
            MappingState.AMBIGUOUS,
            MappingState.UNMAPPABLE,
            MappingState.REJECTED,
            MappingState.UNSUPPORTED,
            MappingState.INSUFFICIENT_EVIDENCE,
            MappingState.CONFLICTING_SEMANTICS,
        }
        if self.decision_state not in valid_states:
            raise MappingRuntimeError(f"invalid decision_state: {self.decision_state}")
        if self.decision_state == MappingState.MAPPED:
            if not (self.canonical_type and self.canonical_target is not None):
                raise MappingRuntimeError(
                    "mapped result requires canonical_type and canonical_target"
                )
        if self.canonical_mutation:
            raise MappingRuntimeError("P7-B mapping must not mutate Canonical Truth")


@dataclass(frozen=True)
class MappingRun:
    """Deterministic mapping run over one source evidence set."""

    rule: MappingRule | None
    results: tuple[CanonicalizationResult, ...]
    adapter_version: str

    @property
    def mapped_count(self) -> int:
        return sum(1 for r in self.results if r.decision_state == MappingState.MAPPED)

    @property
    def gap_count(self) -> int:
        return sum(1 for r in self.results if r.decision_state != MappingState.MAPPED)

    def to_json(self) -> str:
        return json.dumps(
            {
                "contract_version": "P7B.1",
                "rule_id": self.rule.rule_id if self.rule else None,
                "mapping_version": self.rule.mapping_version if self.rule else None,
                "adapter_version": self.adapter_version,
                "mapped_count": self.mapped_count,
                "gap_count": self.gap_count,
                "results": [self._result_to_map(r) for r in self.results],
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @staticmethod
    def _result_to_map(result: CanonicalizationResult) -> dict[str, Any]:
        return {
            "result_id": result.result_id,
            "source_system": result.source_system,
            "source_location": result.source_location,
            "scope": result.scope,
            "decision_state": result.decision_state,
            "mapping_confidence": result.mapping_confidence,
            "provenance": result.provenance,
            "reason": result.reason,
            "mapping_rule_id": result.mapping_rule_id,
            "canonical_type": result.canonical_type,
            "canonical_target": result.canonical_target,
            "canonical_attributes": sorted(result.canonical_attributes.items()),
            "canonical_edges": sorted(result.canonical_edges),
            "semantic_gap": result.semantic_gap,
            "transformation_metadata": sorted(result.transformation_metadata.items()),
            "canonical_mutation": result.canonical_mutation,
        }


class MappingCanonicalizer:
    """Deterministic, read-only source-to-canonical mapping runtime."""

    def __init__(self, rules: Sequence[MappingRule]) -> None:
        self._rules = {rule.source_system: rule for rule in rules}
        if len(self._rules) != len(rules):
            raise CanonicalizationError("duplicate mapping rule for a source system")

    def canonicalize(self, dataset: SourceDataset) -> MappingRun:
        rule = self._rules.get(dataset.manifest.source_system)
        results = tuple(
            self._govern(record, rule, dataset.manifest.adapter_version)
            for record in dataset.records
        )
        return MappingRun(
            rule=rule,
            results=results,
            adapter_version=dataset.manifest.adapter_version,
        )

    def run(self, dataset: SourceDataset) -> MappingRun:
        return self.canonicalize(dataset)

    # -- per-record governing -------------------------------------------------
    def _govern(self, record, rule, adapter_version):
        if rule is None:
            return _unmappable_result(
                record, adapter_version,
                reason="no mapping rule for this source system",
                gap=SemanticGap.NO_CANONICAL_TARGET,
            )

        # Build partial outcome explicitly. ``state`` is resolved only at the
        # end, so an intermediate MAPPED record never violates the invariant
        # that a mapped result carries a canonical target.
        out = _Outcome(
            result_id=f"{record.source_system}:{record.record_id}:result",
            source_system=record.source_system,
            source_location=record.source_location,
            scope=record.scope,
            adapter_version=adapter_version,
            mapping_rule_id=rule.rule_id,
            provenance=record.source_location,
        )

        # entity mapping (S256)
        entity = rule.entity
        if entity is not None:
            out.canonical_type = entity.canonical_entity_type
            id_field = entity.canonical_id_field or record.record_id
            if id_field in rule.rejected_fields:
                return out.gap(
                    record, MappingState.REJECTED, SemanticGap.VENDOR_SPECIFIC_SEMANTICS,
                    f"entity id field {id_field!r} is rejected",
                )
            if id_field not in record.payload:
                return out.gap(
                    record, MappingState.UNMAPPABLE, SemanticGap.AUTHORITY_INSUFFICIENT,
                    f"entity id field {id_field!r} missing",
                )
            out.canonical_target = str(record.payload[id_field])

        # attribute mapping (S257)
        for attr in rule.attributes:
            if attr.source_field not in record.payload:
                return out.gap(
                    record, MappingState.UNMAPPABLE, SemanticGap.NO_CANONICAL_TARGET,
                    f"missing source field {attr.source_field!r}",
                )
            raw = record.payload[attr.source_field]
            try:
                value = attr.transform.apply(raw) if attr.transform else raw
            except MappingRuntimeError as exc:
                return out.gap(
                    record, MappingState.UNMAPPABLE, SemanticGap.VENDOR_SPECIFIC_SEMANTICS,
                    str(exc),
                )
            out.canonical_attributes[attr.canonical_attribute] = value
            if attr.transform is not None:
                out.transformation_metadata[attr.canonical_attribute] = {
                    "transform": attr.transform.name,
                    "kind": attr.transform.kind,
                }

        # a rejected field present in the source payload is explicitly excluded
        for rejected in rule.rejected_fields:
            if rejected in record.payload:
                return out.gap(
                    record, MappingState.REJECTED, SemanticGap.VENDOR_SPECIFIC_SEMANTICS,
                    f"field {rejected!r} is explicitly rejected (vendor/control field)",
                )

        # predicate mapping (S258)
        for pred in rule.predicates:
            if (
                pred.source_subject_field not in record.payload
                or pred.source_target_field not in record.payload
            ):
                return out.gap(
                    record, MappingState.REJECTED, SemanticGap.VENDOR_SPECIFIC_SEMANTICS,
                    "predicate endpoint fields missing",
                )
            out.canonical_edges.append(
                (
                    pred.canonical_predicate,
                    str(record.payload[pred.source_subject_field]),
                    str(record.payload[pred.source_target_field]),
                )
            )

        return out.finish(record, MappingState.MAPPED, reason="mapped by explicit rule")


@dataclass(frozen=False)
class _Outcome:
    """Mutable builder for a CanonicalizationResult; never exposed directly."""

    result_id: str
    source_system: str
    source_location: str
    scope: str
    adapter_version: str
    mapping_rule_id: str
    provenance: str
    canonical_type: str | None = None
    canonical_target: str | None = None
    canonical_attributes: dict[str, Any] = field(default_factory=dict)
    canonical_edges: list[tuple[str, str, str]] = field(default_factory=list)
    transformation_metadata: dict[str, Any] = field(default_factory=dict)

    def finish(self, record, state, reason):
        return CanonicalizationResult(
            result_id=self.result_id,
            source_system=self.source_system,
            source_location=self.source_location,
            scope=self.scope,
            decision_state=state,
            mapping_confidence=1.0 if state == MappingState.MAPPED else None,
            provenance=self.provenance,
            reason=reason,
            mapping_rule_id=self.mapping_rule_id,
            adapter_version=self.adapter_version,
            canonical_type=self.canonical_type,
            canonical_target=self.canonical_target if state == MappingState.MAPPED else None,
            canonical_attributes=dict(self.canonical_attributes) if state == MappingState.MAPPED else {},
            canonical_edges=tuple(self.canonical_edges) if state == MappingState.MAPPED else (),
            semantic_gap=SemanticGap.NONE if state == MappingState.MAPPED else SemanticGap.NO_CANONICAL_TARGET,
            transformation_metadata=dict(self.transformation_metadata) if state == MappingState.MAPPED else {},
        )

    def gap(self, record, state, gap, reason):
        """Return a gapped result carrying the partial canonical identity."""
        return CanonicalizationResult(
            result_id=self.result_id,
            source_system=self.source_system,
            source_location=self.source_location,
            scope=self.scope,
            decision_state=state,
            mapping_confidence=None,
            provenance=self.provenance,
            reason=reason,
            mapping_rule_id=self.mapping_rule_id,
            adapter_version=self.adapter_version,
            canonical_type=self.canonical_type,
            canonical_target=self.canonical_target if state == MappingState.AMBIGUOUS and self.canonical_target else None,
            canonical_attributes={},
            canonical_edges=(),
            semantic_gap=gap,
            transformation_metadata={},
        )


def _unmappable_result(record: SourceEvidence, adapter_version: str, reason: str, gap: str) -> CanonicalizationResult:
    return CanonicalizationResult(
        result_id=f"{record.source_system}:{record.record_id}:result",
        source_system=record.source_system,
        source_location=record.source_location,
        scope=record.scope,
        decision_state=MappingState.UNMAPPABLE,
        mapping_confidence=None,
        provenance=record.source_location,
        reason=reason,
        mapping_rule_id="",
        adapter_version=adapter_version,
        semantic_gap=gap,
    )


# ---------------------------------------------------------------------------
# Deterministic reference path
# ---------------------------------------------------------------------------
def reference_mapping_rule(source_system: str) -> MappingRule:
    """The explicit mapping rule used by the P7-B reference path."""
    if source_system == "erp":
        return MappingRule(
            source_system="erp",
            rule_id="erp-material-master-v1",
            mapping_version="P7B.1",
            entity=EntityMapping("erp", "Material", canonical_id_field="material_id"),
            attributes=(
                AttributeMapping("material_id", "materialId"),
                AttributeMapping("description", "description"),
            ),
        )
    if source_system == "wms":
        return MappingRule(
            source_system="wms",
            rule_id="wms-stock-ledger-v1",
            mapping_version="P7B.1",
            entity=EntityMapping("wms", "InventoryPosition", canonical_id_field="stock_id"),
            attributes=(
                AttributeMapping("stock_id", "stockId"),
                AttributeMapping("location", "locationId"),
                AttributeMapping("qty", "quantity"),
            ),
        )
    if source_system == "tms":
        return MappingRule(
            source_system="tms",
            rule_id="tms-shipment-v1",
            mapping_version="P7B.1",
            entity=EntityMapping("tms", "Shipment", canonical_id_field="shipment_id"),
            attributes=(
                AttributeMapping("shipment_id", "shipmentId"),
                AttributeMapping("carrier", "carrierId"),
                AttributeMapping("lanes", "laneCount"),
            ),
            predicates=(
                PredicateMapping(
                    "carried_by",
                    "carriedBy",
                    source_subject_field="shipment_id",
                    source_target_field="carrier",
                ),
            ),
        )
    return _reference_rule_not_defined(source_system)


def _reference_rule_not_defined(source_system: str) -> None:
    raise MappingRuntimeError(f"no reference rule for source_system {source_system!r}")


def run_reference_mapping_path() -> MappingRun:
    """Deterministic reference path: P7-A evidence -> canonicalization."""
    from .reference_data_adapter import run_reference_data_adapter_path

    bundle = run_reference_data_adapter_path()
    canonicalizer = MappingCanonicalizer(
        [reference_mapping_rule(source) for source in ("erp", "wms", "tms")]
    )
    results: list[CanonicalizationResult] = []
    for dataset in bundle.datasets:
        for result in canonicalizer.canonicalize(dataset).results:
            results.append(result)
    return MappingRun(rule=None, results=tuple(results), adapter_version="P7B.1")
