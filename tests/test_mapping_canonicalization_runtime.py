from dataclasses import FrozenInstanceError

from dataclasses import replace

import pytest

from scm_ontology.mapping_canonicalization_runtime import (
    AttributeMapping,
    CanonicalizationResult,
    EntityMapping,
    MappingCanonicalizer,
    MappingRule,
    MappingRun,
    MappingRuntimeError,
    MappingState,
    PredicateMapping,
    SemanticGap,
    Transform,
    reference_mapping_rule,
    run_reference_mapping_path,
)
from scm_ontology.reference_data_adapter import (
    CsvAdapterConfig,
    SourceDataset,
    SourceEvidence,
    SourceManifest,
    adapt_csv,
    adapt_json,
    adapt_sql,
)


def _manifest(source="erp", adapter_kind="csv", **overrides):
    args = dict(
        source_system=source,
        adapter_version="P7A.1",
        data_contract_version="P7A.1",
        mapping_config_version="M8-reference",
        extracted_at="2026-08-19T09:00:00Z",
        scope="enterprise:acme",
        adapter_kind=adapter_kind,
    )
    args.update(overrides)
    return SourceManifest(**args)


def _erp_rule():
    return MappingRule(
        source_system="erp",
        rule_id="erp-material-v1",
        mapping_version="P7B.1",
        entity=EntityMapping("erp", "Material", canonical_id_field="material_id"),
        attributes=(
            AttributeMapping("material_id", "materialId"),
            AttributeMapping("description", "description"),
        ),
    )


def _run(rule, manifest=None, rows=None):
    canonicalizer = MappingCanonicalizer([rule])
    dataset = adapt_csv(
        rows or [{"material_id": "MAT-1", "description": "Red widget", "plant": "PLT-1"}],
        manifest or _manifest(source=rule.source_system),
        CsvAdapterConfig(source_system=rule.source_system, record_id_column="material_id"),
    )
    return canonicalizer.canonicalize(dataset)


def _single(run):
    return run.results[0]


def test_reference_path_maps_all_sources_deterministically():
    first = run_reference_mapping_path()
    second = run_reference_mapping_path()
    assert first.mapped_count == 6
    assert first.gap_count == 0
    assert first.to_json() == second.to_json()


def test_reference_path_produces_entity_and_predicate_signatures():
    run = run_reference_mapping_path()
    by_type = {r.canonical_type for r in run.results}
    assert by_type == {"Material", "InventoryPosition", "Shipment"}
    edges = [e for r in run.results if r.canonical_edges for e in r.canonical_edges]
    assert ("carriedBy", "SHIP-1", "carrier-a") in edges


def test_mapped_result_carries_canonical_attributes_without_mutating_truth():
    run = _run(_erp_rule())
    result = run.results[0]
    assert result.decision_state == MappingState.MAPPED
    assert result.canonical_type == "Material"
    assert result.canonical_target == "MAT-1"
    assert result.canonical_attributes["description"] == "Red widget"
    assert result.canonical_mutation is False
    # mapping_confidence is mapping metadata, provenance is lineage
    assert result.mapping_confidence == 1.0
    assert "row=1" in result.provenance
    assert run.rule.rule_id == "erp-material-v1"


def test_no_rule_fails_closed_as_unmappable():
    canonicalizer = MappingCanonicalizer([])
    dataset = adapt_csv(
        [{"material_id": "MAT-1"}],
        _manifest(source="unk"),
        CsvAdapterConfig(source_system="unk", record_id_column="material_id"),
    )
    result = canonicalizer.canonicalize(dataset).results[0]
    assert result.decision_state == MappingState.UNMAPPABLE
    assert result.semantic_gap == SemanticGap.NO_CANONICAL_TARGET
    assert result.canonical_target is None
    assert result.canonical_mutation is False


def test_missing_source_field_is_a_gap_not_truth():
    run = _run(_erp_rule(), rows=[{"material_id": "MAT-1"}])
    result = run.results[0]
    assert result.decision_state == MappingState.UNMAPPABLE
    assert result.semantic_gap == SemanticGap.NO_CANONICAL_TARGET
    assert "description" in result.reason
    assert result.canonical_attributes == {}


def test_missing_entity_id_field_is_authority_insufficient():
    rule = MappingRule(
        source_system="erp",
        rule_id="r",
        mapping_version="v",
        entity=EntityMapping("erp", "Material", canonical_id_field="uid"),
        attributes=(),
    )
    result = _run(rule, rows=[{"material_id": "MAT-1"}]).results[0]
    assert result.decision_state == MappingState.UNMAPPABLE
    assert result.semantic_gap == SemanticGap.AUTHORITY_INSUFFICIENT


def test_explicit_value_transform_normalizes_without_inventing_meaning():
    rule = MappingRule(
        source_system="erp",
        rule_id="r",
        mapping_version="P",
        entity=EntityMapping("erp", "Material", canonical_id_field="material_id"),
        attributes=(
            AttributeMapping(
                "status",
                "status",
                transform=Transform("mat-status", "code", {"active": "ACTIVE", "hold": "HOLD"}),
            ),
        ),
    )
    result = _run(rule, rows=[{"material_id": "M1", "status": "active"}]).results[0]
    assert result.decision_state == MappingState.MAPPED
    assert result.canonical_attributes["status"] == "ACTIVE"
    assert result.transformation_metadata["status"]["kind"] == "code"


