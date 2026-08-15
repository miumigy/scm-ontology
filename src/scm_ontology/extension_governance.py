from __future__ import annotations

from enum import StrEnum

from .relation_validation_result import RelationValidationResult


class ExtensionDecision(StrEnum):
    PENDING = "pending"
    ACCEPT = "accept"
    REJECT = "reject"


def initial_extension_decision(
    candidate: RelationValidationResult,
) -> ExtensionDecision:
    """Create a governance state without approving or rejecting the candidate."""
    del candidate
    return ExtensionDecision.PENDING
