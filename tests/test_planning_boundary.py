from scm_ontology.auditable_reasoning import build_reasoning_result
from scm_ontology.constraint_reasoning import PathConstraint, evaluate_path
from scm_ontology.planning_boundary import build_planning_request, planning_request_to_mapping
from scm_ontology.semantic_query import SemanticPathStep, SemanticSupplyChainPath


def _reasoning():
    path = SemanticSupplyChainPath(
        at="2026-06-01T00:00:00+00:00",
        node_ids=("supplier", "factory", "customer"),
        steps=(
            SemanticPathStep("r1", "supplies", "supplier", "factory", {"lead_time_days": 2}),
            SemanticPathStep("r2", "delivers", "factory", "customer", {"lead_time_days": 2}),
        ),
    )
    return build_reasoning_result(evaluate_path(path, PathConstraint(max_total_lead_time_days=5)))


def test_planning_request_is_deterministic_and_does_not_select_plan():
    reasoning = _reasoning()
    first = build_planning_request(
        reasoning,
        source_node_id="supplier",
        target_node_id="customer",
        objective="minimize_total_cost",
        constraints={"max_cost": 1000},
    )
    second = build_planning_request(
        reasoning,
        source_node_id="supplier",
        target_node_id="customer",
        objective="minimize_total_cost",
        constraints={"max_cost": 1000},
    )
    assert first == second
    assert first.request_id
    assert first.reasoning_result_id == reasoning.result_id
    assert planning_request_to_mapping(first)["objective"] == "minimize_total_cost"


def test_infeasible_reasoning_cannot_cross_into_planning():
    path = SemanticSupplyChainPath(
        at="2026-06-01T00:00:00+00:00",
        node_ids=("supplier", "factory"),
        steps=(SemanticPathStep("r1", "supplies", "supplier", "factory", {"lead_time_days": 8}),),
    )
    reasoning = build_reasoning_result(evaluate_path(path, PathConstraint(max_total_lead_time_days=5)))
    try:
        build_planning_request(reasoning, source_node_id="supplier", target_node_id="factory", objective="minimize_cost")
    except ValueError as exc:
        assert "feasible" in str(exc)
    else:
        raise AssertionError("infeasible reasoning must not create a planning request")
