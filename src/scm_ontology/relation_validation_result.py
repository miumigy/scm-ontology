from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ValidationStatus(str, Enum):
    PASS = "pass"
    REVIEW = "review"
    EXTENSION = "extension"
    ERROR = "error"


@dataclass(frozen=True)
class RelationValidationResult:
    predicate_ref: str
    status: ValidationStatus
    reason: str = ""
    subject_type: str | None = None
    object_type: str | None = None
    domain_ok: bool | None = None
    range_ok: bool | None = None

    @property
    def valid(self) -> bool:
        return self.status is ValidationStatus.PASS


def validation_result(
    predicate_ref: str,
    *,
    domain_ok: bool,
    range_ok: bool,
    known_predicate: bool = True,
    subject_type: str | None = None,
    object_type: str | None = None,
) -> RelationValidationResult:
    if not known_predicate:
        return RelationValidationResult(
            predicate_ref,
            ValidationStatus.EXTENSION,
            "unknown canonical predicate",
            subject_type,
            object_type,
            domain_ok,
            range_ok,
        )
    if domain_ok and range_ok:
        return RelationValidationResult(
            predicate_ref,
            ValidationStatus.PASS,
            subject_type=subject_type,
            object_type=object_type,
            domain_ok=domain_ok,
            range_ok=range_ok,
        )
    return RelationValidationResult(
        predicate_ref,
        ValidationStatus.REVIEW,
        "domain/range constraint requires review",
        subject_type,
        object_type,
        domain_ok,
        range_ok,
    )
