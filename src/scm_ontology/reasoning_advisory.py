"""Safe boundary for injecting learned knowledge into reasoning as advisory signals."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .learned_knowledge import LearnedKnowledge


@dataclass(frozen=True)
class ReasoningAdvisory:
    advisory_id: str
    knowledge_id: str
    metric: str
    statement: str
    confidence: float
    mode: str = "advisory"


def build_reasoning_advisories(items: Iterable[LearnedKnowledge], *, min_confidence: float = 0.0) -> tuple[ReasoningAdvisory, ...]:
    """Expose learned knowledge to reasoning without promoting it to canonical fact."""
    if not 0.0 <= min_confidence <= 1.0:
        raise ValueError("min_confidence must be between 0 and 1")
    result: list[ReasoningAdvisory] = []
    for item in items:
        if item.source_layer != "empirical":
            raise ValueError("only empirical learned knowledge may be used as advisory input")
        if item.confidence >= min_confidence:
            result.append(ReasoningAdvisory(item.knowledge_id, item.knowledge_id, item.metric, item.statement, item.confidence))
    return tuple(result)


def reasoning_advisories_to_mapping(items: Iterable[ReasoningAdvisory]) -> dict[str, Any]:
    return {"advisories": [{"advisory_id": x.advisory_id, "knowledge_id": x.knowledge_id, "metric": x.metric, "statement": x.statement, "confidence": x.confidence, "mode": x.mode} for x in items]}
