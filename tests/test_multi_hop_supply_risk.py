from scm_ontology.multi_hop_supply_risk import (
    MultiHopSupplyRiskError,
    SupplyDependency,
    SupplyRiskObservation,
    multi_hop_supply_risk_to_json,
    resolve_multi_hop_supply_risk,
)


def test_propagates_explicit_upstream_risk_across_multiple_hops() -> None:
    result = resolve_multi_hop_supply_risk(
        [
            SupplyDependency("S1", "P1", evidence_id="E1"),
            SupplyDependency("P1", "F1", evidence_id="E2"),
        ],
        [SupplyRiskObservation("S1", 0.8, evidence_id="E0", provenance_id="SRC")],
    )
    assert [(x.node_id, x.hop_count, x.path) for x in result] == [
        ("F1", 2, ("S1", "P1", "F1")),
        ("P1", 1, ("S1", "P1")),
    ]
    assert result[0].risk_score == 0.8
    assert result[0].evidence_ids == ("E0", "E1", "E2")


def test_does_not_infer_reverse_relationships() -> None:
    result = resolve_multi_hop_supply_risk(
        [SupplyDependency("S1", "P1")],
        [SupplyRiskObservation("P1", 0.9)],
    )
    assert result == ()


def test_cycle_is_not_traversed() -> None:
    result = resolve_multi_hop_supply_risk(
        [SupplyDependency("A", "B"), SupplyDependency("B", "A")],
        [SupplyRiskObservation("A", 0.7)],
    )
    assert len(result) == 1
    assert result[0].path == ("A", "B")


def test_max_hops_is_explicit_and_fail_closed() -> None:
    try:
        resolve_multi_hop_supply_risk([], [], max_hops=0)
    except MultiHopSupplyRiskError:
        pass
    else:
        raise AssertionError("max_hops=0 must fail closed")


def test_json_is_deterministic_and_utf8_safe() -> None:
    result = resolve_multi_hop_supply_risk(
        [SupplyDependency("東京S", "大阪P", evidence_id="証拠")],
        [SupplyRiskObservation("東京S", 0.5, provenance_id="由来")],
    )
    payload = multi_hop_supply_risk_to_json(result)
    assert payload == multi_hop_supply_risk_to_json(result)
    assert "東京S" in payload
    assert "証拠" in payload
    assert '"contract_version":"S329.1"' in payload
