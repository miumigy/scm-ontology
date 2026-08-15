from __future__ import annotations

from .relation_constraints import relation_constraint
from .type_hierarchy import is_subtype_of


class SubtypeValidationError(ValueError):
    """Raised when a typed relation cannot satisfy its canonical contract."""


def validate_subtype_compatible_relation(
    predicate_ref: str, subject_type: str, object_type: str
) -> None:
    """Accept exact or explicitly registered subtype-compatible domain/range."""
    constraint = relation_constraint(predicate_ref)
    if not any(is_subtype_of(subject_type, expected) for expected in constraint.domain):
        raise SubtypeValidationError(
            f"invalid domain for {predicate_ref}: {subject_type}"
        )
    if not any(is_subtype_of(object_type, expected) for expected in constraint.range):
        raise SubtypeValidationError(
            f"invalid range for {predicate_ref}: {object_type}"
        )
