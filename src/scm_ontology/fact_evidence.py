"""Canonical SCM fact to runtime evidence binding primitives."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .fact_provenance import FactProvenance, ProvenancedFact
from .semantic_runtime import DecisionTrace

@dataclass(frozen=True)
class CanonicalFact:
    fact_id: str
    predicate: str
    subject_id: str
    value: Any
    observed_at: str | None = None

@dataclass(frozen=True)
class EvidenceBinding:
    evidence_id: str
    fact_id: str
    fact: ProvenancedFact


def bind_fact_evidence(fact: ProvenancedFact, *, evidence_id: str) -> EvidenceBinding:
    return EvidenceBinding(evidence_id, fact.fact_id, fact)


def trace_with_fact_evidence(decision_id: str, decision: Any, evidence: tuple[EvidenceBinding, ...]) -> DecisionTrace:
    return DecisionTrace(decision_id, decision, evidence)


def provenanced_fact_from_canonical(fact: CanonicalFact, provenance: FactProvenance) -> ProvenancedFact:
    return ProvenancedFact(fact.fact_id, fact.predicate, fact.subject_id, fact.value, provenance)
