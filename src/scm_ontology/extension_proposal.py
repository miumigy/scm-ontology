from __future__ import annotations

from dataclasses import dataclass

from .extension_governance_decision import GovernanceDecision


class InvalidExtensionProposal(ValueError):
    pass


@dataclass(frozen=True)
class ExtensionProposal:
    candidate_ref: str
    predicate_ref: str
    subject_type: str
    object_type: str


def build_extension_proposal(
    candidate_ref: str,
    predicate_ref: str,
    subject_type: str,
    object_type: str,
    decision: GovernanceDecision,
) -> ExtensionProposal:
    if decision is not GovernanceDecision.ACCEPTED:
        raise InvalidExtensionProposal(
            "an extension proposal requires an ACCEPTED governance decision"
        )
    return ExtensionProposal(candidate_ref, predicate_ref, subject_type, object_type)
