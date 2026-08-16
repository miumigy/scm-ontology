"""Canonical execution outcome, validation, and feedback for the semantic runtime."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .semantic_runtime import ExecutionRequest

@dataclass(frozen=True)
class ExecutionEvent:
    event_id: str
    request_id: str
    outcome: Any

@dataclass(frozen=True)
class ValidationResult:
    event_id: str
    valid: bool
    findings: tuple[str, ...] = ()

@dataclass(frozen=True)
class RuntimeFeedback:
    event: ExecutionEvent
    validation: ValidationResult


def record_execution_feedback(request: ExecutionRequest, *, event_id: str, outcome: Any, valid: bool, findings: tuple[str, ...] = ()) -> RuntimeFeedback:
    event = ExecutionEvent(event_id, request.request_id, outcome)
    validation = ValidationResult(event_id, valid, findings)
    return RuntimeFeedback(event, validation)
