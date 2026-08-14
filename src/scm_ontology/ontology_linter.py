"""Canonical semantic linter for SCM relationships."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .relationship_cardinality import get_relationship_cardinality
from .relationship_constraints import get_relationship_constraint
from .relationship_identity import RelationshipInstance
from .relationship_version import RelationshipVersion


class ValidationSeverity(str, Enum):
    """Severity of a semantic validation finding."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class ValidationIssue:
    """A single canonical semantic validation finding."""

    code: str
    severity: ValidationSeverity
    message: str


@dataclass(frozen=True)
class ValidationResult:
    """Result of linting one relationship semantic representation."""

    issues: tuple[ValidationIssue, ...] = ()

    @property
    def valid(self) -> bool:
        return not any(issue.severity == ValidationSeverity.ERROR for issue in self.issues)


def lint_relationship(
    relationship: RelationshipInstance,
    from_type: str,
    to_type: str,
    *,
    from_count: int | None = None,
    to_count: int | None = None,
    version: RelationshipVersion | None = None,
) -> ValidationResult:
    """Validate the canonical semantics available for one relationship.

    Unknown predicates are intentionally not rejected. Cardinality checks are
    performed only when occurrence counts are supplied by the caller because
    the canonical relationship itself does not contain dataset-level counts.
    """

    issues: list[ValidationIssue] = []

    constraint = get_relationship_constraint(relationship.predicate)
    if constraint is None:
        issues.append(
            ValidationIssue(
                "UNKNOWN_PREDICATE",
                ValidationSeverity.INFO,
                f"predicate is not in the canonical vocabulary: {relationship.predicate}",
            )
        )
    elif not constraint.allows(from_type, to_type):
        issues.append(
            ValidationIssue(
                "ENDPOINT_CONSTRAINT_VIOLATION",
                ValidationSeverity.ERROR,
                f"invalid endpoints for {relationship.predicate}: {from_type} -> {to_type}",
            )
        )

    cardinality = get_relationship_cardinality(relationship.predicate)
    if cardinality is not None:
        if from_count is not None and not cardinality.from_cardinality.allows(from_count):
            issues.append(
                ValidationIssue(
                    "FROM_CARDINALITY_VIOLATION",
                    ValidationSeverity.ERROR,
                    f"from endpoint count {from_count} violates {relationship.predicate} "
                    f"cardinality {cardinality.from_cardinality}",
                )
            )
        if to_count is not None and not cardinality.to_cardinality.allows(to_count):
            issues.append(
                ValidationIssue(
                    "TO_CARDINALITY_VIOLATION",
                    ValidationSeverity.ERROR,
                    f"to endpoint count {to_count} violates {relationship.predicate} "
                    f"cardinality {cardinality.to_cardinality}",
                )
            )

    if version is not None:
        # RelationshipVersion already enforces these structural invariants.
        # This branch deliberately does not add temporal interval semantics.
        if not version.valid_from.strip():
            issues.append(
                ValidationIssue(
                    "INVALID_VALID_FROM",
                    ValidationSeverity.ERROR,
                    "valid_from must be non-empty",
                )
            )
        if version.valid_to is not None and not version.valid_to.strip():
            issues.append(
                ValidationIssue(
                    "INVALID_VALID_TO",
                    ValidationSeverity.ERROR,
                    "valid_to must be non-empty when provided",
                )
            )

    return ValidationResult(tuple(issues))


def is_validation_result(value: object) -> bool:
    return isinstance(value, ValidationResult)
