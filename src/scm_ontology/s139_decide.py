from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DecisionStatus(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVOKED = "revoked"
    SUPERSEDED = "superseded"
    EXECUTION_PENDING = "execution_pending"
    EXECUTED = "executed"


class DecisionDisposition(str, Enum):
    SELECT = "select"
    AUTHORIZE = "authorize"
    REJECT = "reject"
    DEFER = "defer"
    NO_ACTION = "no_action"


@dataclass(frozen=True)
class Decision:
    ref: str
    subject_ref: str
    decision_maker_ref: str
    disposition: DecisionDisposition
    status: DecisionStatus = DecisionStatus.PROPOSED
    selected_alternative_refs: tuple[str, ...] = ()
    considered_alternative_refs: tuple[str, ...] = ()
    objective_refs: tuple[str, ...] = ()
    constraint_refs: tuple[str, ...] = ()
    policy_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    reasoning_refs: tuple[str, ...] = ()
    recommendation_refs: tuple[str, ...] = ()
    plan_refs: tuple[str, ...] = ()
    scenario_ref: Optional[str] = None
    decided_at: Optional[str] = None
    predecessor_ref: Optional[str] = None
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref or not self.decision_maker_ref:
            raise ValueError("ref, subject_ref, and decision_maker_ref are required")

    @property
    def is_scenario_decision(self) -> bool:
        return self.scenario_ref is not None

    @property
    def is_recommendation(self) -> bool:
        return False

    @property
    def is_action(self) -> bool:
        return False

    @property
    def is_outcome(self) -> bool:
        return False


def make_decision(
    *,
    ref: str,
    subject_ref: str,
    decision_maker_ref: str,
    disposition: DecisionDisposition,
    status: DecisionStatus = DecisionStatus.PROPOSED,
    selected_alternative_refs: tuple[str, ...] = (),
    considered_alternative_refs: tuple[str, ...] = (),
    objective_refs: tuple[str, ...] = (),
    constraint_refs: tuple[str, ...] = (),
    policy_refs: tuple[str, ...] = (),
    evidence_refs: tuple[str, ...] = (),
    reasoning_refs: tuple[str, ...] = (),
    recommendation_refs: tuple[str, ...] = (),
    plan_refs: tuple[str, ...] = (),
    scenario_ref: Optional[str] = None,
    decided_at: Optional[str] = None,
    predecessor_ref: Optional[str] = None,
    provenance_refs: tuple[str, ...] = (),
) -> Decision:
    return Decision(
        ref=ref,
        subject_ref=subject_ref,
        decision_maker_ref=decision_maker_ref,
        disposition=disposition,
        status=status,
        selected_alternative_refs=selected_alternative_refs,
        considered_alternative_refs=considered_alternative_refs,
        objective_refs=objective_refs,
        constraint_refs=constraint_refs,
        policy_refs=policy_refs,
        evidence_refs=evidence_refs,
        reasoning_refs=reasoning_refs,
        recommendation_refs=recommendation_refs,
        plan_refs=plan_refs,
        scenario_ref=scenario_ref,
        decided_at=decided_at,
        predecessor_ref=predecessor_ref,
        provenance_refs=provenance_refs,
    )
