"""Canonical feedback from execution outcomes into SCM facts."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .execution_lineage import ExecutionLineage
from .fact_provenance import FactProvenance, ProvenancedFact

@dataclass(frozen=True)
class FeedbackFact:
    fact: ProvenancedFact
    outcome_id: str

def outcome_to_fact(lineage: ExecutionLineage, *, fact_id: str, predicate: str, subject_id: str, value: Any, source: str = "execution", observed_at: str | None = None) -> FeedbackFact:
    if lineage.outcome is None:
        raise ValueError("feedback requires an observed outcome")
    observed = observed_at or lineage.outcome.observed_at
    provenance = FactProvenance(source, lineage.outcome.outcome_id, observed_at=observed, valid_from=observed)
    return FeedbackFact(ProvenancedFact(fact_id, predicate, subject_id, value, provenance), lineage.outcome.outcome_id)
