"""Explicit lineage between SCM snapshots and the execution that changed state."""
from __future__ import annotations
from dataclasses import dataclass
from .execution_lineage import ExecutionLineage
from .snapshot_identity import snapshot_fingerprint
from .temporal_snapshot import SCMSnapshot

@dataclass(frozen=True)
class SnapshotTransition:
    from_snapshot_id: str
    from_fingerprint: str
    execution_event_id: str
    outcome_id: str
    to_snapshot_id: str
    to_fingerprint: str
    observed_at: str

def link_snapshot_transition(previous: SCMSnapshot, execution: ExecutionLineage, next_snapshot: SCMSnapshot) -> SnapshotTransition:
    if execution.outcome is None:
        raise ValueError("snapshot transition requires an observed outcome")
    if execution.outcome.observed_at > next_snapshot.at:
        raise ValueError("next snapshot cannot precede the observed outcome")
    return SnapshotTransition(previous.snapshot_id, snapshot_fingerprint(previous), execution.event.event_id, execution.outcome.outcome_id, next_snapshot.snapshot_id, snapshot_fingerprint(next_snapshot), execution.outcome.observed_at)
