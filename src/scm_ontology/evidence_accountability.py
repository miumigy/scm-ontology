"""Canonical accountability query from a decision to its supporting evidence."""
from __future__ import annotations
from dataclasses import dataclass
from .semantic_runtime import DecisionTrace

@dataclass(frozen=True)
class EvidenceAccountability:
    decision_id: str
    evidence: tuple[object, ...]

class EvidenceAccountabilityNotFound(LookupError):
    pass

def trace_evidence_accountability(decision: DecisionTrace, *, evidence_by_id: dict[str, object]) -> EvidenceAccountability:
    missing = [item for item in decision.evidence if item not in evidence_by_id]
    if missing:
        raise EvidenceAccountabilityNotFound(", ".join(missing))
    return EvidenceAccountability(decision.decision_id, tuple(evidence_by_id[item] for item in decision.evidence))
