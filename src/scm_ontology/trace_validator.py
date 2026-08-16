"""End-to-end integrity checks for the SCM decision-to-execution trace."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable
from .decision_trace import DecisionTrace
from .execution_boundary import ExecutionRequest
from .execution_event import ExecutionEvent
from .learned_knowledge import LearnedKnowledge
from .learning_evidence import LearningEvidence
from .reasoning_advisory import ReasoningAdvisory
from .reasoning_provenance import ReasoningProvenance

@dataclass(frozen=True)
class TraceValidation:
    valid: bool
    errors: tuple[str, ...]

def validate_end_to_end_trace(trace: DecisionTrace, execution_request: ExecutionRequest, execution_event: ExecutionEvent, provenance: ReasoningProvenance, advisories: Iterable[ReasoningAdvisory] = (), learned_knowledge: Iterable[LearnedKnowledge] = (), learning_evidence: Iterable[LearningEvidence] = ()) -> TraceValidation:
    errors: list[str] = []
    advisory_list, knowledge_list, evidence_list = tuple(advisories), tuple(learned_knowledge), tuple(learning_evidence)
    if execution_request.plan_id != trace.planning_result.plan_id: errors.append("execution request plan_id does not match decision trace")
    if execution_request.decision_trace_id != trace.trace_id: errors.append("execution request decision_trace_id does not match decision trace")
    if execution_event.execution_request_id != execution_request.request_id: errors.append("execution event does not reference execution request")
    if execution_event.plan_id != trace.planning_result.plan_id: errors.append("execution event plan_id does not match decision trace")
    if execution_event.decision_trace_id != trace.trace_id: errors.append("execution event decision_trace_id does not match decision trace")
    if provenance.reasoning_result_id != trace.reasoning_result_id: errors.append("reasoning provenance does not reference trace reasoning result")
    advisory_ids = {x.advisory_id for x in advisory_list}
    if set(provenance.advisory_ids) != advisory_ids: errors.append("reasoning provenance advisory ids do not match supplied advisories")
    knowledge_ids = {x.knowledge_id for x in knowledge_list}
    for x in advisory_list:
        if x.knowledge_id not in knowledge_ids: errors.append(f"advisory {x.advisory_id} has no supplied learned knowledge")
    evidence_event_ids = {event_id for x in evidence_list for event_id in x.source_event_ids}
    for x in knowledge_list:
        if not set(x.source_event_ids).issubset(evidence_event_ids | {execution_event.event_id}): errors.append(f"learned knowledge {x.knowledge_id} has unresolved source events")
    return TraceValidation(not errors, tuple(errors))

def trace_validation_to_mapping(result: TraceValidation) -> dict[str, Any]:
    return {"valid": result.valid, "errors": list(result.errors)}
