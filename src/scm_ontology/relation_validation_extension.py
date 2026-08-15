from __future__ import annotations

from collections.abc import Iterable

from .relation_validation_policy import ValidationDisposition, disposition_for
from .relation_validation_result import RelationValidationResult


def extension_candidate_queue(
    results: Iterable[RelationValidationResult],
) -> tuple[RelationValidationResult, ...]:
    """Return extension candidates in source order without promoting them."""
    return tuple(
        result
        for result in results
        if disposition_for(result) is ValidationDisposition.EXTENSION_CANDIDATE
    )
