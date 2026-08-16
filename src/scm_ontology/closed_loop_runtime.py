"""Single canonical API for decision -> execution -> feedback -> revision."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .contract_runtime import ContractRuntime
from .decision_learning import LearningOutcome, learn_from_feedback
from .runtime_feedback import RuntimeFeedback, record_execution_feedback
from .semantic_runtime import DecisionTrace, RuntimePipeline

@dataclass(frozen=True)
class ClosedLoopResult:
    pipeline: RuntimePipeline
    feedback: RuntimeFeedback
    learning: LearningOutcome

class ClosedLoopRuntime:
    def __init__(self, runtime: ContractRuntime) -> None:
        self._runtime = runtime

    def run(self, trace: DecisionTrace, *, rationale: str, request_id: str, event_id: str, outcome: Any, valid: bool, findings: tuple[str, ...] = (), revision_id: str | None = None, revised_decision: Any = None, revision_reason: str = "") -> ClosedLoopResult:
        pipeline = self._runtime.build_pipeline(trace, rationale=rationale, request_id=request_id)
        feedback = record_execution_feedback(pipeline.request, event_id=event_id, outcome=outcome, valid=valid, findings=findings)
        learning = learn_from_feedback(trace, feedback, revision_id=revision_id, revised_decision=revised_decision, reason=revision_reason)
        return ClosedLoopResult(pipeline, feedback, learning)
