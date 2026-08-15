from __future__ import annotations

from .canonical_relations import CANONICAL_RELATION_TYPES
from .relation_validation import RelationValidationError, validate_relation_instance
from .relation_validation_result import RelationValidationResult, ValidationStatus

_KNOWN = {item.predicate_ref for item in CANONICAL_RELATION_TYPES}


def validate_relation(
    predicate_ref: str,
    subject_type: str,
    object_type: str,
) -> RelationValidationResult:
    """Validate one typed relation while preserving review/extension semantics."""
    if predicate_ref not in _KNOWN:
        return RelationValidationResult(
            predicate_ref,
            ValidationStatus.EXTENSION,
            "unknown canonical predicate",
            subject_type,
            object_type,
            None,
            None,
        )
    try:
        validate_relation_instance(predicate_ref, subject_type, object_type)
    except RelationValidationError as exc:
        return RelationValidationResult(
            predicate_ref,
            ValidationStatus.REVIEW,
            str(exc),
            subject_type,
            object_type,
            False,
            False,
        )
    return RelationValidationResult(
        predicate_ref,
        ValidationStatus.PASS,
        subject_type=subject_type,
        object_type=object_type,
        domain_ok=True,
        range_ok=True,
    )
