from scm_ontology.network_disruption_propagation import (
    DisruptionDependency,
    DisruptionObservation,
    NetworkDisruptionError,
    network_disruption_to_json,
    resolve_network_disruption_propagation,
)


def test_propagates_explicit_dependency_chain() -> None:
    result = resolve_network_disruption_propagation(
        [DisruptionObservation("A", 0.8, evidence_id="E1", provenance_id="P1")],
        [
            DisruptionDependency("A", "B", 0.5),
            DisruptionDependency("B", "C", 0.5),
        ],
    )
    assert [(r.affected_node_id, r.hop_count, r.impact_score) for r in result] == [
        ("B", 1, 0.4),
        ("C", 2, 0.2),
    ]
    assert result[1].path == ("A", "B", "C")
    assert result[1].evidence_ids == ("E1",)
    assert result[1].provenance_ids == ("P1",)


def test_does_not_infer_reverse_relationships() -> None:
    result = resolve_network_disruption_propagation(
        [DisruptionObservation("B", 1.0)],
        [DisruptionDependency("A", "B")],
    )
    assert result == ()


def test_cycle_is_not_traversed() -> None:
    result = resolve_network_disruption_propagation(
        [DisruptionObservation("A", 1.0)],
        [DisruptionDependency("A", "B"), DisruptionDependency("B", "A")],
    )
    assert [(r.affected_node_id, r.path) for r in result] == [("B", ("A", "B"))]


def test_max_hops_is_explicit() -> None:
    result = resolve_network_disruption_propagation(
        [DisruptionObservation("A", 1.0)],
        [DisruptionDependency("A", "B"), DisruptionDependency("B", "C")],
        max_hops=1,
    )
    assert [(r.affected_node_id, r.hop_count) for r in result] == [("B", 1)]


def test_invalid_inputs_fail_closed() -> None:
    try:
        DisruptionObservation("A", 1.1)
    except NetworkDisruptionError:
        pass
    else:
        raise AssertionError("severity outside [0,1] must fail closed")

    try:
        DisruptionDependency("A", "B", 2)
    except NetworkDisruptionError:
        pass
    else:
        raise AssertionError("propagation factor outside [0,1] must fail closed")


def test_json_is_deterministic_and_utf8_safe() -> None:
    result = resolve_network_disruption_propagation(
        [DisruptionObservation("東京A", 0.5, evidence_id="証拠")],
        [DisruptionDependency("東京A", "大阪B")],
    )
    payload = network_disruption_to_json(result)
    assert payload == network_disruption_to_json(result)
    assert "東京A" in payload
    assert "証拠" in payload
    assert '"contract_version":"S331.1"' in payload
