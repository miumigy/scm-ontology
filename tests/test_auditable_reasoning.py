from scm_ontology.auditable_reasoning import build_reasoning_result
from scm_ontology.constraint_reasoning import evaluate_path, PathConstraint
from scm_ontology.semantic_query import SemanticSupplyChainPath, SemanticPathStep


def _result():
    path = SemanticSupplyChainPath(
        at="2026-06-01T00:00:00+00:00",
        node_ids=("supplier", "factory"),
        steps=(SemanticPathStep("r1", "supplies", "supplier", "factory", {"lead_time_days": 3, "capacity": 100}),),
    )
    return evaluate_path(path, PathConstraint(max_total_lead_time_days=5, min_total_capacity=90))


def test_auditable_result_is_deterministic_and_contains_evidence():
    first = build_reasoning_result(_result())
    second = build_reasoning_result(_result())
    assert first == second
    assert first.status == "feasible"
    assert first.result_id
    assert first.evidence[0].relationship_id == "r1"
    assert first.checks[0]["actual"] == 3.0


def test_failed_reasoning_is_auditable_too():
    path = SemanticSupplyChainPath(
        at="2026-06-01T00:00:00+00:00",
        node_ids=("supplier", "factory"),
        steps=(SemanticPathStep("r1", "supplies", "supplier", "factory", {"lead_time_days": 8}),),
    )
    result = build_reasoning_result(evaluate_path(path, PathConstraint(max_total_lead_time_days=5)))
    assert result.status == "infeasible"
    assert result.checks[0]["passed"] is False
    assert result.evidence[0].qualifiers["lead_time_days"] == 8
