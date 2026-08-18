import pytest

from scm_ontology.data_quality_gate import (
    CheckOutcome,
    CheckType,
    DataQualityGate,
    DataQualityGateError,
    DataQualityPolicy,
    DataQualityReport,
    UnitConstraint,
    run_reference_data_quality_path,
)
from scm_ontology.reference_data_adapter import (
    CsvAdapterConfig,
    SourceDataset,
    SourceEvidence,
    SourceManifest,
    adapt_csv,
)


def _manifest(extracted_at="2026-08-19T09:00:00Z", scope="enterprise:acme", adapter_kind="csv", source="erp"):
    return SourceManifest(
        source_system=source,
        adapter_version="P7A.1",
        data_contract_version="P7A.1",
        mapping_config_version="M8-reference",
        extracted_at=extracted_at,
        scope=scope,
        adapter_kind=adapter_kind,
    )


def _policy(**overrides):
    args = dict(
        policy_id="p", policy_version="P7D.1",
        required_fields=("material_id", "description"),
        allowed_scopes=("enterprise:acme",),
        max_age_seconds=3600.0,
        unit_constraints=(UnitConstraint("quantity", ("EA", "KG")),),
    )
    args.update(overrides)
    return DataQualityPolicy(**args)


def _csv_dataset(rows, manifest=None):
    manifest = manifest or _manifest()
    return adapt_csv(
        rows,
        manifest,
        CsvAdapterConfig(source_system=manifest.source_system, record_id_column="material_id"),
    )


def test_reference_path_passes_and_is_deterministic():
    first = run_reference_data_quality_path()
    second = run_reference_data_quality_path()
    assert first.all_passed
    assert not first.blocked
    assert first.evaluated_count == 2
    assert first.to_json() == second.to_json()


def test_completeness_failure_blocks_batch():
    gate = DataQualityGate(_policy(), now="2026-08-19T09:30:00Z")
    report = gate.evaluate(_csv_dataset([{"material_id": "MAT-1"}]))  # missing description
    record = report.records[0]
    assert CheckType.COMPLETENESS in record.failed_checks
    assert report.blocked
    assert not report.all_passed


def test_freshness_failure_on_stale_record():
    gate = DataQualityGate(_policy(), now="2026-08-19T12:00:00Z")
    stale_manifest = _manifest(extracted_at="2026-08-19T08:00:00Z")
    report = gate.evaluate(
        _csv_dataset(
            [{"material_id": "MAT-1", "description": "d"}],
            stale_manifest,
        )
    )
    assert CheckType.FRESHNESS in report.records[0].failed_checks


def test_freshness_passes_within_limit():
    gate = DataQualityGate(_policy(), now="2026-08-19T09:10:00Z")
    report = gate.evaluate(_csv_dataset([{"material_id": "MAT-1", "description": "d"}]))
    assert report.all_passed


def test_scope_failure():
    gate = DataQualityGate(_policy(), now="2026-08-19T09:30:00Z")
    bad_scope = _manifest(scope="enterprise:other")
    report = gate.evaluate(_csv_dataset([{"material_id": "MAT-1", "description": "d"}], bad_scope))
    assert CheckType.SCOPE in report.records[0].failed_checks


def test_unit_failure():
    policy = _policy(unit_constraints=(UnitConstraint("quantity", ("kg",)),))
    gate = DataQualityGate(policy, now="2026-08-19T09:30:00Z")
    report = gate.evaluate(
        _csv_dataset([{"material_id": "MAT-1", "description": "d", "quantity": "lb"}])
    )
    assert CheckType.UNIT in report.records[0].failed_checks


def test_unit_pass_with_non_matching_field_ignored():
    gate = DataQualityGate(_policy(), now="2026-08-19T09:30:00Z")
    report = gate.evaluate(
        _csv_dataset([{"material_id": "MAT-1", "description": "d", "status": "monsoon"}])
    )
    assert report.all_passed


def test_provenance_failure_on_missing_field_evidence():
    record = SourceEvidence(
        evidence_id="erp:M1", source_system="erp", source_location="erp:row=1",
        record_id="M1", payload={"material_id": "M1", "description": "d"},
        observed_at="2026-08-19T09:00:00Z", scope="enterprise:acme",
        mapping_config_version="M8-reference",
    )
    dataset = SourceDataset(manifest=_manifest(), records=(record,))
    gate = DataQualityGate(_policy(), now="2026-08-19T09:30:00Z")
    report = gate.evaluate(dataset)
    assert CheckType.PROVENANCE in report.records[0].failed_checks
    assert report.blocked


def test_policy_fails_closed():
    with pytest.raises(DataQualityGateError, match="policy_id"):
        DataQualityPolicy(policy_id=" ", policy_version="v")
    with pytest.raises(DataQualityGateError, match="unique"):
        DataQualityPolicy(
            policy_id="p", policy_version="v",
            unit_constraints=(UnitConstraint("a", ("x",)), UnitConstraint("a", ("y",))),
        )


def test_invalid_check_outcome_rejected():
    from scm_ontology.data_quality_gate import QualityCheckResult

    with pytest.raises(DataQualityGateError, match="invalid outcome"):
        QualityCheckResult(CheckType.SCOPE, "nope")
    with pytest.raises(DataQualityGateError, match="invalid check"):
        QualityCheckResult("bogus", CheckOutcome.PASS)
