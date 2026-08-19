"""P10-D — Policy-aware Autonomy.

Autonomy is a *policy decision*, not an implicit property of an AI model.
P10-D determines the allowed autonomy level for an agent proposal from explicit
inputs: proposal confidence, assessed risk, monetary impact, the operation's
scope, and an approval-policy gate.

```text
AgentProposal
   ├─ confidence, risk, monetary_impact, scope
   └─ approval policy (allowed autonomy levels per scope)
               ↓
      AutonomyLevel (none / review / auto)
```

P10-D never authorizes or executes anything. It produces a deterministic,
content-addressed ``AutonomyVerdict`` that the governance layer consults.
Higher confidence, lower risk, lower monetary impact, and a narrower scope
permit a higher autonomy level; high risk, high impact, or wide scope narrow
autonomy toward human review.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any

from .agent_tool import AgentProposal


class AutonomyLevel(str, Enum):
    """Supported autonomy levels for agent-initiated actions."""

    FULLY_AUTONOMOUS = "fully_autonomous"
    APPROVED = "approved"
    HUMAN_REVIEW = "human_review"
    BLOCKED = "blocked"


class AutonomyPolicyError(ValueError):
    """Raised when an autonomy policy input is invalid."""


@dataclass(frozen=True)
class AutonomyPolicy:
    """Declarative policy: which scopes allow which autonomy levels."""

    policy_id: str
    # Map operation scope -> maximum autonomy level permitted.
    allowed_by_scope: dict[str, AutonomyLevel]
    max_monetary_impact: float = 1000.0
    max_confidence_required: float = 0.7
    max_risk_allowed: float = 0.3

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise AutonomyPolicyError("policy_id must be non-empty")
        if not self.allowed_by_scope:
            raise AutonomyPolicyError("allowed_by_scope must not be empty")
        if any(v not in AutonomyLevel for v in self.allowed_by_scope.values()):
            raise AutonomyPolicyError("allowed_by_scope values must be AutonomyLevel")
        if not 0.0 <= self.max_monetary_impact:
            raise AutonomyPolicyError("max_monetary_impact must be non-negative")
        if not 0.0 <= self.max_confidence_required <= 1.0:
            raise AutonomyPolicyError("max_confidence_required must be between 0 and 1")
        if not 0.0 <= self.max_risk_allowed <= 1.0:
            raise AutonomyPolicyError("max_risk_allowed must be between 0 and 1")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "allowed_by_scope": {
                scope: level.value for scope, level in self.allowed_by_scope.items()
            },
            "max_monetary_impact": self.max_monetary_impact,
            "max_confidence_required": self.max_confidence_required,
            "max_risk_allowed": self.max_risk_allowed,
        }


@dataclass(frozen=True)
class AutonomyInput:
    """Explicit factors contributing to an autonomy verdict."""

    confidence: float
    risk: float
    monetary_impact: float
    scope: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise AutonomyPolicyError("confidence must be between 0 and 1")
        if not 0.0 <= self.risk <= 1.0:
            raise AutonomyPolicyError("risk must be between 0 and 1")
        if not self.monetary_impact >= 0.0:
            raise AutonomyPolicyError("monetary_impact must be non-negative")
        if not isinstance(self.scope, str) or not self.scope.strip():
            raise AutonomyPolicyError("scope must be non-empty")


@dataclass(frozen=True)
class AutonomyVerdict:
    """Immutable, content-addressed autonomy decision for one agent proposal."""

    verdict_id: str
    proposal_id: str
    autonomy: AutonomyLevel
    reason: str
    policy_id: str

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P10D.1",
            "verdict_id": self.verdict_id,
            "proposal_id": self.proposal_id,
            "autonomy": self.autonomy.value,
            "reason": self.reason,
            "policy_id": self.policy_id,
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def evaluate_autonomy(
    proposal: AgentProposal,
    *,
    inputs: AutonomyInput,
    policy: AutonomyPolicy,
) -> AutonomyVerdict:
    """Determine the allowed autonomy level for a proposal under a policy.

    Fails closed: any factor outside the policy's permitted threshold narrows
    the autonomy level, and an unknown scope is denied the autonomous path.

    Autonomy levels, from most to least permissive:
      fully_autonomous > approved > human_review > blocked
    """
    if not isinstance(proposal, AgentProposal):
        raise AutonomyPolicyError("proposal must be an AgentProposal")
    if not isinstance(inputs, AutonomyInput):
        raise AutonomyPolicyError("inputs must be an AutonomyInput")
    if not isinstance(policy, AutonomyPolicy):
        raise AutonomyPolicyError("policy must be an AutonomyPolicy")

    if inputs.scope not in policy.allowed_by_scope:
        return AutonomyVerdict(
            verdict_id=_verdict_id(proposal, policy, AutonomyLevel.BLOCKED),
            proposal_id=proposal.proposal_id,
            autonomy=AutonomyLevel.BLOCKED,
            reason=f"scope {inputs.scope!r} is not permitted by policy {policy.policy_id}",
            policy_id=policy.policy_id,
        )

    permitted = policy.allowed_by_scope[inputs.scope]

    # Fail closed: any threshold violation narrows autonomy.
    if inputs.confidence < policy.max_confidence_required:
        return AutonomyVerdict(
            verdict_id=_verdict_id(proposal, policy, AutonomyLevel.BLOCKED),
            proposal_id=proposal.proposal_id,
            autonomy=AutonomyLevel.BLOCKED,
            reason=(
                f"confidence {inputs.confidence:.2f} below required "
                f"{policy.max_confidence_required}"
            ),
            policy_id=policy.policy_id,
        )

    if inputs.risk > policy.max_risk_allowed:
        return AutonomyVerdict(
            verdict_id=_verdict_id(proposal, policy, AutonomyLevel.HUMAN_REVIEW),
            proposal_id=proposal.proposal_id,
            autonomy=AutonomyLevel.HUMAN_REVIEW,
            reason=(
                f"risk {inputs.risk:.2f} exceeds policy limit "
                f"{policy.max_risk_allowed}; requires human review"
            ),
            policy_id=policy.policy_id,
        )

    if inputs.monetary_impact > policy.max_monetary_impact:
        return AutonomyVerdict(
            verdict_id=_verdict_id(proposal, policy, AutonomyLevel.APPROVED),
            proposal_id=proposal.proposal_id,
            autonomy=AutonomyLevel.APPROVED,
            reason=(
                f"monetary_impact {inputs.monetary_impact:.2f} exceeds policy "
                f"limit {policy.max_monetary_impact:.2f}; requires explicit approval"
            ),
            policy_id=policy.policy_id,
        )

    # Otherwise the most permissive level allowed by scope applies.
    return AutonomyVerdict(
        verdict_id=_verdict_id(proposal, policy, permitted),
        proposal_id=proposal.proposal_id,
        autonomy=permitted,
        reason=f"within policy {policy.policy_id}; autonomy level {permitted.value}",
        policy_id=policy.policy_id,
    )


def _verdict_id(
    proposal: AgentProposal,
    policy: AutonomyPolicy,
    level: AutonomyLevel,
) -> str:
    payload = json.dumps(
        {
            "proposal_id": proposal.proposal_id,
            "policy_id": policy.policy_id,
            "level": level.value,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256(payload.encode()).hexdigest()
