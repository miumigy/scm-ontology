from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class StateEpistemicStatus(str, Enum):
    OBSERVED = "observed"
    MEASURED = "measured"
    ESTIMATED = "estimated"
    PREDICTED = "predicted"
    INFERRED = "inferred"
    UNKNOWN = "unknown"
    ACTUAL = "actual"


@dataclass(frozen=True)
class State:
    ref: str
    subject_ref: str
    state_type: str
    value: object
    effective_from: Optional[str] = None
    effective_to: Optional[str] = None
    transaction_time: Optional[str] = None
    scenario_ref: Optional[str] = None
    provenance_refs: tuple[str, ...] = ()
    epistemic_status: StateEpistemicStatus = StateEpistemicStatus.UNKNOWN

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref or not self.state_type:
            raise ValueError("ref, subject_ref, and state_type are required")

    @property
    def is_scenario_state(self) -> bool:
        return self.scenario_ref is not None


@dataclass(frozen=True)
class StateTransition:
    ref: str
    prior_state_ref: Optional[str]
    resulting_state_ref: str
    triggering_event_ref: Optional[str] = None
    actor_ref: Optional[str] = None
    effective_at: Optional[str] = None
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ref or not self.resulting_state_ref:
            raise ValueError("ref and resulting_state_ref are required")


def reconstruct_state(
    *,
    ref: str,
    subject_ref: str,
    state_type: str,
    value: object,
    effective_from: Optional[str] = None,
    effective_to: Optional[str] = None,
    transaction_time: Optional[str] = None,
    scenario_ref: Optional[str] = None,
    provenance_refs: tuple[str, ...] = (),
    epistemic_status: StateEpistemicStatus = StateEpistemicStatus.UNKNOWN,
) -> State:
    """Construct a canonical state without mutating historical events."""
    return State(
        ref=ref,
        subject_ref=subject_ref,
        state_type=state_type,
        value=value,
        effective_from=effective_from,
        effective_to=effective_to,
        transaction_time=transaction_time,
        scenario_ref=scenario_ref,
        provenance_refs=provenance_refs,
        epistemic_status=epistemic_status,
    )
