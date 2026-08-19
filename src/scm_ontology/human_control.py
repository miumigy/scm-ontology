"""P10-E — Human-in-the-loop Control.

Explicit human review, override, escalation, and delegation paths for
agent-initiated actions. P10-E composes the P10-D autonomy verdict with the
existing S356 authorization governance to keep a human in the loop when
autonomy is not full.

```text
AutonomyVerdict (P10-D)
   ├─ fully_autonomous -> proceed autonomously
   ├─ approved         -> require explicit human approval (delegation path)
   ├─ human_review     -> escalate for human review/override (override path)
   └─ blocked          -> no authorization path; reject
```

P10-E introduces no new canonical semantics and performs no side effect. It
records the human-control result (approval / override / escalation /
delegation) as an immutable, replayable `HumanControlRecord`.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any

from .agent_tool import AgentProposal
from .authorization_governance import ApprovalRecord, DecisionOverride
from .policy_autonomy import AutonomyLevel, AutonomyVerdict


class HumanControlError(ValueError):
    """Raised when a human-in-the-loop control path is violated."""


class ControlPath(str, Enum):
    """Explicit human control paths."""

    AUTONOMOUS = "autonomous"
    APPROVAL = "approval"
    OVERRIDE = "override"
    ESCALATION = "escalation"
    DELEGATION = "delegation"
    REJECTED = "rejected"


@dataclass(frozen=True)
class HumanControlRecord:
    """Immutable record of one human-in-the-loop control decision."""

    record_id: str
    proposal_id: str
    path: ControlPath
    ruled_by: str
    at: str
    reason: str = ""
    approval: ApprovalRecord | None = None
    override: DecisionOverride | None = None

    def __post_init__(self) -> None:
        if not self.proposal_id.strip():
            raise HumanControlError("proposal_id must be non-empty")
        if not isinstance(self.path, ControlPath):
            raise HumanControlError("path must be a ControlPath")
        if not self.ruled_by.strip():
            raise HumanControlError("ruled_by must be non-empty")
        if not self.at.strip():
            raise HumanControlError("at must be non-empty")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P10E.1",
            "record_id": self.record_id,
            "proposal_id": self.proposal_id,
            "path": self.path.value,
            "ruled_by": self.ruled_by,
            "at": self.at,
            "reason": self.reason,
            "approval": {
                "approval_id": self.approval.approval_id,
                "approver_id": self.approval.approver_id,
            }
            if self.approval is not None else None,
            "override": {
                "override_id": self.override.override_id,
                "actor_id": self.override.actor_id,
            }
            if self.override is not None else None,
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


@dataclass(frozen=True)
class HumanReviewDecision:
    """Explicit human decision: either approve, override, escalate, or reject."""

    decision: str  # approve | override | escalate | reject
    ruled_by: str
    at: str
    reason: str = ""

    def __post_init__(self) -> None:
        allowed = {"approve", "override", "escalate", "reject"}
        if self.decision not in allowed:
            raise HumanControlError(
                f"decision must be one of {sorted(allowed)}"
            )
        if not self.ruled_by.strip() or not self.at.strip():
            raise HumanControlError("ruled_by and at must be non-empty")


def route_human_control(
    proposal: AgentProposal,
    *,
    verdict: AutonomyVerdict,
    review_decision: HumanReviewDecision | None = None,
    approver_id: str = "",
    reviewer_id: str = "",
    senior_id: str = "",
    at: str = "",
) -> HumanControlRecord:
    """Route an agent proposal through the explicit human-control paths.

    Fails closed: a high-risk or blocked verdict never gets approved without an
    explicit human path. Every outcome is recorded as a replayable
    ``HumanControlRecord``.

    - ``fully_autonomous`` -> record ``autonomous`` path (no side effect).
    - ``approved`` -> requires an explicit ``approve`` review decision and an
      approver identity -> ``approval`` path producing an ``ApprovalRecord``.
    - ``human_review`` -> requires an explicit review decision: ``override``
      (senior override) or ``escalate`` (escalation path).
    - ``blocked`` -> returns ``rejected`` unless a senior override is provided.
    """
    if not isinstance(proposal, AgentProposal):
        raise HumanControlError("proposal must be an AgentProposal")
    if not isinstance(verdict, AutonomyVerdict):
        raise HumanControlError("verdict must be an AutonomyVerdict")
    if not at.strip():
        raise HumanControlError("at must be non-empty")

    proposal_id = proposal.proposal_id

    if verdict.autonomy is AutonomyLevel.FULLY_AUTONOMOUS:
        return _record(proposal_id, ControlPath.AUTONOMOUS, "os-governance", at, "autonomy granted by policy")

    if verdict.autonomy is AutonomyLevel.APPROVED:
        if review_decision is None or review_decision.decision != "approve":
            return _rejected_record(proposal_id, "delegation/approval", at, "approval path requires explicit human approval")
        if not reviewer_id.strip():
            raise HumanControlError("approval path requires reviewer_id")
        approval = ApprovalRecord(
            approval_id=f"apr-{proposal_id[:8]}",
            context_id=proposal.context_id,
            command_type=proposal.action,
            approver_id=reviewer_id,
            approved_at=at,
            reason=review_decision.reason,
        )
        return _record(proposal_id, ControlPath.APPROVAL, approval.approver_id, at, "human approval granted", approval=approval)

    if verdict.autonomy is AutonomyLevel.HUMAN_REVIEW:
        if review_decision is None:
            return _record(proposal_id, ControlPath.ESCALATION, reviewer_id or "gov", at, "escalated for human review")
        if review_decision.decision == "override":
            if not senior_id.strip():
                raise HumanControlError("override path requires senior_id")
            override = DecisionOverride(
                override_id=f"ovr-{proposal_id[:8]}",
                context_id=proposal.context_id,
                actor_id=proposal.agent_id,
                authority="senior",
                overridden_at=at,
                reason=review_decision.reason,
            )
            return _record(
                proposal_id, ControlPath.OVERRIDE, override.actor_id, at,
                "senior override granted", override=override,
            )
        if review_decision.decision == "escalate":
            return _record(proposal_id, ControlPath.ESCALATION, reviewer_id or "gov", at, "escalated to senior")
        return _rejected_record(proposal_id, "human-review", at, "human review rejected proposal")

    # blocked
    if review_decision is not None and review_decision.decision == "override" and senior_id.strip():
        override = DecisionOverride(
            override_id=f"ovr-{proposal_id[:8]}",
            context_id=proposal.context_id,
            actor_id=proposal.agent_id,
            authority="senior",
            overridden_at=at,
            reason=review_decision.reason,
        )
        return _record(proposal_id, ControlPath.OVERRIDE, "senior", at, "senior override over blocked verdict", override=override)
    return _rejected_record(proposal_id, "no-authorized-path", at, "no authorized human path for blocked verdict")


def _record(
    proposal_id: str,
    path: ControlPath,
    ruled_by: str,
    at: str,
    reason: str,
    *,
    approval: ApprovalRecord | None = None,
    override: DecisionOverride | None = None,
) -> HumanControlRecord:
    record = HumanControlRecord(
        record_id="",
        proposal_id=proposal_id,
        path=path,
        ruled_by=ruled_by,
        at=at,
        reason=reason,
        approval=approval,
        override=override,
    )
    object.__setattr__(record, "record_id", _record_id(record))
    return record


def _rejected_record(proposal_id: str, ruled_by: str, at: str, reason: str) -> HumanControlRecord:
    return _record(proposal_id, ControlPath.REJECTED, ruled_by, at, reason)


def _record_id(record: HumanControlRecord) -> str:
    payload = json.dumps(
        {
            "proposal_id": record.proposal_id,
            "path": record.path.value,
            "ruled_by": record.ruled_by,
            "at": record.at,
            "reason": record.reason,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256(payload.encode()).hexdigest()
