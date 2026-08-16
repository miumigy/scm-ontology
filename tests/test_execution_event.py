from scm_ontology.auditable_reasoning import build_reasoning_result
from scm_ontology.constraint_reasoning import PathConstraint, evaluate_path
from scm_ontology.decision_trace import record_planning_result
from scm_ontology.execution_boundary import build_execution_request
from scm_ontology.execution_event import execution_event_to_mapping, record_execution_event
from scm_ontology.planning_boundary import build_planning_request
from scm_ontology.semantic_query import SemanticPathStep, SemanticSupplyChainPath


def _request():
    path = SemanticSupplyChainPath(
        at="2026-06-01T00:00:00+00:00",
        node_ids=("supplier", "factory"),
        steps=(SemanticPathStep("r1", "supplies", "supplier", "factory", {"lead_time_days": 2}),),
    )
    reasoning = build_reasoning_result(evaluate_path(path, PathConstraint(max_total_lead_time_days=5)))
    planning = build_planning_request(reasoning, source_node_id="supplier", target_node_id="factory", objective="minimize_cost")
    trace = record_planning_result(planning, reasoning, plan_id="plan-1", status="accepted")
    return build_execution_request(trace, execution_target="WMS", action="release_order", payload={"order_id": "o-1"})


def test_execution_event_is_deterministic_and_traceable():
    request = _request()
    first = record_execution_event(request, status="succeeded", occurred_at="2026-06-01T01:00:00+00:00", payload={"external_id": "w-1"})
    second = record_execution_event(request, status="succeeded", occurred_at="2026-06-01T01:00:00+00:00", payload={"external_id": "w-1"})
    assert first == second
    assert first.execution_request_id == request.request_id
    assert first.plan_id == request.plan_id
    assert first.decision_trace_id == request.decision_trace_id
    assert execution_event_to_mapping(first)["status"] == "succeeded"


def test_execution_event_rejects_unknown_status():
    try:
        record_execution_event(_request(), status="invented", occurred_at="2026-06-01T01:00:00+00:00")
    except ValueError as exc:
        assert "unsupported execution status" in str(exc)
    else:
        raise AssertionError("unknown execution status must be rejected")
