from scm_ontology.plan_actual_commitment_reconciliation import (
    ReconciliationError,
    ReconciliationFact,
    reconciliation_to_json,
    resolve_plan_actual_commitment,
)


def test_reconciles_explicit_plan_actual_commitment_scope() -> None:
    result = resolve_plan_actual_commitment([
        ReconciliationFact("P1", "2026-08-01", "2026-08-31", 100, "plan", evidence_id="E1"),
        ReconciliationFact("P1", "2026-08-01", "2026-08-31", 90, "actual", evidence_id="E2"),
        ReconciliationFact("P1", "2026-08-01", "2026-08-31", 95, "commitment", provenance_id="PR1"),
    ])
    assert len(result) == 1
    assert result[0].actual_vs_plan == -10
    assert result[0].commitment_vs_plan == -5
    assert result[0].actual_vs_commitment == -5
    assert result[0].evidence_ids == ("E1", "E2")
    assert result[0].provenance_ids == ("PR1",)


def test_scopes_by_item_period_and_unit() -> None:
    result = resolve_plan_actual_commitment([
        ReconciliationFact("B", "2026-08-01", "2026-08-31", 10, "plan"),
        ReconciliationFact("A", "2026-09-01", "2026-09-30", 20, "actual"),
        ReconciliationFact("A", "2026-08-01", "2026-08-31", 30, "commitment"),
    ])
    assert [(r.item_id, r.period_start) for r in result] == [
        ("A", "2026-08-01"), ("A", "2026-09-01"), ("B", "2026-08-01")
    ]


def test_invalid_fact_class_fails_closed() -> None:
    try:
        ReconciliationFact("P1", "2026-08-01", "2026-08-31", 1, "forecast")
    except ReconciliationError:
        pass
    else:
        raise AssertionError("invalid fact class must fail closed")


def test_json_is_deterministic_and_utf8_safe() -> None:
    result = resolve_plan_actual_commitment([
        ReconciliationFact("東京P", "2026-08-01", "2026-08-31", 10, "plan", evidence_id="証拠"),
    ])
    payload = reconciliation_to_json(result)
    assert payload == reconciliation_to_json(result)
    assert "東京P" in payload
    assert "証拠" in payload
    assert '"contract_version":"S332.1"' in payload


def test_empty_input_is_empty_answer() -> None:
    assert resolve_plan_actual_commitment([]) == ()
