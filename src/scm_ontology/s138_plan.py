from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PlanStatus(str, Enum):
    DRAFT = "draft"
    PROPOSED = "proposed"
    APPROVED = "approved"
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


@dataclass(frozen=True)
class Plan:
    ref: str
    subject_ref: str
    plan_type: str
    status: PlanStatus = PlanStatus.DRAFT
    objective_refs: tuple[str, ...] = ()
    constraint_refs: tuple[str, ...] = ()
    policy_refs: tuple[str, ...] = ()
    alternative_ref: Optional[str] = None
    scenario_ref: Optional[str] = None
    decision_ref: Optional[str] = None
    predecessor_ref: Optional[str] = None
    planned_start: Optional[str] = None
    planned_end: Optional[str] = None
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref or not self.plan_type:
            raise ValueError("ref, subject_ref, and plan_type are required")

    @property
    def is_scenario_plan(self) -> bool:
        return self.scenario_ref is not None

    @property
    def is_actual(self) -> bool:
        return False

    @property
    def is_schedule(self) -> bool:
        return False

    @property
    def is_commitment(self) -> bool:
        return False


def create_plan(
    *,
    ref: str,
    subject_ref: str,
    plan_type: str,
    status: PlanStatus = PlanStatus.DRAFT,
    objective_refs: tuple[str, ...] = (),
    constraint_refs: tuple[str, ...] = (),
    policy_refs: tuple[str, ...] = (),
    alternative_ref: Optional[str] = None,
    scenario_ref: Optional[str] = None,
    decision_ref: Optional[str] = None,
    predecessor_ref: Optional[str] = None,
    planned_start: Optional[str] = None,
    planned_end: Optional[str] = None,
    provenance_refs: tuple[str, ...] = (),
) -> Plan:
    return Plan(
        ref=ref,
        subject_ref=subject_ref,
        plan_type=plan_type,
        status=status,
        objective_refs=objective_refs,
        constraint_refs=constraint_refs,
        policy_refs=policy_refs,
        alternative_ref=alternative_ref,
        scenario_ref=scenario_ref,
        decision_ref=decision_ref,
        predecessor_ref=predecessor_ref,
        planned_start=planned_start,
        planned_end=planned_end,
        provenance_refs=provenance_refs,
    )
