from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

from .relation_validation_result import RelationValidationResult, ValidationStatus


def summarize_validation(
    results: Iterable[RelationValidationResult],
) -> dict[str, int]:
    """Return deterministic counts by validation status."""
    counts = Counter(result.status for result in results)
    return {
        ValidationStatus.PASS.value: counts[ValidationStatus.PASS],
        ValidationStatus.REVIEW.value: counts[ValidationStatus.REVIEW],
        ValidationStatus.EXTENSION.value: counts[ValidationStatus.EXTENSION],
    }
