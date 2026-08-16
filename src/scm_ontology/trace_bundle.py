"""Immutable, serializable snapshot of the complete SCM decision lifecycle trace."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .decision_trace import DecisionTrace, decision_trace_to_mapping
from .execution_boundary import ExecutionRequest, execution_request_to_mapping
from .execution_event import ExecutionEvent, execution_event_to_mapping
from .reasoning_provenance import ReasoningProvenance, reasoning_provenance_to_mapping
from .trace_validator import TraceValidation, trace_validation_to_mapping


@dataclass(frozen=True)
class TraceBundle:
    decision_trace: DecisionTrace
    execution_request: ExecutionRequest
    execution_event: ExecutionEvent
    reasoning_provenance: ReasoningProvenance
    validation: TraceValidation


def build_trace_bundle(trace: DecisionTrace, execution_request: ExecutionRequest, execution_event: ExecutionEvent, provenance: ReasoningProvenance, validation: TraceValidation) -> TraceBundle:
    """Package the lifecycle references only after an explicit successful validation."""
    if not validation.valid:
        raise ValueError("cannot build trace bundle from invalid trace")
    return TraceBundle(trace, execution_request, execution_event, provenance, validation)


def trace_bundle_to_mapping(bundle: TraceBundle) -> dict[str, Any]:
    return {"decision_trace": decision_trace_to_mapping(bundle.decision_trace), "execution_request": execution_request_to_mapping(bundle.execution_request), "execution_event": execution_event_to_mapping(bundle.execution_event), "reasoning_provenance": reasoning_provenance_to_mapping(bundle.reasoning_provenance), "validation": trace_validation_to_mapping(bundle.validation)}
