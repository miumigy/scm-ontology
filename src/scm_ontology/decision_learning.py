"""Canonical feedback-to-decision evaluation and revision primitives."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .runtime_feedback import RuntimeFeedback
from .semantic_runtime import DecisionTrace

@dataclass(frozen=True)
class DecisionEvaluation:
    decision_id: str
    successful: bool
    findings: tuple[str, ...] = ()

@dataclass(frozen=True)
class DecisionRevision:
    revision_id: str
    source_decision_id: str
    revised_decision: Any
    reason: str

@dataclass(frozen=True)
class LearningOutcome:
    evaluation: DecisionEvaluation
    revision: DecisionRevision | None


def evaluate_feedback(trace: DecisionTrace, feedback: RuntimeFeedback) -> DecisionEvaluation:
    if feedback.event.request_id != trace.decision_id and feedback.validation.event_id != feedback.event.event_id:
        raise ValueError("feedback lineage does not match execution event")
    return DecisionEvaluation(trace.decision_id, feedback.validation.valid, feedback.validation.findings)


def revise_decision(evaluation: DecisionEvaluation, *, revision_id: str, revised_decision: Any, reason: str) -> DecisionRevision:
    return DecisionRevision(revision_id, evaluation.decision_id, revised_decision, reason)


def learn_from_feedback(trace: DecisionTrace, feedback: RuntimeFeedback, *, revision_id: str | None = None, revised_decision: Any = None, reason: str = "") -> LearningOutcome:
    evaluation = evaluate_feedback(trace, feedback)
    revision = None
    if revision_id is not None:
        revision = revise_decision(evaluation, revision_id=revision_id, revised_decision=revised_decision, reason=reason)
    return LearningOutcome(evaluation, revision)
