"""Canonical gate from temporal SCM state to reasoning evidence."""
from __future__ import annotations
from dataclasses import dataclass
from .snapshot_consistency import require_consistent_snapshot
from .temporal_snapshot import SCMSnapshot
from .temporal_evidence import select_evidence_at
from .snapshot_identity import snapshot_fingerprint
from .semantic_runtime import DecisionTrace

@dataclass(frozen=True)
class ReasoningContext:
    snapshot: SCMSnapshot
    trace: DecisionTrace

def build_reasoning_context(decision_id: str, decision: object, snapshot: SCMSnapshot) -> ReasoningContext:
    consistent = require_consistent_snapshot(snapshot)
    evidence = select_evidence_at(consistent.facts, at=consistent.at)
    return ReasoningContext(consistent, DecisionTrace(decision_id, decision, evidence, snapshot_fingerprint(consistent)))
