"""Canonical lineage from decision to execution and observed outcome."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .semantic_runtime import ExecutionRequest

@dataclass(frozen=True)
class ExecutionEvent:
    event_id: str
    request_id: str
    status: str
    observed_at: str
    details: Any = None

@dataclass(frozen=True)
class OutcomeObservation:
    outcome_id: str
    event_id: str
    observed_at: str
    result: Any

@dataclass(frozen=True)
class ExecutionLineage:
    request: ExecutionRequest
    event: ExecutionEvent
    outcome: OutcomeObservation | None = None

def record_execution(request: ExecutionRequest, *, event_id: str, status: str, observed_at: str, details: Any = None) -> ExecutionLineage:
    return ExecutionLineage(request, ExecutionEvent(event_id, request.request_id, status, observed_at, details))

def record_outcome(lineage: ExecutionLineage, *, outcome_id: str, observed_at: str, result: Any) -> ExecutionLineage:
    if lineage.event.status != "completed":
        raise ValueError("outcome requires a completed execution event")
    outcome = OutcomeObservation(outcome_id, lineage.event.event_id, observed_at, result)
    return ExecutionLineage(lineage.request, lineage.event, outcome)
