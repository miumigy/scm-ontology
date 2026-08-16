"""Separate empirical learned knowledge from canonical SCM facts."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Iterable

from .learning_evidence import LearningEvidence


@dataclass(frozen=True)
class LearnedKnowledge:
    knowledge_id: str
    metric: str
    statement: str
    confidence: float
    evidence_count: int
    source_event_ids: tuple[str, ...]
    source_layer: str = "empirical"


def promote_learning_evidence(evidence: LearningEvidence, *, confidence: float = 1.0) -> LearnedKnowledge:
    """Create empirical knowledge without modifying canonical graph facts."""
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be between 0 and 1")
    statement = f"Observed {evidence.metric} variance mean is {evidence.mean_variance:g} across {evidence.sample_count} execution events"
    canonical = {"metric": evidence.metric, "statement": statement, "confidence": confidence, "evidence_count": evidence.sample_count, "source_event_ids": list(evidence.source_event_ids), "source_layer": "empirical"}
    knowledge_id = sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return LearnedKnowledge(knowledge_id, evidence.metric, statement, confidence, evidence.sample_count, evidence.source_event_ids)


def learned_knowledge_to_mapping(items: Iterable[LearnedKnowledge]) -> dict[str, Any]:
    return {"learned_knowledge": [{"knowledge_id": x.knowledge_id, "metric": x.metric, "statement": x.statement, "confidence": x.confidence, "evidence_count": x.evidence_count, "source_event_ids": list(x.source_event_ids), "source_layer": x.source_layer} for x in items]}
