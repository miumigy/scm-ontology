"""Rebuild the next decision-time SCM snapshot from prior state and feedback."""
from __future__ import annotations
from .feedback_loop import FeedbackFact
from .temporal_snapshot import SCMSnapshot, build_snapshot

def rebuild_snapshot(snapshot_id: str, prior_facts, feedback: tuple[FeedbackFact, ...], *, at: str) -> SCMSnapshot:
    """Carry prior canonical facts forward and append observed feedback facts."""
    facts = tuple(prior_facts) + tuple(item.fact for item in feedback)
    return build_snapshot(snapshot_id, facts, at=at)
