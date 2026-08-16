"""Explicit boundary from an externally produced plan to execution systems."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

from .decision_trace import DecisionTrace


@dataclass(frozen=True)
class ExecutionRequest:
    request_id: str
    plan_id: str
    decision_trace_id: str
    execution_target: str
    action: str
    payload: dict[str, Any]


def build_execution_request(
    trace: DecisionTrace,
    *,
    execution_target: str,
    action: str,
    payload: dict[str, Any] | None = None,
) -> ExecutionRequest:
    """Create an execution request without executing or mutating operational state."""
    if not trace.planning_result.plan_id.strip():
        raise ValueError("plan_id must be non-empty")
    if not execution_target.strip() or not action.strip():
        raise ValueError("execution_target and action must be non-empty")
    normalized = {
        "plan_id": trace.planning_result.plan_id,
        "decision_trace_id": trace.trace_id,
        "execution_target": execution_target,
        "action": action,
        "payload": payload or {},
    }
    request_id = sha256(json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return ExecutionRequest(request_id, trace.planning_result.plan_id, trace.trace_id, execution_target, action, dict(payload or {}))


def execution_request_to_mapping(request: ExecutionRequest) -> dict[str, Any]:
    return {
        "request_id": request.request_id,
        "plan_id": request.plan_id,
        "decision_trace_id": request.decision_trace_id,
        "execution_target": request.execution_target,
        "action": request.action,
        "payload": dict(request.payload),
    }
