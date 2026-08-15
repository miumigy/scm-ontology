from __future__ import annotations

from enum import StrEnum

from .relation_validation_result import RelationValidationResult, ValidationStatus


class ValidationDisposition(StrEnum):
    ACCEPT = "accept"
    REVIEW = "review"
    EXTENSION_CANDIDATE = "extension_candidate"


def disposition_for(result: RelationValidationResult) -> ValidationDisposition:
    """Map validation status to an explicit downstream disposition."""
    if result.status is ValidationStatus.PASS:
        return ValidationDisposition.ACCEPT
    if result.status is ValidationStatus.REVIEW:
        return ValidationDisposition.REVIEW
    return ValidationDisposition.EXTENSION_CANDIDATE
