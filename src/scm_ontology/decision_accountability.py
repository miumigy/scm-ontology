"""Canonical accountability query from current state back to decision evidence."""
from __future__ import annotations
from dataclasses import dataclass
from .snapshot_causal_query import trace_snapshot_causal_chain
from .snapshot_lineage import SnapshotTransition
from .semantic_runtime import DecisionTrace

@dataclass(frozen=True)
class DecisionAccountability:
    snapshot_id: str
    transitions: tuple[SnapshotTransition, ...]
    decision_id: str
    snapshot_fingerprint: str | None

class DecisionAccountabilityNotFound(LookupError):
    pass

def trace_decision_accountability(transitions: tuple[SnapshotTransition, ...], decisions: tuple[DecisionTrace, ...], *, snapshot_id: str) -> DecisionAccountability:
    chain = trace_snapshot_causal_chain(transitions, snapshot_id=snapshot_id)
    fingerprints = {t.from_fingerprint for t in chain}
    for decision in decisions:
        if decision.snapshot_fingerprint is not None and decision.snapshot_fingerprint in fingerprints:
            return DecisionAccountability(snapshot_id, chain, decision.decision_id, decision.snapshot_fingerprint)
    raise DecisionAccountabilityNotFound(snapshot_id)
