from scm_ontology.reasoning_output import ReasoningOutput, ReasoningOutputError


def test_reasoning_output_is_immutable_and_deterministic():
    result = ReasoningOutput(
        context_id="ctx-1",
        proposal={"action": "expedite"},
        rationale="Lead time risk exceeds threshold.",
        evidence_ids=("e2", "e1", "e1"),
        provenance_ids=("p2", "p1", "p2"),
        confidence=0.8,
    )
    assert isinstance(result, ReasoningOutput)
    assert result.evidence_ids == ("e1", "e2")
    assert result.provenance_ids == ("p1", "p2")
    assert result.to_mapping()["contract_version"] == "S343.1"
    assert result.to_mapping()["confidence"] == 0.8


def test_reasoning_output_rejects_invalid_confidence_and_rationale():
    try:
        ReasoningOutput("ctx-1", {}, "ok", confidence=1.1)
    except ReasoningOutputError:
        pass
    else:
        raise AssertionError("confidence outside [0,1] must fail")

    try:
        ReasoningOutput("ctx-1", {}, " ")
    except ReasoningOutputError:
        pass
    else:
        raise AssertionError("blank rationale must fail")
