from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .relation_validation_extension import extension_candidate_queue
from .relation_validation_result import RelationValidationResult


@dataclass(frozen=True)
class ExtensionCandidateReport:
    candidates: tuple[RelationValidationResult, ...]


def build_extension_candidate_report(
    results: Iterable[RelationValidationResult],
) -> ExtensionCandidateReport:
    return ExtensionCandidateReport(extension_candidate_queue(results))
