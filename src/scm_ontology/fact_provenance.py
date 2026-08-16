"""Canonical identity and provenance lineage for SCM facts."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class FactProvenance:
    source: str
    source_record: str
    observed_at: str | None = None
    valid_from: str | None = None
    valid_to: str | None = None
    confidence: float | None = None

    def __post_init__(self) -> None:
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")

@dataclass(frozen=True)
class ProvenancedFact:
    fact_id: str
    predicate: str
    subject_id: str
    value: Any
    provenance: FactProvenance

def bind_provenance(fact_id: str, predicate: str, subject_id: str, value: Any, provenance: FactProvenance) -> ProvenancedFact:
    return ProvenancedFact(fact_id, predicate, subject_id, value, provenance)
