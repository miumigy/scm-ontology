from scm_ontology.auditable_reasoning import build_reasoning_result
from scm_ontology.constraint_reasoning import PathConstraint, evaluate_path
from scm_ontology.decision_trace import record_planning_result
from scm_ontology.execution_boundary import build_execution_request
from scm_ontology.execution_event import record_execution_event
from scm_ontology.plan_actual import compare_plan_actual, plan_actual_to_mapping
from scm_ontology.planning_boundary import build_planning_request
from scm_ontology.semantic_query import SemanticPathStep, SemanticSupplyChainPath


def _trace_and_event():
    path = SemanticSupplyChainPath(
        at="2026-06-01T00:00:00+00:00",
        node_ids=("supplier", "factory"),
        steps=(SemanticPathStep("r1", "supplies", "supplier", "factory", {"lead_time_days": 3}),),
    )
    reasoning = build_reasoning_result(evaluate_path(path, PathConstraint(max_total_lead_time_days=5)))
    request = build_planning_request(reasoning, source_node_id="supplier", target_node_id="factory", objective="minimize_cost")
    trace = record_planning_result(request, reasoning, plan_id="plan-1", status="accepted", decision_payload={"planned_metrics": {"lead_time_days": 3, "cost": 100}})
    execution = build_execution_request(trace, execution_target="WMS", action="release_order")
    event = record_execution_event(execution, status="succeeded", occurred_at="2026-06-02T00:00:00+00:00", payload={"actual_metrics": {"lead_time_days": 5, "cost": 110}})
    return trace, event


def test_plan_actual_comparison_is_explicit_and_traceable():
    trace, event = _trace_and_event()
    result = compare_plan_actual(trace, event)
    assert result.decision_trace_id == trace.trace_id
    assert [(v.metric, v.variance, v.status) for v in result.variances] == [("cost", 10.0, "above_plan"), ("lead_time_days", 2.0, "above_plan")]
    assert plan_actual_to_mapping(result)["execution_event_id"] == event.event_id


def test_missing_metric_is_not_inferred():
    trace, event = _trace_and_event()
    event = type(event)(event.event_id, event.execution_request_id, event.plan_id, event.decision_trace_id, event.status, event.occurred_at, {"actual_metrics": {"cost": 110}})
    result = compare_plan_actual(trace, event)
    lead = next(v for v in result.variances if v.metric == "lead_time_days")
    assert lead.status == "insufficient_data"
    assert lead.variance is None
