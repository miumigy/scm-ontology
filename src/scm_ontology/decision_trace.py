"""Traceability contract for plans returned by external planning engines."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

from .auditable_reasoning import AuditableReasoningResult
from .planning_boundary import PlanningRequest


@dataclass(frozen=True)
class PlanningResultReference:
    plan_id: str
    planning_request_id: str
    reasoning_result_id: str
    status: str
    objective: str
    decision_payload: dict[str, Any]


@dataclass(frozen=True)
class DecisionTrace:
    trace_id: str
    planning_request: PlanningRequest
    planning_result: PlanningResultReference
    reasoning_result_id: str


def record_planning_result(
    request: PlanningRequest,
    reasoning: AuditableReasoningResult,
    *,
    plan_id: str,
    status: str,
    decision_payload: dict[str, Any] | None = None,
) -> DecisionTrace:
    """Record provenance for an externally produced plan; never validate or mutate the plan."""
    if request.reasoning_result_id != reasoning.result_id:
        raise ValueError("planning request and reasoning result do not match")
    if not plan_id.strip() or not status.strip():
        raise ValueError("plan_id and status must be non-empty")
    result = PlanningResultReference(
        plan_id=plan_id,
        planning_request_id=request.request_id,
        reasoning_result_id=reasoning.result_id,
        status=status,
        objective=request.objective,
        decision_payload=dict(decision_payload or {}),
    )
    canonical = {
        "planning_request_id": request.request_id,
        "reasoning_result_id": reasoning.result_id,
        "plan_id": plan_id,
        "status": status,
        "objective": request.objective,
        "decision_payload": result.decision_payload,
    }
    trace_id = sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return DecisionTrace(trace_id, request, result, reasoning.result_id)


def decision_trace_to_mapping(trace: DecisionTrace) -> dict[str, Any]:
    return {
        "trace_id": trace.trace_id,
        "planning_request_id": trace.planning_request.request_id,
        "reasoning_result_id": trace.reasoning_result_id,
        "plan_id": trace.planning_result.plan_id,
        "status": trace.planning_result.status,
        "objective": trace.planning_result.objective,
        "decision_payload": dict(trace.planning_result.decision_payload),
    }
