from __future__ import annotations

from .canonical_relations import CANONICAL_RELATION_TYPES
from .relation_constraints import RelationConstraintError, relation_constraint
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
        constraint = relation_constraint(predicate_ref)
    except RelationConstraintError as exc:
        return RelationValidationResult(
            predicate_ref,
            ValidationStatus.REVIEW,
            str(exc),
            subject_type,
            object_type,
            None,
            None,
        )

    domain_ok = subject_type in constraint.domain
    range_ok = object_type in constraint.range
    if domain_ok and range_ok:
        return RelationValidationResult(
            predicate_ref,
            ValidationStatus.PASS,
            subject_type=subject_type,
            object_type=object_type,
            domain_ok=True,
            range_ok=True,
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
