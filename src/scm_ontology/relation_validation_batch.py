from __future__ import annotations

from collections.abc import Iterable

from .relation_validation_pipeline import validate_relation
from .relation_validation_result import RelationValidationResult


def validate_relations(
    relations: Iterable[tuple[str, str, str]],
) -> tuple[RelationValidationResult, ...]:
    """Validate typed relations independently and preserve input order."""
    return tuple(
        validate_relation(predicate_ref, subject_type, object_type)
        for predicate_ref, subject_type, object_type in relations
    )
