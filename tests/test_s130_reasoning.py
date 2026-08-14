import pytest

from scm_ontology.s130_reasoning import (
    Evaluation,
    EvaluationResult,
    evaluate_known,
)


def test_constraint_violation_requires_evidence() -> None:
    with pytest.raises(ValueError):
        Evaluation(
            semantic_ref="constraint:c1",
            input_ref="state:s1",
            result=EvaluationResult.VIOLATED,
        )


def test_unknown_is_not_satisfied() -> None:
    evaluation = Evaluation(
        semantic_ref="rule:r1",
        input_ref="prediction:p1",
        result=EvaluationResult.UNKNOWN,
        evidence_refs=("e1",),
    )
    assert evaluation.result is EvaluationResult.UNKNOWN
    assert evaluation.result is not EvaluationResult.SATISFIED


def test_reasoning_does_not_become_decision() -> None:
    evaluation = evaluate_known(
        True,
        semantic_ref="constraint:c1",
        input_ref="state:s1",
        evidence_refs=("obs:1",),
    )
    assert evaluation.result is EvaluationResult.SATISFIED
    assert evaluation.can_be_decision is False


def test_scenario_scope_is_preserved() -> None:
    evaluation = evaluate_known(
        False,
        semantic_ref="rule:r2",
        input_ref="state:scenario-1",
        evidence_refs=("e2",),
        scenario_ref="scenario:1",
    )
    assert evaluation.result is EvaluationResult.VIOLATED
    assert evaluation.scenario_ref == "scenario:1"
