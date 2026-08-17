"""SCM OS authorization governance (Phase R4) — S356 policy, approval, override.

S356 provides the fail-closed authorization policy, human approval, and senior
override gates for the governed decision loop. It decides whether an already
validated proposal may be authorized, reusing the S345 ``authorize_decision``
boundary. It never performs an external side effect.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from .decision_authorization import AuthorizedDecision, authorize_decision
from .proposal_validation import ValidatedDecisionProposal


class AuthorizationGovernanceError(ValueError):
    """Raised when a proposal is not authorized by policy/approval/override."""


@dataclass(frozen=True)
class AuthorizationDecision:
    """Immutable result of evaluating an authorization policy."""

    allowed: bool
    policy_id: str
    requires_approval: bool = False
    reason: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.policy_id, str) or not self.policy_id.strip():
            raise AuthorizationGovernanceError("policy_id must be non-empty")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "policy_id": self.policy_id,
            "requires_approval": self.requires_approval,
            "reason": self.reason,
        }


class AuthorizationPolicy(Protocol):
    """Fail-closed gate that decides whether a proposal may be authorized."""

    policy_id: str

    def decide(
        self,
        *,
        proposal: ValidatedDecisionProposal,
        actor_id: str,
        authority: str,
        command_type: str,
    ) -> AuthorizationDecision: ...


@dataclass(frozen=True)
class DefaultAuthorizationPolicy:
    """Allow-list policy keyed on authority; fails closed by default."""

    policy_id: str
    allowed_authorities: tuple[str, ...]
    require_approval_for: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.policy_id, str) or not self.policy_id.strip():
            raise AuthorizationGovernanceError("policy_id must be non-empty")
        if not self.allowed_authorities:
            raise AuthorizationGovernanceError("allowed_authorities must not be empty")
        object.__setattr__(self, "allowed_authorities", tuple(self.allowed_authorities))
        object.__setattr__(self, "require_approval_for", tuple(self.require_approval_for))

    def decide(
        self,
        *,
        proposal: ValidatedDecisionProposal,
        actor_id: str,
        authority: str,
        command_type: str,
    ) -> AuthorizationDecision:
        if authority not in self.allowed_authorities:
            return AuthorizationDecision(
                allowed=False,
                policy_id=self.policy_id,
                reason=f"authority {authority!r} is not permitted",
            )
        requires_approval = command_type in self.require_approval_for
        return AuthorizationDecision(
            allowed=True,
            policy_id=self.policy_id,
            requires_approval=requires_approval,
            reason="authorization allowed by policy",
        )


@dataclass(frozen=True)
class ApprovalRecord:
    """Record of an explicit human approval for a context and command type."""

    approval_id: str
    context_id: str
    command_type: str
    approver_id: str
    approved_at: str
    reason: str = ""

    def __post_init__(self) -> None:
        for name in ("approval_id", "context_id", "command_type", "approver_id", "approved_at"):
            if not getattr(self, name).strip():
                raise AuthorizationGovernanceError(f"{name} must be non-empty")

    def matches(self, context_id: str, command_type: str) -> bool:
        return self.context_id == context_id and self.command_type == command_type


@dataclass(frozen=True)
class DecisionOverride:
    """Record of an explicit senior override that permits a denied routine decision."""

    override_id: str
    context_id: str
    actor_id: str
    authority: str
    overridden_at: str
    reason: str = ""

    def __post_init__(self) -> None:
        for name in ("override_id", "context_id", "actor_id", "authority", "overridden_at"):
            if not getattr(self, name).strip():
                raise AuthorizationGovernanceError(f"{name} must be non-empty")

    def matches(self, context_id: str, actor_id: str, authority: str) -> bool:
        return (
            self.context_id == context_id
            and self.actor_id == actor_id
            and self.authority == authority
        )


def evaluate_authorization_policy(
    policy: AuthorizationPolicy,
    *,
    proposal: ValidatedDecisionProposal,
    actor_id: str,
    authority: str,
    command_type: str,
) -> AuthorizationDecision:
    """Evaluate a fail-closed authorization policy against a validated proposal."""
    if not isinstance(proposal, ValidatedDecisionProposal):
        raise AuthorizationGovernanceError("proposal must be a ValidatedDecisionProposal")
    policy_id = getattr(policy, "policy_id", None)
    if not isinstance(policy_id, str) or not policy_id.strip():
        raise AuthorizationGovernanceError("policy must expose a non-empty policy_id")
    decide = getattr(policy, "decide", None)
    if not callable(decide):
        raise AuthorizationGovernanceError("policy must expose a callable decide method")
    decision = decide(
        proposal=proposal,
        actor_id=actor_id,
        authority=authority,
        command_type=command_type,
    )
    if not isinstance(decision, AuthorizationDecision):
        raise AuthorizationGovernanceError("policy decide must return an AuthorizationDecision")
    return decision


def authorize_under_policy(
    proposal: ValidatedDecisionProposal,
    *,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_type: str,
    policy: AuthorizationPolicy,
    approvals: Sequence[ApprovalRecord] = (),
    overrides: Sequence[DecisionOverride] = (),
) -> AuthorizedDecision:
    """Authorize a validated proposal subject to policy, approval, and override.

    Fails closed (raises) unless the policy allows and, when required, an
    explicit human approval or senior override is present.
    """
    decision = evaluate_authorization_policy(
        policy,
        proposal=proposal,
        actor_id=actor_id,
        authority=authority,
        command_type=command_type,
    )
    context_id = proposal.output.context_id

    if not decision.allowed:
        if not any(o.matches(context_id, actor_id, authority) for o in overrides):
            raise AuthorizationGovernanceError(
                f"authorization denied by {decision.policy_id}: {decision.reason}"
            )

    if decision.requires_approval:
        if not any(a.matches(context_id, command_type) for a in approvals):
            raise AuthorizationGovernanceError(
                f"authorization for {command_type!r} requires human approval"
            )

    return authorize_decision(
        proposal,
        actor_id=actor_id,
        authority=authority,
        authorized_at=authorized_at,
    )
