from scm_ontology.auditable_reasoning import build_reasoning_result
from scm_ontology.constraint_reasoning import PathConstraint, evaluate_path
from scm_ontology.decision_trace import record_planning_result
from scm_ontology.execution_boundary import build_execution_request, execution_request_to_mapping
from scm_ontology.planning_boundary import build_planning_request
from scm_ontology.semantic_query import SemanticPathStep, SemanticSupplyChainPath


def _trace():
    path = SemanticSupplyChainPath(
        at="2026-06-01T00:00:00+00:00",
        node_ids=("supplier", "factory"),
        steps=(SemanticPathStep("r1", "supplies", "supplier", "factory", {"lead_time_days": 2}),),
    )
    reasoning = build_reasoning_result(evaluate_path(path, PathConstraint(max_total_lead_time_days=5)))
    planning = build_planning_request(reasoning, source_node_id="supplier", target_node_id="factory", objective="minimize_cost")
    return record_planning_result(planning, reasoning, plan_id="plan-1", status="accepted")


def test_execution_request_is_deterministic_and_traceable():
    trace = _trace()
    first = build_execution_request(trace, execution_target="WMS", action="release_order", payload={"order_id": "o-1"})
    second = build_execution_request(trace, execution_target="WMS", action="release_order", payload={"order_id": "o-1"})
    assert first == second
    assert first.plan_id == "plan-1"
    assert first.decision_trace_id == trace.trace_id
    assert execution_request_to_mapping(first)["action"] == "release_order"


def test_execution_request_does_not_execute():
    trace = _trace()
    request = build_execution_request(trace, execution_target="ERP", action="create_purchase_order")
    assert request.request_id
    assert request.payload == {}
