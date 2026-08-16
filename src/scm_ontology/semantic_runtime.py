"""Canonical runtime pipeline from decision trace to execution request."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class DecisionTrace:
    decision_id: str
    decision: Any
    evidence: tuple[Any, ...] = ()

@dataclass(frozen=True)
class ReasoningProvenance:
    decision_id: str
    rationale: str
    evidence: tuple[Any, ...] = ()

@dataclass(frozen=True)
class ExecutionRequest:
    request_id: str
    decision_id: str
    action: Any
    provenance: ReasoningProvenance

@dataclass(frozen=True)
class RuntimePipeline:
    trace: DecisionTrace
    provenance: ReasoningProvenance
    request: ExecutionRequest

def build_runtime_pipeline(trace: DecisionTrace, *, rationale: str, request_id: str) -> RuntimePipeline:
    provenance = ReasoningProvenance(trace.decision_id, rationale, trace.evidence)
    request = ExecutionRequest(request_id, trace.decision_id, trace.decision, provenance)
    return RuntimePipeline(trace, provenance, request)
