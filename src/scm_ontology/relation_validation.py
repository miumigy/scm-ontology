from __future__ import annotations

from .canonical_relations import CANONICAL_RELATION_TYPES
from .core_instance import CanonicalRelation


CANONICAL_PREDICATES = frozenset(item.predicate_ref for item in CANONICAL_RELATION_TYPES)


class CanonicalRelationValidationError(ValueError):
    """Raised when a relation uses a non-canonical predicate."""


def validate_canonical_relation(relation: CanonicalRelation) -> None:
    """Validate that a relation uses a registered canonical predicate."""
    if relation.predicate_ref not in CANONICAL_PREDICATES:
        raise CanonicalRelationValidationError(
            f"unknown canonical predicate: {relation.predicate_ref}"
        )
