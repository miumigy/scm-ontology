from scm_ontology.supplier_delay_impact import (
    SupplierCommitment,
    SupplierDelayEvent,
    SupplierDelayImpactError,
    resolve_supplier_delay_impact,
    supplier_delay_impact_to_json,
)


def test_resolves_explicit_supplier_delay_and_lineage() -> None:
    result = resolve_supplier_delay_impact(
        [SupplierCommitment("S1", "P1", "2026-01-01", "2026-01-10", evidence_id="c-e", provenance_id="erp")],
        [SupplierDelayEvent("S1", "P1", "2026-01-10", "2026-01-14", evidence_id="d-e", provenance_id="edi")],
    )
    assert len(result) == 1
    assert result[0].delay_days == 4
    assert result[0].evidence_ids == ("c-e", "d-e")
    assert result[0].provenance_ids == ("edi", "erp")


def test_unmatched_delay_fails_closed_by_not_inventing_scope() -> None:
    result = resolve_supplier_delay_impact(
        [SupplierCommitment("S1", "P1", "2026-01-01", "2026-01-10")],
        [SupplierDelayEvent("S2", "P1", "2026-01-10", "2026-01-14")],
    )
    assert result == ()


def test_early_actual_date_has_zero_delay() -> None:
    result = resolve_supplier_delay_impact(
        [SupplierCommitment("S1", "P1", "2026-01-01", "2026-01-10")],
        [SupplierDelayEvent("S1", "P1", "2026-01-10", "2026-01-10")],
    )
    assert result[0].delay_days == 0


def test_invalid_temporal_order_fails_closed() -> None:
    try:
        SupplierDelayEvent("S1", "P1", "2026-01-10", "2026-01-09")
    except SupplierDelayImpactError:
        pass
    else:
        raise AssertionError("actual_at before expected_at must fail closed")


def test_json_is_deterministic_and_utf8_safe() -> None:
    result = resolve_supplier_delay_impact(
        [SupplierCommitment("東京S", "大阪P", "2026-01-01", "2026-01-10", evidence_id="証拠")],
        [SupplierDelayEvent("東京S", "大阪P", "2026-01-10", "2026-01-12", provenance_id="由来")],
    )
    payload = supplier_delay_impact_to_json(result)
    assert payload == supplier_delay_impact_to_json(result)
    assert "東京S" in payload
    assert "証拠" in payload
    assert '"contract_version":"S328.1"' in payload
