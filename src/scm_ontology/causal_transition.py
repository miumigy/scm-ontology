"""Bridge causal event propagation into the simulation transition chain."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .causal import CausalRule, derive_event
from .simulation import Event, SimulationError, SimulationKernel, State, Transition


class CausalTransitionError(SimulationError):
    """Raised when causal propagation cannot be followed by a state transition."""


@dataclass(frozen=True)
class CausalTransitionResult:
    """Auditable result of one causal derivation followed by state transition."""

    source_event: Event
    derived_event: Event
    transition: Transition
    state: State


def derive_and_transition(
    state: State,
    source_event: Event,
    rule: CausalRule,
    event_id: str,
    kernel: SimulationKernel,
) -> CausalTransitionResult:
    """Derive one event causally, then apply the canonical state transition."""
    derived_event = derive_event(source_event, rule, event_id=event_id)
    try:
        next_state, transition = kernel.apply_event(state, derived_event)
    except SimulationError as exc:
        raise CausalTransitionError(
            f"derived event {derived_event.event_id} cannot transition state: {exc}"
        ) from exc
    return CausalTransitionResult(source_event, derived_event, transition, next_state)
