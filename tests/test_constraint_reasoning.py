from scm_ontology.constraint_reasoning import PathConstraint, evaluate_path
from scm_ontology.semantic_query import SemanticPathStep, SemanticSupplyChainPath


def path(*qualifiers):
    return SemanticSupplyChainPath(
        at="2026-06-01T00:00:00+00:00",
        node_ids=("A", "B", "C"),
        steps=tuple(
            SemanticPathStep(str(i), "ships", "A" if i == 0 else "B", "B" if i == 0 else "C", q)
            for i, q in enumerate(qualifiers)
        ),
    )


def test_path_passes_lead_time_and_capacity_constraints():
    result = evaluate_path(path({"lead_time_days": 2, "capacity": 120}, {"lead_time_days": 3, "capacity": 100}), PathConstraint(max_total_lead_time_days=6, min_total_capacity=90))
    assert result.feasible is True
    assert all(check.passed for check in result.checks)


def test_path_fails_when_bottleneck_capacity_is_too_low():
    result = evaluate_path(path({"lead_time_days": 2, "capacity": 120}, {"lead_time_days": 3, "capacity": 80}), PathConstraint(min_total_capacity=90))
    assert result.feasible is False
    assert result.checks[0].actual == 80


def test_missing_constraint_data_is_not_inferred():
    result = evaluate_path(path({"capacity": 120}, {"capacity": 100}), PathConstraint(max_total_lead_time_days=6))
    assert result.feasible is False
    assert result.checks[0].reason == "missing lead_time_days"
