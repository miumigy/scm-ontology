"""Assemble governed observations into an immutable DecisionContext.

S340 adds no new semantic entity. It provides a small, deterministic boundary
between observation producers and the existing S333 DecisionContext contract.
"""
from __future__ import annotations

from typing import Iterable

from .decision_context import DecisionContext, DecisionObservation, build_decision_context


def assemble_decision_context(
    context_id: str,
    observations: Iterable[DecisionObservation],
) -> DecisionContext:
    """Assemble explicit observations into the existing S333 context.

    Ordering is delegated to the canonical DecisionContext contract. Duplicate
    question identifiers are rejected rather than silently overwritten.
    """
    return build_decision_context(context_id, tuple(observations))
