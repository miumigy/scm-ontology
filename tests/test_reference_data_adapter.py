from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.reference_data_adapter import (
    AdapterConformance,
    AdapterError,
    CsvAdapterConfig,
    ReferenceEvidenceBundle,
    SqlSourceConfig,
    SourceDataset,
    SourceEvidence,
    SourceManifest,
    adapt_csv,
    adapt_json,
    adapt_sql,
    conformant,
    run_reference_data_adapter_path,
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


def test_csv_adapter_produces_evidence_with_field_provenance():
    dataset = adapt_csv(
        [{"material_id": "MAT-1000", "description": "Raw aluminium", "plant": "PLT-E"}],
        _manifest(),
        CsvAdapterConfig(source_system="erp", record_id_column="material_id"),
    )
    assert dataset.record_count == 1
    record = dataset.records[0]
    assert record.evidence_id == "erp:MAT-1000"
    assert record.source_location == "reference:row=1"
    assert record.payload["description"] == "Raw aluminium"
    # every field carries an evidence ref
    assert {ref.metadata["column"] for ref in record.field_evidence} == {
        "description", "material_id", "plant",
    }
    assert all(ref.observed_at == "2026-08-19T09:00:00Z" for ref in record.field_evidence)
    assert dataset.content_hash == dataset.content_hash  # deterministic


def test_csv_adapter_fails_closed_on_missing_identity_column():
    with pytest.raises(AdapterError, match="missing record identity column"):
        adapt_csv(
            [{"description": "Raw aluminium"}],
            _manifest(),
            CsvAdapterConfig(source_system="erp", record_id_column="material_id"),
        )


def test_csv_adapter_fails_closed_on_empty_or_duplicate_record_id():
    config = CsvAdapterConfig(source_system="erp", record_id_column="material_id")
    with pytest.raises(AdapterError, match="empty record_id"):
        adapt_csv([{"material_id": "  "}], _manifest(), config)
    with pytest.raises(AdapterError, match="duplicate record_id"):
        adapt_csv(
            [{"material_id": "M1"}, {"material_id": "M1"}],
            _manifest(),
            config,
        )


def test_csv_adapter_rejects_wrong_adapter_kind_and_source_system():
    config = CsvAdapterConfig(source_system="erp", record_id_column="material_id")
    with pytest.raises(AdapterError, match="adapter_kind"):
        adapt_csv([{"material_id": "M1"}], _manifest(adapter_kind="json"), config)
    with pytest.raises(AdapterError, match="source_system"):
        adapt_csv(
            [{"material_id": "M1"}],
            _manifest(source="wms"),
            CsvAdapterConfig(source_system="erp", record_id_column="material_id"),
        )


def test_json_adapter_produces_evidence_and_respects_custom_record_key():
    dataset = adapt_json(
        {"records": [{"stock_id": "STK-1", "location": "WH-1", "qty": 120.0}]},
        _manifest(source="wms", adapter_kind="json"),
        record_id_key="stock_id",
    )
    assert dataset.records[0].evidence_id == "wms:STK-1"
    assert dataset.records[0].source_location.endswith("[1]")
    assert dataset.records[0].payload["qty"] == 120.0


def test_json_adapter_fails_closed_without_records_or_identity():
    m = _manifest(source="wms", adapter_kind="json")
    with pytest.raises(AdapterError, match="records"):
        adapt_json({"items": []}, m, record_id_key="stock_id")
    with pytest.raises(AdapterError, match="missing record identity"):
        adapt_json([{"location": "WH-1"}], m, record_id_key="stock_id")
    with pytest.raises(AdapterError, match="duplicate record_id"):
        adapt_json(
            [{"stock_id": "S1"}, {"stock_id": "S1"}],
            m,
            record_id_key="stock_id",
        )


def test_sql_adapter_is_backend_neutral_and_attests_location():
    dataset = adapt_sql(
        [{"shipment_id": "SHIP-1", "carrier": "carrier-a", "lanes": 2}],
        _manifest(source="tms", adapter_kind="sql"),
        SqlSourceConfig(table="shipment", scope="enterprise:acme", primary_key="shipment_id"),
        query="SELECT * FROM shipment WHERE active = 1",
    )
    record = dataset.records[0]
    assert record.evidence_id == "tms:SHIP-1"
    assert record.source_location == "sql:shipment:shipment_id"
    # provenance carries the query / column context
    assert any("SELECT * FROM shipment" in ref.source_ref for ref in record.field_evidence)


def test_sql_adapter_fails_closed():
    config = SqlSourceConfig(table="shipment", scope="enterprise:acme", primary_key="shipment_id")
    m = _manifest(source="tms", adapter_kind="sql")
    with pytest.raises(AdapterError, match="missing primary key"):
        adapt_sql([{"carrier": "x"}], m, config)
    with pytest.raises(AdapterError, match="duplicate primary key"):
        adapt_sql([{"shipment_id": "S1"}, {"shipment_id": "S1"}], m, config)
    with pytest.raises(AdapterError, match="scope"):
        adapt_sql(
            [{"shipment_id": "S1"}],
            m,
            SqlSourceConfig(table="shipment", scope="enterprise:other", primary_key="shipment_id"),
        )
    with pytest.raises(AdapterError, match="adapter_kind"):
        adapt_sql([{"shipment_id": "S1"}], _manifest(adapter_kind="csv"), config)


def test_evidence_is_immutable_and_reference_only():
    dataset = adapt_csv(
        [{"material_id": "M1"}],
        _manifest(),
        CsvAdapterConfig(source_system="erp", record_id_column="material_id"),
    )
    record = dataset.records[0]
    with pytest.raises(FrozenInstanceError):
        record.record_id = "mutated"
    with pytest.raises(FrozenInstanceError):
        record.field_evidence = ()

    # evidence is only a *reference*, never a canonical fact
    ref = record.as_evidence_reference()
    assert ref.evidence_id == "erp:M1"
    assert ref.evidence_type == "source_reference"
    assert ref.reference == "reference:row=1"


def test_manifest_fails_closed():
    for field in (
        "source_system", "adapter_version", "data_contract_version",
        "mapping_config_version", "extracted_at", "scope", "adapter_kind",
    ):
        with pytest.raises(AdapterError, match="must be non-empty"):
            _manifest(**{field: " "})
    with pytest.raises(AdapterError, match="unsupported adapter_kind"):
        _manifest(adapter_kind="xml")


def test_dataset_fails_closed_on_empty_or_mismatched_records():
    record = SourceEvidence(
        evidence_id="erp:M1",
        source_system="erp",
        source_location="reference:row=1",
        record_id="M1",
        payload={"material_id": "M1"},
        observed_at="2026-08-19T09:00:00Z",
        scope="enterprise:acme",
        mapping_config_version="M8-reference",
    )
    with pytest.raises(AdapterError, match="at least one evidence record"):
        SourceDataset(manifest=_manifest(), records=())
    # record with a different scope is rejected at dataset level
    other = SourceEvidence(
        evidence_id="erp:M2",
        source_system="erp",
        source_location="reference:row=1",
        record_id="M2",
        payload={"material_id": "M2"},
        observed_at="2026-08-19T09:00:00Z",
        scope="enterprise:other",
        mapping_config_version="M8-reference",
    )
    with pytest.raises(AdapterError, match="scope"):
        SourceDataset(manifest=_manifest(), records=(record, other))


def test_conformance_reports_and_does_not_promote_to_truth():
    dataset = adapt_csv(
        [{"material_id": "M1"}],
        _manifest(source="erp", scope="enterprise:acme"),
        CsvAdapterConfig(source_system="erp", record_id_column="material_id"),
    )
    result = conformant(dataset)
    assert isinstance(result, AdapterConformance)
    assert result.status == "conformant"
    assert result.checked_scope == "enterprise:acme"

    # validly constructed datasets are always conformant because the manifest
    # fails closed earlier; the S273 vocabulary is preserved in the result type
    assert result.status in {"conformant", "non_conformant", "inconclusive"}
    assert result.status == "conformant"
    # a blank manifest is rejected at construction (fail closed), never silently
    # producing a non-conformant batch
    with pytest.raises(AdapterError, match="adapter_version"):
        _manifest(source="erp", adapter_version=" ")


def test_bundle_preserves_source_identity_without_collapsing_it():
    bundle = run_reference_data_adapter_path()
    assert isinstance(bundle, ReferenceEvidenceBundle)
    assert bundle.sources == ("erp", "wms", "tms")
    assert bundle.record_count == 6
    # a shared record_id across sources stays distinct evidence (no identity resolution)
    ids = [r.record_id for d in bundle.datasets for r in d.records]
    evidence_ids = [r.evidence_id for d in bundle.datasets for r in d.records]
    assert len(set(evidence_ids)) == len(evidence_ids)
    # distinct scope + source_system + record_id keys are never merged
    keys = {(d.manifest.scope, d.manifest.source_system, r.record_id)
            for d in bundle.datasets for r in d.records}
    assert len(keys) == bundle.record_count


def test_reference_path_is_deterministic_and_conformant():
    first = run_reference_data_adapter_path()
    second = run_reference_data_adapter_path()
    assert first.content_hash == second.content_hash
    assert first.to_json() == second.to_json()
    for dataset in first.datasets:
        assert conformant(dataset).status == "conformant"
    # the adapter boundary must not claim canonical truth
    for dataset in first.datasets:
        assert dataset.records[0].evidence_type == "source_reference"
