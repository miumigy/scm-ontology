from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass

from .relation_validation_policy import ValidationDisposition, disposition_for
from .relation_validation_result import RelationValidationResult


@dataclass(frozen=True)
class RelationValidationReport:
    results: tuple[RelationValidationResult, ...]

    @property
    def dispositions(self) -> tuple[ValidationDisposition, ...]:
        return tuple(disposition_for(result) for result in self.results)

    @property
    def disposition_counts(self) -> dict[str, int]:
        counts = Counter(self.dispositions)
        return {
            ValidationDisposition.ACCEPT.value: counts[ValidationDisposition.ACCEPT],
            ValidationDisposition.REVIEW.value: counts[ValidationDisposition.REVIEW],
            ValidationDisposition.EXTENSION_CANDIDATE.value: counts[ValidationDisposition.EXTENSION_CANDIDATE],
        }


def build_validation_report(
    results: Iterable[RelationValidationResult],
) -> RelationValidationReport:
    return RelationValidationReport(tuple(results))
