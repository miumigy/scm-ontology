from __future__ import annotations

from collections.abc import Iterable

from .relation_validation_policy import ValidationDisposition, disposition_for
from .relation_validation_result import RelationValidationResult


def review_queue(
    results: Iterable[RelationValidationResult],
) -> tuple[RelationValidationResult, ...]:
    """Return only REVIEW results, preserving source order."""
    return tuple(
        result
        for result in results
        if disposition_for(result) is ValidationDisposition.REVIEW
    )