def test_unknown_source_code_is_a_gap_not_silently_promoted():
    rule = MappingRule(
        source_system="erp",
        rule_id="r",
        mapping_version="P",
        entity=EntityMapping("erp", "Material", canonical_id_field="material_id"),
        attributes=(
            AttributeMapping(
                "status",
                "status",
                transform=Transform("mat-status", "code", {"active": "ACTIVE"}),
            ),
        ),
    )
    result = _run(rule, rows=[{"material_id": "M1", "status": "draft"}]).results[0]
    assert result.decision_state == MappingState.UNMAPPABLE
    assert result.semantic_gap == SemanticGap.VENDOR_SPECIFIC_SEMANTICS
    assert "no mapping" in result.reason


def test_rejected_vendor_field_blocks_mapping():
    rule = replace(_erp_rule(), rejected_fields=("plant",))
    result = _run(rule, rows=[{"material_id": "M1", "description": "d", "plant": "PLT-1"}]).results[0]
    assert result.decision_state == MappingState.REJECTED
    assert result.semantic_gap == SemanticGap.VENDOR_SPECIFIC_SEMANTICS


def test_predicate_mapping_requires_endpoints():
    rule = MappingRule(
        source_system="tms",
        rule_id="R",
        mapping_version="P",
        entity=EntityMapping("tms", "Shipment", canonical_id_field="shipment_id"),
        attributes=(),
        predicates=(
            PredicateMapping("carried_by", "carriedBy", "shipment_id", "carrier"),
        ),
    )
    canonicalizer = MappingCanonicalizer([rule])
    dataset = adapt_csv(
        [{"shipment_id": "S1"}],
        _manifest(source="tms"),
        CsvAdapterConfig(source_system="tms", record_id_column="shipment_id"),
    )
    result = canonicalizer.canonicalize(dataset).results[0]
    assert result.decision_state == MappingState.REJECTED
    assert result.semantic_gap == SemanticGap.VENDOR_SPECIFIC_SEMANTICS


def test_results_are_immutable():
    result = _run(_erp_rule()).results[0]
    with pytest.raises(FrozenInstanceError):
        result.canonical_target = "changed"
    run = _run(_erp_rule())
    with pytest.raises(FrozenInstanceError):
        run.rule = None


def test_result_vocabulary_includes_mapping_states():
    # A mapped result requires a canonical identity, reinforcing result != fact
    with pytest.raises(MappingRuntimeError):
        CanonicalizationResult(
            result_id="r", source_system="erp", source_location="loc", scope="s",
            decision_state=MappingState.MAPPED, mapping_confidence=1.0,
            provenance="p", reason="r", mapping_rule_id="R", adapter_version="A",
        )
    # non-mapped states never require a canonical target
    gap = CanonicalizationResult(
        result_id="r", source_system="erp", source_location="loc", scope="s",
        decision_state=MappingState.AMBIGUOUS, mapping_confidence=None,
        provenance="p", reason="r", mapping_rule_id="R", adapter_version="A",
        canonical_mutation=False,
    )
    assert gap.canonical_target is None


def test_canonical_mutation_is_always_forbidden_in_this_slice():
    with pytest.raises(MappingRuntimeError, match="must not mutate"):
        CanonicalizationResult(
            result_id="r", source_system="erp", source_location="loc", scope="s",
            decision_state=MappingState.REJECTED, mapping_confidence=None,
            provenance="p", reason="r", mapping_rule_id="R", adapter_version="A",
            canonical_mutation=True,
        )


def test_rule_fails_closed():
    with pytest.raises(MappingRuntimeError, match="source_system"):
        MappingRule(source_system=" ", rule_id="R", mapping_version="P")
    with pytest.raises(MappingRuntimeError, match="unique"):
        MappingRule(
            source_system="erp", rule_id="R", mapping_version="P",
            attributes=(AttributeMapping("a", "x"), AttributeMapping("a", "y")),
        )
    with pytest.raises(MappingRuntimeError, match="rejected"):
        MappingRule(
            source_system="erp", rule_id="R", mapping_version="P",
            entity=EntityMapping("erp", "Material", canonical_id_field="id"),
            rejected_fields=("id",),
        )
    with pytest.raises(MappingRuntimeError, match="both mapped and rejected"):
        MappingRule(
            source_system="erp", rule_id="R", mapping_version="P",
            attributes=(AttributeMapping("a", "x"),),
            rejected_fields=("a",),
        )
    with pytest.raises(MappingRuntimeError, match="entity.source_entity_type"):
        MappingRule(
            source_system="erp", rule_id="R", mapping_version="P",
            entity=EntityMapping("wms", "Inventory"),
        )


def test_duplicate_rule_for_source_system_rejected():
    rule = _erp_rule()
    with pytest.raises(Exception):
        MappingCanonicalizer([rule, rule])
