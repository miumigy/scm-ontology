from scm_ontology.auditable_reasoning import build_reasoning_result
from scm_ontology.constraint_reasoning import PathConstraint, evaluate_path
from scm_ontology.decision_trace import decision_trace_to_mapping, record_planning_result
from scm_ontology.planning_boundary import build_planning_request
from scm_ontology.semantic_query import SemanticPathStep, SemanticSupplyChainPath


def _fixtures():
    path = SemanticSupplyChainPath(
        at="2026-06-01T00:00:00+00:00",
        node_ids=("supplier", "factory"),
        steps=(SemanticPathStep("r1", "supplies", "supplier", "factory", {"lead_time_days": 2}),),
    )
    reasoning = build_reasoning_result(evaluate_path(path, PathConstraint(max_total_lead_time_days=5)))
    request = build_planning_request(reasoning, source_node_id="supplier", target_node_id="factory", objective="minimize_cost")
    return reasoning, request


def test_decision_trace_is_deterministic_and_links_plan_to_reasoning():
    reasoning, request = _fixtures()
    first = record_planning_result(request, reasoning, plan_id="plan-1", status="accepted", decision_payload={"cost": 42})
    second = record_planning_result(request, reasoning, plan_id="plan-1", status="accepted", decision_payload={"cost": 42})
    assert first == second
    assert first.planning_result.planning_request_id == request.request_id
    assert first.reasoning_result_id == reasoning.result_id
    assert decision_trace_to_mapping(first)["plan_id"] == "plan-1"


def test_decision_trace_rejects_mismatched_reasoning():
    reasoning, request = _fixtures()
    other = type(reasoning)(reasoning.result_id + "x", reasoning.status, reasoning.at, reasoning.node_ids, reasoning.checks, reasoning.evidence)
    try:
        record_planning_result(request, other, plan_id="plan-1", status="accepted")
    except ValueError as exc:
        assert "do not match" in str(exc)
    else:
        raise AssertionError("mismatched reasoning must be rejected")
