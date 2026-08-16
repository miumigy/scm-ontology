from scm_ontology.demand_supply_gap import (
    DemandSupplyGapError,
    DemandSupplyRecord,
    demand_supply_gap_to_json,
    demand_supply_gap_to_mapping,
    resolve_demand_supply_gap,
)


def test_resolves_explicit_demand_supply_gap_with_lineage():
    result = resolve_demand_supply_gap(
        [
            DemandSupplyRecord("P-1", 100, "demand", "unit", "2026-01-01", "2026-01-31", evidence_id="e2", provenance_id="erp"),
            DemandSupplyRecord("P-1", 60, "supply", "unit", "2026-01-01", "2026-01-31", evidence_id="e1", provenance_id="aps"),
            DemandSupplyRecord("P-1", 25, "supply", "unit", "2026-01-01", "2026-01-31", evidence_id="e3", provenance_id="wms"),
        ]
    )

    assert len(result) == 1
    assert result[0].demand == 100
    assert result[0].supply == 85
    assert result[0].gap == 15
    assert result[0].evidence_ids == ("e1", "e2", "e3")
    assert result[0].provenance_ids == ("aps", "erp", "wms")


def test_gap_is_zero_when_supply_meets_or_exceeds_demand():
    met = resolve_demand_supply_gap(
        [
            DemandSupplyRecord("P-1", 10, "demand", "unit", "2026-01-01", "2026-01-31"),
            DemandSupplyRecord("P-1", 10, "supply", "unit", "2026-01-01", "2026-01-31"),
        ]
    )[0]
    assert met.gap == 0

    exceeded = resolve_demand_supply_gap(
        [
            DemandSupplyRecord("P-1", 10, "demand", "unit", "2026-01-01", "2026-01-31"),
            DemandSupplyRecord("P-1", 20, "supply", "unit", "2026-01-01", "2026-01-31"),
        ]
    )[0]
    assert exceeded.gap == 0


def test_grouping_is_scoped_to_explicit_item_unit_and_period():
    result = resolve_demand_supply_gap(
        [
            DemandSupplyRecord("P-1", 10, "demand", "unit", "2026-01-01", "2026-01-31"),
            DemandSupplyRecord("P-2", 10, "demand", "unit", "2026-01-01", "2026-01-31"),
            DemandSupplyRecord("P-1", 10, "demand", "unit", "2026-02-01", "2026-02-28"),
            DemandSupplyRecord("P-1", 10, "demand", "kg", "2026-01-01", "2026-01-31"),
        ]
    )
    assert [(g.item_id, g.unit, g.period_start, g.period_end) for g in result] == [
        ("P-1", "kg", "2026-01-01", "2026-01-31"),
        ("P-1", "unit", "2026-01-01", "2026-01-31"),
        ("P-1", "unit", "2026-02-01", "2026-02-28"),
        ("P-2", "unit", "2026-01-01", "2026-01-31"),
    ]


def test_supply_only_or_demand_only_sides_are_zero_filled():
    supply_only = resolve_demand_supply_gap(
        [DemandSupplyRecord("P-1", 5, "supply", "unit", "2026-01-01", "2026-01-31")]
    )[0]
    assert supply_only.demand == 0
    assert supply_only.supply == 5
    assert supply_only.gap == 0

    demand_only = resolve_demand_supply_gap(
        [DemandSupplyRecord("P-1", 7, "demand", "unit", "2026-01-01", "2026-01-31")]
    )[0]
    assert demand_only.demand == 7
    assert demand_only.supply == 0
    assert demand_only.gap == 7


def test_invalid_kind_fails_closed():
    try:
        DemandSupplyRecord("P-1", 1, "forecast")
    except DemandSupplyGapError as exc:
        assert "kind" in str(exc)
    else:
        raise AssertionError("invalid kind must fail")


def test_negative_quantity_fails_closed():
    try:
        DemandSupplyRecord("P-1", -1, "demand")
    except DemandSupplyGapError as exc:
        assert "non-negative" in str(exc)
    else:
        raise AssertionError("negative quantity must fail")


def test_period_end_before_start_fails_closed():
    try:
        DemandSupplyRecord("P-1", 1, "demand", "unit", "2026-02-01", "2026-01-01")
    except DemandSupplyGapError as exc:
        assert "period_end" in str(exc)
    else:
        raise AssertionError("reversed period must fail")


def test_mapping_and_json_are_deterministic_and_utf8_safe():
    result = resolve_demand_supply_gap(
        [DemandSupplyRecord("部品-1", 100, "demand", "unit", "2026-01-01", "2026-01-31", evidence_id="証拠-1", provenance_id="東京APS")]
    )
    mapping = demand_supply_gap_to_mapping(result)
    assert mapping["contract_version"] == "S327.1"
    assert "東京" in demand_supply_gap_to_json(result)
    assert "部品-1" in demand_supply_gap_to_json(result)
    assert "証拠-1" in demand_supply_gap_to_json(result)
    assert demand_supply_gap_to_json(result) == demand_supply_gap_to_json(result)


def test_empty_input_is_a_valid_empty_answer():
    assert demand_supply_gap_to_mapping(()) == {
        "contract_version": "S327.1",
        "gaps": [],
    }
