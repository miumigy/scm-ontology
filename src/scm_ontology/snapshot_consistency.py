"""Consistency checks for decision-time SCM snapshots."""
from __future__ import annotations
from dataclasses import dataclass
from .temporal_snapshot import SCMSnapshot

@dataclass(frozen=True)
class FactConflict:
    subject_id: str
    predicate: str
    fact_ids: tuple[str, ...]

class SnapshotConsistencyError(ValueError):
    pass

def find_conflicts(snapshot: SCMSnapshot) -> tuple[FactConflict, ...]:
    groups: dict[tuple[str, str], list] = {}
    for fact in snapshot.facts:
        groups.setdefault((fact.subject_id, fact.predicate), []).append(fact)
    conflicts = []
    for (subject_id, predicate), facts in groups.items():
        if len({repr(fact.value) for fact in facts}) > 1:
            conflicts.append(FactConflict(subject_id, predicate, tuple(fact.fact_id for fact in facts)))
    return tuple(conflicts)

def require_consistent_snapshot(snapshot: SCMSnapshot) -> SCMSnapshot:
    conflicts = find_conflicts(snapshot)
    if conflicts:
        detail = "; ".join(f"{c.subject_id}.{c.predicate}: {', '.join(c.fact_ids)}" for c in conflicts)
        raise SnapshotConsistencyError(f"conflicting facts in SCM snapshot: {detail}")
    return snapshot
