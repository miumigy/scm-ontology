import pytest

from scm_ontology.graph_reasoning_projection import GraphReasoningObservation
from scm_ontology.reasoning_assembly import ReasoningAssemblyError, assemble_reasoning_input


def observation(question_id: str, evidence: tuple[str, ...], provenance: tuple[str, ...]):
    return GraphReasoningObservation(
        question_id=question_id,
        value={"question_id": question_id},
        evidence_ids=evidence,
        provenance_ids=provenance,
    )


def test_assembly_is_deterministic_and_aggregates_support_metadata():
    result = assemble_reasoning_input(
        "ctx-1",
        (
            observation("q2", ("e2",), ("p2",)),
            observation("q1", ("e1", "e2"), ("p1",)),
        ),
    )

    assert result.context_id == "ctx-1"
    assert [item.question_id for item in result.observations] == ["q1", "q2"]
    assert result.evidence_ids == ("e1", "e2")
    assert result.provenance_ids == ("p1", "p2")
    assert result.to_mapping()["contract_version"] == "S342.1"


def test_assembly_rejects_duplicate_questions():
    with pytest.raises(ReasoningAssemblyError, match="question_id must be unique"):
        assemble_reasoning_input(
            "ctx-1",
            (
                observation("q1", ("e1",), ("p1",)),
                observation("q1", ("e2",), ("p2",)),
            ),
        )


def test_assembly_fails_closed_for_missing_support_metadata():
    with pytest.raises(ReasoningAssemblyError, match="not ready for downstream reasoning"):
        assemble_reasoning_input(
            "ctx-1",
            (observation("q1", (), ("p1",)),),
        )

    with pytest.raises(ReasoningAssemblyError, match="not ready for downstream reasoning"):
        assemble_reasoning_input(
            "ctx-1",
            (observation("q1", ("e1",), ()),),
        )


def test_assembly_rejects_invalid_context_and_observation_inputs():
    with pytest.raises(ReasoningAssemblyError, match="context_id must be non-empty"):
        assemble_reasoning_input("", (observation("q1", ("e1",), ("p1",)),))

    with pytest.raises(ReasoningAssemblyError, match="observations must not be empty"):
        assemble_reasoning_input("ctx-1", ())

    with pytest.raises(ReasoningAssemblyError, match="GraphReasoningObservation"):
        assemble_reasoning_input("ctx-1", (object(),))
