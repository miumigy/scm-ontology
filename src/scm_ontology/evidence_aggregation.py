from __future__ import annotations

from dataclasses import dataclass

from .evidence_provenance import EvidenceRef, EvidenceSet


class EvidenceAggregationError(ValueError):
    pass


@dataclass(frozen=True)
class AggregatedEvidence:
    evidence: EvidenceSet
    source_count: int


def aggregate_evidence(*sets: EvidenceSet) -> AggregatedEvidence:
    refs: list[EvidenceRef] = []
    seen: set[str] = set()
    for evidence in sets:
        for ref in evidence.refs:
            if ref.source_ref not in seen:
                seen.add(ref.source_ref)
                refs.append(ref)
    result = EvidenceSet(tuple(refs))
    return AggregatedEvidence(result, len(refs))
