from scm_ontology.context_readiness import ContextReadinessError
from scm_ontology.decision_context import DecisionContext, DecisionObservation
from scm_ontology.reasoning_input import ReasoningInput, build_reasoning_input


def ready_context():
    return DecisionContext(
        context_id="ctx-1",
        observations=(
            DecisionObservation("q2", {"value": 2}, ("e2",), ("p2",)),
            DecisionObservation("q1", {"value": 1}, ("e1", "e2"), ("p1",)),
        ),
    )


def test_build_reasoning_input_is_immutable_and_deterministic():
    result = build_reasoning_input(ready_context())
    assert isinstance(result, ReasoningInput)
    assert result.context_id == "ctx-1"
    assert result.evidence_ids == ("e1", "e2")
    assert result.provenance_ids == ("p1", "p2")
    # S333 canonicalizes DecisionContext observations by question_id.
    assert result.observations[0].question_id == "q1"
    assert result.to_mapping()["contract_version"] == "S342.1"


def test_build_reasoning_input_fails_closed_for_unready_context():
    context = DecisionContext(
        context_id="ctx-2",
        observations=(DecisionObservation("q1", {"value": 1}, (), ("p1",)),),
    )
    try:
        build_reasoning_input(context)
    except ContextReadinessError:
        pass
    else:
        raise AssertionError("unready context must not enter reasoning")
