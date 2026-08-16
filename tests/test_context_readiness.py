import pytest

from scm_ontology.context_readiness import (
    ContextReadinessError,
    require_context_ready,
    validate_context_readiness,
)
from scm_ontology.decision_context import DecisionObservation, build_decision_context


def test_context_is_ready_when_observations_have_evidence_and_provenance():
    context = build_decision_context(
        "ctx-1",
        [DecisionObservation("q2", 2, ("e2",), ("p2",)), DecisionObservation("q1", 1, ("e1",), ("p1",))],
    )
    status = validate_context_readiness(context)
    assert status.ready is True
    assert status.observation_count == 2
    assert status.missing_evidence_questions == ()
    assert status.missing_provenance_questions == ()
    assert require_context_ready(context) is context


def test_readiness_fails_closed_for_missing_evidence_or_provenance():
    context = build_decision_context(
        "ctx-2",
        [DecisionObservation("q1", 1, (), ("p1",)), DecisionObservation("q2", 2, ("e2",), ())],
    )
    status = validate_context_readiness(context)
    assert status.ready is False
    assert status.missing_evidence_questions == ("q1",)
    assert status.missing_provenance_questions == ("q2",)
    with pytest.raises(ContextReadinessError):
        require_context_ready(context)


def test_empty_context_is_not_ready():
    context = build_decision_context("ctx-3", [])
    status = validate_context_readiness(context)
    assert status.ready is False
    assert status.observation_count == 0
