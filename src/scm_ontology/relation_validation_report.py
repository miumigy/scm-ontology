from __future__ import annotations

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


def build_validation_report(
    results: Iterable[RelationValidationResult],
) -> RelationValidationReport:
    return RelationValidationReport(tuple(results))
