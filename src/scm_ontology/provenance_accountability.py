"""Resolve evidence to its provenance-bearing canonical fact."""
from __future__ import annotations
from dataclasses import dataclass
from .fact_provenance import ProvenancedFact

@dataclass(frozen=True)
class ProvenanceAccountability:
    evidence_id: str
    fact: ProvenancedFact
    source_record: str
    observed_at: str | None
    valid_from: str | None
    valid_to: str | None

class ProvenanceAccountabilityNotFound(LookupError):
    pass

def trace_provenance_accountability(evidence_id: str, *, facts_by_evidence_id: dict[str, ProvenancedFact]) -> ProvenanceAccountability:
    fact = facts_by_evidence_id.get(evidence_id)
    if fact is None:
        raise ProvenanceAccountabilityNotFound(evidence_id)
    provenance = fact.provenance
    return ProvenanceAccountability(evidence_id, fact, provenance.source_record, provenance.observed_at, provenance.valid_from, provenance.valid_to)
