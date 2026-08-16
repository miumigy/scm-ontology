"""Single-query accountability chain from current state to source provenance."""
from __future__ import annotations
from dataclasses import dataclass
from .decision_accountability import DecisionAccountability, trace_decision_accountability
from .evidence_accountability import EvidenceAccountability, trace_evidence_accountability
from .provenance_accountability import ProvenanceAccountability, trace_provenance_accountability
from .semantic_runtime import DecisionTrace
from .snapshot_lineage import SnapshotTransition

@dataclass(frozen=True)
class EndToEndAccountability:
    decision: DecisionAccountability
    evidence: tuple[EvidenceAccountability, ...]
    provenance: tuple[ProvenanceAccountability, ...]

def trace_end_to_end_accountability(
    transitions: tuple[SnapshotTransition, ...],
    decisions: tuple[DecisionTrace, ...],
    *, snapshot_id: str,
    evidence_by_id: dict[str, object],
    facts_by_evidence_id,
) -> EndToEndAccountability:
    decision = trace_decision_accountability(transitions, decisions, snapshot_id=snapshot_id)
    source = next(item for item in decisions if item.decision_id == decision.decision_id)
    evidence = tuple(trace_evidence_accountability(eid, evidence_by_id=evidence_by_id) for eid in source.evidence)
    provenance = tuple(trace_provenance_accountability(eid, facts_by_evidence_id=facts_by_evidence_id) for eid in source.evidence)
    return EndToEndAccountability(decision, evidence, provenance)
