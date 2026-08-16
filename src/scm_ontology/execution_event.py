"""Execution outcome and event trace contract."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Any

from .execution_boundary import ExecutionRequest


_ALLOWED_STATUSES = {"succeeded", "failed", "partial", "cancelled"}


@dataclass(frozen=True)
class ExecutionEvent:
    event_id: str
    execution_request_id: str
    plan_id: str
    decision_trace_id: str
    status: str
    occurred_at: str
    payload: dict[str, Any]


def record_execution_event(request: ExecutionRequest, *, status: str, occurred_at: str, payload: dict[str, Any] | None = None) -> ExecutionEvent:
    """Record an externally observed execution outcome; never execute the request."""
    if status not in _ALLOWED_STATUSES:
        raise ValueError(f"unsupported execution status: {status}")
    datetime.fromisoformat(occurred_at.replace("Z", "+00:00"))
    normalized_payload = dict(payload or {})
    canonical = {
        "execution_request_id": request.request_id,
        "plan_id": request.plan_id,
        "decision_trace_id": request.decision_trace_id,
        "status": status,
        "occurred_at": occurred_at,
        "payload": normalized_payload,
    }
    event_id = sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return ExecutionEvent(event_id, request.request_id, request.plan_id, request.decision_trace_id, status, occurred_at, normalized_payload)


def execution_event_to_mapping(event: ExecutionEvent) -> dict[str, Any]:
    return {
        "event_id": event.event_id,
        "execution_request_id": event.execution_request_id,
        "plan_id": event.plan_id,
        "decision_trace_id": event.decision_trace_id,
        "status": event.status,
        "occurred_at": event.occurred_at,
        "payload": dict(event.payload),
    }
