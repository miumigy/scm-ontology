from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class GovernanceDecision(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class InvalidGovernanceTransition(ValueError):
    pass


@dataclass(frozen=True)
class ExtensionGovernanceDecision:
    candidate_ref: str
    status: GovernanceDecision = GovernanceDecision.PENDING

    def accept(self) -> ExtensionGovernanceDecision:
        return self._transition(GovernanceDecision.ACCEPTED)

    def reject(self) -> ExtensionGovernanceDecision:
        return self._transition(GovernanceDecision.REJECTED)

    def _transition(self, target: GovernanceDecision) -> ExtensionGovernanceDecision:
        if self.status is not GovernanceDecision.PENDING:
            raise InvalidGovernanceTransition(
                f"cannot transition {self.status.value} decision"
            )
        return ExtensionGovernanceDecision(self.candidate_ref, target)
