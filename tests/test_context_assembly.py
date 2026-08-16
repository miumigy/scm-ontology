import pytest

from scm_ontology.context_assembly import assemble_decision_context
from scm_ontology.decision_context import DecisionContext, DecisionContextError, DecisionObservation


def test_assembly_reuses_canonical_context_and_is_deterministic():
    observations = (
        DecisionObservation("q2", {"value": "大阪"}, ("e2",), ("p2",)),
        DecisionObservation("q1", {"value": "東京"}, ("e1",), ("p1",)),
    )

    context = assemble_decision_context("ctx-1", observations)

    assert isinstance(context, DecisionContext)
    assert [o.question_id for o in context.observations] == ["q1", "q2"]
    assert context.observations[0].evidence_ids == ("e1",)
    assert context.observations[1].provenance_ids == ("p2",)


def test_assembly_rejects_duplicate_question_ids():
    observations = (
        DecisionObservation("q1", 1),
        DecisionObservation("q1", 2),
    )

    with pytest.raises(DecisionContextError, match="question_id must be unique"):
        assemble_decision_context("ctx-1", observations)


def test_assembly_rejects_blank_context_id():
    with pytest.raises(DecisionContextError, match="context_id must be non-empty"):
        assemble_decision_context(" ", ())
