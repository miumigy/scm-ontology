from __future__ import annotations

from .relation_constraints import relation_constraint


class RelationInstanceValidationError(ValueError):
    """Raised when a typed relation instance violates its contract."""


def validate_relation_instance(predicate_ref: str, subject_type: str, object_type: str) -> None:
    """Validate a typed relation instance against canonical domain/range constraints."""
    constraint = relation_constraint(predicate_ref)
    if subject_type not in constraint.domain:
        raise RelationInstanceValidationError(
            f"invalid domain for {predicate_ref}: {subject_type}"
        )
    if object_type not in constraint.range:
        raise RelationInstanceValidationError(
            f"invalid range for {predicate_ref}: {object_type}"
        )
