from scm_ontology.decision_context import (
    DecisionContextError,
    DecisionObservation,
    build_decision_context,
    decision_context_to_json,
)


def test_builds_deterministic_context_and_sorts_observations() -> None:
    context = build_decision_context(
        "CTX-1",
        [
            DecisionObservation("inventory-position", {"available": 10}, ("E2", "E1"), ("P2",)),
            DecisionObservation("demand-supply-gap", {"gap": 4}, ("E3",)),
        ],
    )
    assert [o.question_id for o in context.observations] == ["demand-supply-gap", "inventory-position"]
    assert context.observations[1].evidence_ids == ("E1", "E2")


def test_duplicate_question_id_fails_closed() -> None:
    try:
        build_decision_context("CTX-1", [DecisionObservation("inventory-position", 1), DecisionObservation("inventory-position", 2)])
    except DecisionContextError:
        pass
    else:
        raise AssertionError("duplicate question_id must fail closed")


def test_empty_context_id_fails_closed() -> None:
    try:
        build_decision_context("", [])
    except DecisionContextError:
        pass
    else:
        raise AssertionError("empty context_id must fail closed")


def test_json_is_deterministic_and_utf8_safe() -> None:
    context = build_decision_context("東京-CTX", [DecisionObservation("capacity-constraint", {"headroom": 2}, ("証拠",), ("由来",))])
    payload = decision_context_to_json(context)
    assert payload == decision_context_to_json(context)
    assert "東京-CTX" in payload
    assert "証拠" in payload
    assert '"contract_version":"S333.1"' in payload
