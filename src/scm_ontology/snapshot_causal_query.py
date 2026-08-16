"""Canonical queries over SCM snapshot state-transition lineage."""
from __future__ import annotations
from .snapshot_lineage import SnapshotTransition

class SnapshotCausalChainNotFound(LookupError):
    pass

def trace_snapshot_causal_chain(transitions: tuple[SnapshotTransition, ...], *, snapshot_id: str) -> tuple[SnapshotTransition, ...]:
    """Return transitions leading into snapshot_id, ordered newest-to-oldest."""
    by_to = {transition.to_snapshot_id: transition for transition in transitions}
    chain: list[SnapshotTransition] = []
    current = snapshot_id
    seen: set[str] = set()
    while current in by_to:
        if current in seen:
            raise ValueError("snapshot lineage contains a cycle")
        seen.add(current)
        transition = by_to[current]
        chain.append(transition)
        current = transition.from_snapshot_id
    if not chain:
        raise SnapshotCausalChainNotFound(snapshot_id)
    return tuple(chain)
