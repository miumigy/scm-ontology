"""Immutable authorization boundary for validated decision proposals."""
from __future__ import annotations

from dataclasses import dataclass

from .proposal_validation import ValidatedDecisionProposal


class DecisionAuthorizationError(ValueError):
    """Raised when a decision proposal cannot be authorized."""


@dataclass(frozen=True)
class AuthorizedDecision:
    proposal: ValidatedDecisionProposal
    actor_id: str
    authority: str
    authorized_at: str

    def __post_init__(self) -> None:
        if not self.actor_id.strip():
            raise DecisionAuthorizationError("actor_id must be non-empty")
        if not self.authority.strip():
            raise DecisionAuthorizationError("authority must be non-empty")
        if not self.authorized_at.strip():
            raise DecisionAuthorizationError("authorized_at must be non-empty")

    @property
    def context_id(self) -> str:
        return self.proposal.output.context_id

    def to_mapping(self) -> dict[str, object]:
        return {
            "contract_version": "S345.1",
            "context_id": self.context_id,
            "proposal": self.proposal.output.proposal,
            "actor_id": self.actor_id,
            "authority": self.authority,
            "authorized_at": self.authorized_at,
            "evidence_ids": list(self.proposal.output.evidence_ids),
            "provenance_ids": list(self.proposal.output.provenance_ids),
        }


def authorize_decision(
    proposal: ValidatedDecisionProposal,
    *,
    actor_id: str,
    authority: str,
    authorized_at: str,
) -> AuthorizedDecision:
    """Record authorization of an already validated proposal; never execute it."""
    return AuthorizedDecision(
        proposal=proposal,
        actor_id=actor_id,
        authority=authority,
        authorized_at=authorized_at,
    )
