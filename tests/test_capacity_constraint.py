from scm_ontology.capacity_constraint import (
    CapacityConstraintError,
    CapacityFact,
    CapacityRequirement,
    capacity_constraint_to_json,
    resolve_capacity_constraints,
)


def test_computes_headroom_utilization_and_feasibility() -> None:
    result = resolve_capacity_constraints(
        [CapacityFact("CAP-001", 100, evidence_id="C1", provenance_id="P1")],
        [CapacityRequirement("CAP-001", 80, evidence_id="R1")],
    )
    assert result[0].capacity == 100
    assert result[0].required == 80
    assert result[0].headroom == 20
    assert result[0].utilization == 0.8
    assert result[0].feasible is True
    assert result[0].evidence_ids == ("C1", "R1")
    assert result[0].provenance_ids == ("P1",)


def test_over_capacity_is_infeasible_without_recommending_mitigation() -> None:
    result = resolve_capacity_constraints(
        [CapacityFact("CAP-001", 100)],
        [CapacityRequirement("CAP-001", 120)],
    )
    assert result[0].headroom == -20
    assert result[0].feasible is False


def test_exact_resource_and_unit_scope_is_preserved() -> None:
    result = resolve_capacity_constraints(
        [CapacityFact("CAP-001", 100), CapacityFact("CAP-002", 50, unit="hour")],
        [CapacityRequirement("CAP-002", 20, unit="hour")],
    )
    assert [(x.resource_id, x.unit) for x in result] == [("CAP-001", "unit"), ("CAP-002", "hour")]


def test_invalid_negative_values_fail_closed() -> None:
    try:
        CapacityFact("CAP-001", -1)
    except CapacityConstraintError:
        pass
    else:
        raise AssertionError("negative capacity must fail closed")


def test_zero_capacity_is_explicitly_undefined_utilization() -> None:
    result = resolve_capacity_constraints([], [CapacityRequirement("CAP-001", 1)])
    assert result[0].feasible is False
    assert result[0].utilization is None
    payload = capacity_constraint_to_json(result)
    assert "Infinity" not in payload


def test_json_is_deterministic_and_utf8_safe() -> None:
    result = resolve_capacity_constraints(
        [CapacityFact("東京CAP", 100, evidence_id="証拠")],
        [CapacityRequirement("東京CAP", 50, provenance_id="由来")],
    )
    payload = capacity_constraint_to_json(result)
    assert payload == capacity_constraint_to_json(result)
    assert "東京CAP" in payload
    assert "証拠" in payload
    assert '"contract_version":"S330.1"' in payload
