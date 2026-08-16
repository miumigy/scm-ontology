"""Decision-time SCM snapshots composed from temporally valid canonical facts."""
from __future__ import annotations
from dataclasses import dataclass
from .fact_provenance import ProvenancedFact
from .temporal_evidence import select_evidence_at
from .semantic_runtime import DecisionTrace

@dataclass(frozen=True)
class SCMSnapshot:
    snapshot_id: str
    at: str
    facts: tuple[ProvenancedFact, ...]

    def fact(self, fact_id: str) -> ProvenancedFact | None:
        return next((fact for fact in self.facts if fact.fact_id == fact_id), None)

def build_snapshot(snapshot_id: str, facts: tuple[ProvenancedFact, ...], *, at: str) -> SCMSnapshot:
    selected = tuple(binding.fact for binding in select_evidence_at(facts, at=at))
    return SCMSnapshot(snapshot_id, at, selected)

def trace_from_snapshot(decision_id: str, decision: object, snapshot: SCMSnapshot) -> DecisionTrace:
    return DecisionTrace(decision_id, decision, select_evidence_at(snapshot.facts, at=snapshot.at))
