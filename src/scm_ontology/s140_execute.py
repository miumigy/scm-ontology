from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ExecutionStatus(str, Enum):
    PENDING = "pending"
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    PARTIALLY_COMPLETED = "partially_completed"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    INTERRUPTED = "interrupted"


@dataclass(frozen=True)
class Action:
    ref: str
    subject_ref: str
    action_type: str
    decision_ref: Optional[str] = None
    plan_ref: Optional[str] = None
    intended_quantity: Optional[float] = None
    intended_start: Optional[str] = None
    intended_end: Optional[str] = None
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref or not self.action_type:
            raise ValueError("ref, subject_ref, and action_type are required")

    @property
    def is_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class Execution:
    ref: str
    action_ref: str
    executor_ref: Optional[str] = None
    status: ExecutionStatus = ExecutionStatus.PENDING
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    actual_quantity: Optional[float] = None
    location_ref: Optional[str] = None
    resource_ref: Optional[str] = None
    event_refs: tuple[str, ...] = ()
    state_change_refs: tuple[str, ...] = ()
    exception_refs: tuple[str, ...] = ()
    outcome_refs: tuple[str, ...] = ()
    scenario_ref: Optional[str] = None
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ref or not self.action_ref:
            raise ValueError("ref and action_ref are required")

    @property
    def is_actual_outcome(self) -> bool:
        return False

    @property
    def is_event(self) -> bool:
        return False

    @property
    def is_scenario_execution(self) -> bool:
        return self.scenario_ref is not None


def execute_action(
    *,
    ref: str,
    action_ref: str,
    executor_ref: Optional[str] = None,
    status: ExecutionStatus = ExecutionStatus.PENDING,
    started_at: Optional[str] = None,
    ended_at: Optional[str] = None,
    actual_quantity: Optional[float] = None,
    location_ref: Optional[str] = None,
    resource_ref: Optional[str] = None,
    event_refs: tuple[str, ...] = (),
    state_change_refs: tuple[str, ...] = (),
    exception_refs: tuple[str, ...] = (),
    outcome_refs: tuple[str, ...] = (),
    scenario_ref: Optional[str] = None,
    provenance_refs: tuple[str, ...] = (),
) -> Execution:
    return Execution(
        ref=ref,
        action_ref=action_ref,
        executor_ref=executor_ref,
        status=status,
        started_at=started_at,
        ended_at=ended_at,
        actual_quantity=actual_quantity,
        location_ref=location_ref,
        resource_ref=resource_ref,
        event_refs=event_refs,
        state_change_refs=state_change_refs,
        exception_refs=exception_refs,
        outcome_refs=outcome_refs,
        scenario_ref=scenario_ref,
        provenance_refs=provenance_refs,
    )
