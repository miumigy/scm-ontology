"""Canonical Decision Proposal boundary for SCM OS integration.

S334 represents a proposed action without executing or approving it. A proposal
references an existing DecisionContext and carries explicit rationale,
evidence, and provenance.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any


class DecisionProposalError(ValueError):
    """Raised when an S334 input violates the canonical contract."""


@dataclass(frozen=True)
class DecisionProposal:
    decision_id: str
    decision_type: str
    context_id: str
    action: Any
    rationale: str
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name, value in (("decision_id", self.decision_id), ("decision_type", self.decision_type), ("context_id", self.context_id), ("rationale", self.rationale)):
            if not value.strip():
                raise DecisionProposalError(f"{name} must be non-empty")
        object.__setattr__(self, "evidence_ids", tuple(sorted(set(self.evidence_ids))))
        object.__setattr__(self, "provenance_ids", tuple(sorted(set(self.provenance_ids))))

    def to_mapping(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "decision_type": self.decision_type,
            "context_id": self.context_id,
            "action": self.action,
            "rationale": self.rationale,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


def decision_proposal_to_mapping(proposal: DecisionProposal) -> dict[str, Any]:
    return {"contract_version": "S334.1", **proposal.to_mapping()}


def decision_proposal_to_json(proposal: DecisionProposal) -> str:
    return json.dumps(decision_proposal_to_mapping(proposal), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
