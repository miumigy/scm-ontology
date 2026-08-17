"""Assembly boundary from graph reasoning observations into ReasoningInput.

S367 completes the graph-to-reasoning handoff without introducing business
semantics. Graph projections remain observations; this module only assembles
them into the existing immutable DecisionContext and fail-closed
ReasoningInput contracts.
"""
from __future__ import annotations

from collections.abc import Iterable

from .decision_context import DecisionContext, build_decision_context
from .graph_reasoning_projection import GraphReasoningObservation
from .reasoning_input import ReasoningInput, build_reasoning_input


class ReasoningAssemblyError(ValueError):
    """Raised when graph observations cannot form a reasoning input."""


def assemble_reasoning_input(
    context_id: str,
    observations: Iterable[GraphReasoningObservation],
) -> ReasoningInput:
    """Assemble graph-derived observations into a ready, immutable reasoning input.

    The function deliberately performs no inference or semantic transformation:
    each graph observation is converted to one DecisionObservation and the
    existing DecisionContext/ReasoningInput contracts enforce uniqueness,
    evidence/provenance readiness, and deterministic ordering.
    """
    if not isinstance(context_id, str) or not context_id.strip():
        raise ReasoningAssemblyError("context_id must be non-empty")

    graph_observations = tuple(observations)
    if any(not isinstance(observation, GraphReasoningObservation) for observation in graph_observations):
        raise ReasoningAssemblyError("observations must contain only GraphReasoningObservation values")
    if not graph_observations:
        raise ReasoningAssemblyError("observations must not be empty")

    decision_observations = tuple(
        observation.to_decision_observation() for observation in graph_observations
    )
    try:
        context: DecisionContext = build_decision_context(
            context_id,
            decision_observations,
        )
        return build_reasoning_input(context)
    except ValueError as exc:
        raise ReasoningAssemblyError(str(exc)) from exc
