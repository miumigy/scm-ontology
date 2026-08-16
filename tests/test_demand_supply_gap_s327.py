from scm_ontology.demand_supply_gap import (
    DemandSupplyFact,
    DemandSupplyGapError,
    demand_supply_gap_to_json,
    resolve_demand_supply_gap,
)


def test_aggregates_scope_and_computes_gap() -> None:
    result = resolve_demand_supply_gap([
        DemandSupplyFact("P1", "L1", 100, "demand", evidence_id="E2"),
        DemandSupplyFact("P1", "L1", 30, "demand", evidence_id="E1"),
        DemandSupplyFact("P1", "L1", 80, "supply", provenance_id="PR1"),
    ])
    assert result[0].demand == 130
    assert result[0].supply == 80
    assert result[0].gap == 50
    assert result[0].evidence_ids == ("E1", "E2")
    assert result[0].provenance_ids == ("PR1",)


def test_scopes_are_deterministically_sorted() -> None:
    result = resolve_demand_supply_gap([
        DemandSupplyFact("P2", "L2", 10),
        DemandSupplyFact("P1", "L2", 20),
        DemandSupplyFact("P1", "L1", 30),
    ])
    assert [(r.product_id, r.location_id) for r in result] == [("P1", "L1"), ("P1", "L2"), ("P2", "L2")]


def test_invalid_fact_class_fails_closed() -> None:
    try:
        DemandSupplyFact("P1", "L1", 1, "forecast")
    except DemandSupplyGapError:
        pass
    else:
        raise AssertionError("invalid fact class must fail closed")


def test_json_is_deterministic_and_utf8_safe() -> None:
    facts = [
        DemandSupplyFact("東京P", "大阪L", 10, "demand", evidence_id="証拠"),
        DemandSupplyFact("東京P", "大阪L", 7, "supply", provenance_id="由来"),
    ]
    payload = demand_supply_gap_to_json(resolve_demand_supply_gap(facts))
    assert payload == demand_supply_gap_to_json(resolve_demand_supply_gap(facts))
    assert "東京P" in payload and "証拠" in payload
    assert '"contract_version":"S327.1"' in payload


def test_empty_input_is_empty_answer() -> None:
    assert resolve_demand_supply_gap([]) == ()
