from scm_ontology.constraint_evaluation import (
    ConstraintEvaluation,
    ConstraintResult,
    EvaluationContext,
)


def test_result_distinguishes_unknown_from_violation():
    assert ConstraintResult.UNKNOWN != ConstraintResult.VIOLATED


def test_evaluation_is_a_result_not_an_evaluator():
    result = ConstraintEvaluation(ConstraintResult.SATISFIED, "all required facts available")
    assert result.result is ConstraintResult.SATISFIED
    assert not hasattr(result, "evaluate")


def test_context_is_supplied_to_runtime():
    context = EvaluationContext(facts={"capacity": 100})
    assert context.facts["capacity"] == 100
