"""Closed-loop comparison between planned assumptions and observed execution facts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .execution_event import ExecutionEvent
from .decision_trace import DecisionTrace


@dataclass(frozen=True)
class PlanActualVariance:
    metric: str
    planned: float | None
    actual: float | None
    variance: float | None
    status: str


@dataclass(frozen=True)
class PlanActualComparison:
    execution_event_id: str
    decision_trace_id: str
    variances: tuple[PlanActualVariance, ...]


def compare_plan_actual(trace: DecisionTrace, event: ExecutionEvent) -> PlanActualComparison:
    """Compare explicitly supplied planned/actual metrics; missing values are never inferred."""
    if event.decision_trace_id != trace.trace_id:
        raise ValueError("execution event does not belong to decision trace")
    planned = trace.planning_result.decision_payload.get("planned_metrics", {})
    actual = event.payload.get("actual_metrics", {})
    metrics = sorted(set(planned) | set(actual))
    variances: list[PlanActualVariance] = []
    for metric in metrics:
        p = planned.get(metric)
        a = actual.get(metric)
        if isinstance(p, (int, float)) and isinstance(a, (int, float)):
            variance = float(a) - float(p)
            status = "on_target" if variance == 0 else ("above_plan" if variance > 0 else "below_plan")
        else:
            variance = None
            status = "insufficient_data"
        variances.append(PlanActualVariance(metric, float(p) if isinstance(p, (int, float)) else None, float(a) if isinstance(a, (int, float)) else None, variance, status))
    return PlanActualComparison(event.event_id, trace.trace_id, tuple(variances))


def plan_actual_to_mapping(result: PlanActualComparison) -> dict[str, Any]:
    return {
        "execution_event_id": result.execution_event_id,
        "decision_trace_id": result.decision_trace_id,
        "variances": [
            {"metric": v.metric, "planned": v.planned, "actual": v.actual, "variance": v.variance, "status": v.status}
            for v in result.variances
        ],
    }
