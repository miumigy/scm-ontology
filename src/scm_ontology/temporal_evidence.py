"""Build decision evidence from facts valid at the decision time."""
from __future__ import annotations
from .fact_evidence import EvidenceBinding
from .fact_temporal import select_valid_facts
from .fact_provenance import ProvenancedFact
from .semantic_runtime import DecisionTrace

def select_evidence_at(facts: tuple[ProvenancedFact, ...], *, at: str, evidence_id_prefix: str = "ev") -> tuple[EvidenceBinding, ...]:
    valid = select_valid_facts(facts, at=at)
    return tuple(EvidenceBinding(f"{evidence_id_prefix}-{index}", fact.fact_id, fact) for index, fact in enumerate(valid, 1))

def trace_with_temporal_evidence(decision_id: str, decision: object, facts: tuple[ProvenancedFact, ...], *, at: str) -> DecisionTrace:
    return DecisionTrace(decision_id, decision, select_evidence_at(facts, at=at))
