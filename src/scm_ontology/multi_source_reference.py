"""P7-E Multi-source Reference Dataset (Phase 7, SCM OS Real Data Plane).

Composes the P7-A Reference Data Adapter, P7-B Mapping / Canonicalization
Runtime, P7-C Identity Resolution Runtime, and P7-D Data Quality / Freshness
Gate into one *reproducible, traceable* pipeline in which several heterogeneous
source representations converge onto a single reference Canonical Graph.

```text
ERP @csv ─┐
WMS @json ┼─ P7-A adapters -> SourceEvidence
TMS @sql ─┘        │
                   ├─ P7-D quality gate (fail closed)
                   ├─ P7-B canonicalization -> CanonicalizationResult
                   ├─ P7-C identity resolution -> matched identities
                   ▼
          ConvergedReferenceGraph (reproducible + traceable)
```

Guardrails honored:
  - the converged graph is a *reference* projection, NEVER Canonical Truth
    (``canonical_truth_boundary = "reference"``);
  - every node / edge / identity link is reproducible and traceable to evidence;
  - the quality gate is fail-closed; identity resolution never mutates anything;
  - provenance, scope, and temporal context are preserved throughout;
  - the pipeline never creates canonical entities, attributes, or predicates
    automatically.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping, Sequence

from .data_quality_gate import DataQualityGate, DataQualityPolicy
from .identity_resolution_runtime import (
    IdentityRecord,
    IdentityResolver,
    IdentityResolutionPolicy,
    IdentityResolutionRun,
    IdentitySignal,
    ResolutionOutcome,
)
from .mapping_canonicalization_runtime import (
    AttributeMapping,
    CanonicalizationResult,
    EntityMapping,
    MappingCanonicalizer,
    MappingRule,
    MappingState,
    PredicateMapping,
)
from .reference_data_adapter import (
    CsvAdapterConfig,
    SqlSourceConfig,
    SourceDataset,
    SourceManifest,
    adapt_csv,
    adapt_json,
    adapt_sql,
)


class MultiSourceError(ValueError):
    """Raised when a multi-source reference pipeline is invalid."""


@dataclass(frozen=True)
class ConvergedNode:
    """One canonical entity node in the converged reference graph."""

    key: str
    canonical_type: str
    attributes: Mapping[str, Any]
    sources: tuple[tuple[str, str, str], ...]  # (source_system, record_id, provenance)

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise MultiSourceError("node key must be non-empty")
        if not self.canonical_type.strip():
            raise MultiSourceError("node canonical_type must be non-empty")
        if not self.sources:
            raise MultiSourceError("node must carry at least one source member")


@dataclass(frozen=True)
class ConvergedEdge:
    """A canonical predicate edge with explicit endpoint provenance."""

    predicate: str
    subject_key: str
    object_key: str | None
    provenance: str

    def __post_init__(self) -> None:
        if not self.predicate.strip():
            raise MultiSourceError("edge predicate must be non-empty")
        if not self.subject_key.strip():
            raise MultiSourceError("edge subject_key must be non-empty")
        if not self.provenance.strip():
            raise MultiSourceError("edge provenance must be non-empty")


@dataclass(frozen=True)
class ConvergedReferenceGraph:
    """Immutable, reproducible, traceable converged view (never Canonical Truth)."""

    run_id: str
    content_hash: str
    nodes: tuple[ConvergedNode, ...] = field(default_factory=tuple)
    edges: tuple[ConvergedEdge, ...] = field(default_factory=tuple)
    identity_links: tuple[tuple[str, ...], ...] = field(default_factory=tuple)
    canonical_truth_boundary: str = "reference"

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    def node(self, key: str) -> "ConvergedNode":
        for node in self.nodes:
            if node.key == key:
                return node
        raise KeyError(key)

    def to_json(self) -> str:
        return json.dumps(
            {
                "contract_version": "P7E.1",
                "run_id": self.run_id,
                "content_hash": self.content_hash,
                "canonical_truth_boundary": self.canonical_truth_boundary,
                "node_count": self.node_count,
                "edge_count": self.edge_count,
                "nodes": [
                    {
                        "key": node.key,
                        "canonical_type": node.canonical_type,
                        "attributes": _freeze(node.attributes),
                        "sources": [list(source) for source in node.sources],
                    }
                    for node in self.nodes
                ],
                "edges": [
                    {
                        "predicate": edge.predicate,
                        "subject_key": edge.subject_key,
                        "object_key": edge.object_key,
                        "provenance": edge.provenance,
                    }
                    for edge in self.edges
                ],
                "identity_links": [list(link) for link in self.identity_links],
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _freeze(item) for key, item in sorted(value.items())}
    if isinstance(value, (list, tuple, set)):
        return [_freeze(item) for item in sorted(value, key=str)]
    return value


def _content_hash(graph_json: str) -> str:
    return sha256(graph_json.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# End-to-end orchestration
# ---------------------------------------------------------------------------
def converge(
    datasets: Sequence[SourceDataset],
    *,
    quality_policies: Mapping[str, DataQualityPolicy],
    mapping_rules: Sequence[MappingRule],
    identity_policy: IdentityResolutionPolicy,
    decision_at: str,
    now: str,
    identity_types: Sequence[str] = ("Product",),
    run_id: str = "p7e-reference",
) -> ConvergedReferenceGraph:
    """Run the fail-closed P7-A -> P7-D -> P7-B -> P7-C pipeline and converge.

    Each source system is quality-gated against its own policy (different
    sources legitimately require different fields).
    """
    if not datasets:
        raise MultiSourceError("at least one source dataset is required")

    # P7-D: quality gate only lets compliant evidence proceed (fail closed).
    for dataset in datasets:
        policy = quality_policies.get(dataset.manifest.source_system)
        if policy is None:
            raise MultiSourceError(
                f"no quality policy for source system {dataset.manifest.source_system!r}"
            )
        gate = DataQualityGate(policy, now=now)
        if gate.evaluate(dataset).blocked:
            raise MultiSourceError(
                f"quality gate blocked {dataset.manifest.source_system!r} before convergence"
            )

    # P7-B: deterministic source-to-canonical mapping.
    canonicalizer = MappingCanonicalizer(list(mapping_rules))
    canonical_results: list[CanonicalizationResult] = []
    for dataset in datasets:
        canonical_results.extend(canonicalizer.canonicalize(dataset).results)

    # P7-C: identity resolution over the mapped records of the resolved types.
    identity_records = [
        IdentityRecord.from_canonicalization(result)
        for result in canonical_results
        if result.decision_state == MappingState.MAPPED
        and (not identity_types or result.canonical_type in identity_types)
    ]
    resolution = IdentityResolver(identity_policy).identify(
        identity_records, decision_at=decision_at
    )

    return _build_graph(canonical_results, resolution, run_id=run_id)


def _build_graph(
    results: Sequence[CanonicalizationResult],
    resolution_run: IdentityResolutionRun,
    *,
    run_id: str,
) -> ConvergedReferenceGraph:
    # Collect mapped results keyed by their canonical reference.
    mapped = [result for result in results if result.decision_state == MappingState.MAPPED]

    # Node identity: canonical_type + canonical_target.
    node_buckets: dict[tuple[str, str], list[CanonicalizationResult]] = {}
    for result in mapped:
        node_buckets.setdefault(
            (result.canonical_type, result.canonical_target), []
        ).append(result)

    nodes: list[ConvergedNode] = []
    edges: list[ConvergedEdge] = []
    # index of canonical target -> node key, to resolve edge endpoints to nodes
    ref_index: dict[str, str] = {}
    for (canonical_type, canonical_ref), members in sorted(node_buckets.items()):
        node_key = f"{canonical_type}:{canonical_ref}"
        ref_index[canonical_ref] = node_key
        sources = tuple(
            sorted(
                {
                    (member.source_system, member.result_id, member.source_location)
                    for member in members
                }
            )
        )
        attributes = members[0].canonical_attributes
        nodes.append(
            ConvergedNode(
                key=node_key,
                canonical_type=canonical_type,
                attributes=attributes,
                sources=sources,
            )
        )
        for member in members:
            for predicate, subject, target in member.canonical_edges:
                # Resolve the subject to its own node; resolve the target to a
                # converged node when it is an identity reference (e.g. gtin).
                subject_key = f"{canonical_type}:{subject}"
                object_key = None
                if target:
                    object_key = ref_index.get(target) or f"{canonical_type}:{target}"
                edges.append(
                    ConvergedEdge(
                        predicate=predicate,
                        subject_key=subject_key,
                        object_key=object_key,
                        provenance=member.source_location,
                    )
                )

    # Identity links from resolved matches (traceable correspondence).
    identity_links = sorted(
        {
            tuple(sorted(member.is_resolved_label for member in candidate.members))
            for candidate in resolution_run.candidates
            if candidate.outcome == ResolutionOutcome.MATCHED
        }
    )

    nodes = sorted(nodes, key=lambda node: node.key)
    edges = sorted(edges, key=lambda edge: (edge.predicate, edge.subject_key, edge.object_key or ""))
    graph = ConvergedReferenceGraph(
        run_id=run_id,
        content_hash="",
        nodes=tuple(nodes),
        edges=tuple(edges),
        identity_links=tuple(identity_links),
    )
    # Content hash is derived from the canonical JSON (reproducible).
    graph_json = json.dumps(
        {
            "nodes": [_node_to_json(n) for n in graph.nodes],
            "edges": [_edge_to_json(e) for e in graph.edges],
            "identity_links": [list(link) for link in graph.identity_links],
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return ConvergedReferenceGraph(
        run_id=run_id,
        content_hash=_content_hash(graph_json),
        nodes=graph.nodes,
        edges=graph.edges,
        identity_links=graph.identity_links,
        canonical_truth_boundary="reference",
    )


def _node_to_json(node: ConvergedNode) -> dict[str, Any]:
    return {
        "key": node.key,
        "canonical_type": node.canonical_type,
        "sources": [list(source) for source in node.sources],
    }


def _edge_to_json(edge: ConvergedEdge) -> dict[str, Any]:
    return {
        "predicate": edge.predicate,
        "subject_key": edge.subject_key,
        "object_key": edge.object_key,
        "provenance": edge.provenance,
    }


# ---------------------------------------------------------------------------
# Deterministic reference path
# ---------------------------------------------------------------------------
def reference_datasets() -> tuple[SourceDataset, ...]:
    """Heterogeneous source datasets built with the P7-A adapters.

    - ERP material master (CSV) and WMS stock positions (JSON) reference the
      same canonical products via a shared, explicit GTIN identity signal.
    - A TMS shipment (SQL) carries a canonical predicate edge (carriedBy).
    """
    erp_manifest = SourceManifest(
        source_system="erp", adapter_version="P7A.1", data_contract_version="P7A.1",
        mapping_config_version="M8-reference", extracted_at="2026-08-19T09:00:00Z",
        scope="enterprise:acme", adapter_kind="csv",
    )
    wms_manifest = SourceManifest(
        source_system="wms", adapter_version="P7A.1", data_contract_version="P7A.1",
        mapping_config_version="M8-reference", extracted_at="2026-08-19T09:00:01Z",
        scope="enterprise:acme", adapter_kind="json",
    )
    tms_manifest = SourceManifest(
        source_system="tms", adapter_version="P7A.1", data_contract_version="P7A.1",
        mapping_config_version="M8-reference", extracted_at="2026-08-19T09:00:02Z",
        scope="enterprise:acme", adapter_kind="sql",
    )
    erp = adapt_csv(
        [
            {"material_id": "MAT-1000", "gtin": "0850000000101", "description": "Raw aluminium"},
            {"material_id": "MAT-1001", "gtin": "0850000000102", "description": "Fastener"},
        ],
        erp_manifest,
        CsvAdapterConfig(source_system="erp", record_id_column="material_id"),
    )
    # A second product registry (WMS) references the SAME canonical Products via
    # the shared GTIN, so identity resolution in P7-C converges them.
    wms = adapt_json(
        {
            "records": [
                {"product_id": "PROD-1000", "gtin": "0850000000101", "category": "raw"},
                {"product_id": "PROD-1001", "gtin": "0850000000102", "category": "assy"},
            ]
        },
        wms_manifest,
        record_id_key="product_id",
    )
    # A TMS shipment references a material via a carriedBy predicate edge.
    tms = adapt_sql(
        [
            {"shipment_id": "SHIP-1", "gtin": "0850000000101", "carrier": "carrier-a"},
            {"shipment_id": "SHIP-2", "gtin": "0850000000102", "carrier": "carrier-b"},
        ],
        tms_manifest,
        SqlSourceConfig(table="shipment", scope="enterprise:acme", primary_key="shipment_id"),
    )
    return (erp, wms, tms)


def reference_quality_policies() -> dict[str, DataQualityPolicy]:
    return {
        "erp": DataQualityPolicy(
            policy_id="p7e-erp-quality", policy_version="P7E.1",
            required_fields=("material_id", "description"),
            allowed_scopes=("enterprise:acme",), max_age_seconds=86400.0,
        ),
        "wms": DataQualityPolicy(
            policy_id="p7e-wms-quality", policy_version="P7E.1",
            required_fields=("product_id", "category"),
            allowed_scopes=("enterprise:acme",), max_age_seconds=86400.0,
        ),
        "tms": DataQualityPolicy(
            policy_id="p7e-tms-quality", policy_version="P7E.1",
            required_fields=("shipment_id", "carrier"),
            allowed_scopes=("enterprise:acme",), max_age_seconds=86400.0,
        ),
    }


def reference_mapping_rules() -> tuple[MappingRule, ...]:
    return (
        MappingRule(
            source_system="erp", rule_id="p7e-erp-product", mapping_version="P7E.1",
            entity=EntityMapping("erp", "Product", canonical_id_field="gtin"),
            attributes=(
                AttributeMapping("material_id", "materialId"),
                AttributeMapping("gtin", "gtin"),
                AttributeMapping("description", "description"),
            ),
        ),
        MappingRule(
            source_system="wms", rule_id="p7e-wms-registry", mapping_version="P7E.1",
            entity=EntityMapping("wms", "Product", canonical_id_field="gtin"),
            attributes=(
                AttributeMapping("product_id", "productId"),
                AttributeMapping("gtin", "gtin"),
                AttributeMapping("category", "category"),
            ),
        ),
        MappingRule(
            source_system="tms", rule_id="p7e-tms-shipment", mapping_version="P7E.1",
            entity=EntityMapping("tms", "Shipment", canonical_id_field="shipment_id"),
            attributes=(
                AttributeMapping("shipment_id", "shipmentId"),
                AttributeMapping("gtin", "gtin"),
            ),
            predicates=(
                PredicateMapping(
                    "carried_by", "carriedBy",
                    source_subject_field="shipment_id", source_target_field="gtin",
                ),
            ),
        ),
    )


REFERENCE_IDENTITY_POLICY = IdentityResolutionPolicy(
    policy_id="p7e-reference-identity",
    policy_version="P7E.1",
    signals=(IdentitySignal("gtin"),),
)


def run_multi_source_reference_path() -> ConvergedReferenceGraph:
    """Deterministic reference path: heterogeneous inputs -> converged graph."""
    datasets = reference_datasets()
    policies = reference_quality_policies()
    for dataset in datasets:
        gate = DataQualityGate(policies[dataset.manifest.source_system], now="2026-08-19T09:30:00Z")
        if gate.evaluate(dataset).blocked:
            raise MultiSourceError(
                f"quality gate blocked {dataset.manifest.source_system!r}"
            )

    canonicalizer = MappingCanonicalizer(list(reference_mapping_rules()))
    results = [
        result
        for dataset in datasets
        for result in canonicalizer.canonicalize(dataset).results
    ]
    records = [
        IdentityRecord.from_canonicalization(result)
        for result in results
        if result.decision_state == MappingState.MAPPED
        and result.canonical_type == "Product"
    ]
    resolution = IdentityResolver(REFERENCE_IDENTITY_POLICY).identify(
        records, decision_at="2026-08-19T09:30:00Z"
    )
    return _build_graph(results, resolution, run_id="p7e-reference")
