"""Canonical predicate vocabulary for SCM graph semantics."""
from __future__ import annotations

from dataclasses import dataclass


class RelationshipVocabularyError(ValueError):
    """Raised when a canonical predicate is invalid."""


@dataclass(frozen=True)
class CanonicalPredicate:
    """A reusable semantic predicate with an explicit category."""

    name: str
    category: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise RelationshipVocabularyError("predicate name must be non-empty")
        if not self.category.strip():
            raise RelationshipVocabularyError("predicate category must be non-empty")


CANONICAL_PREDICATES = (
    CanonicalPredicate("contains", "structural"),
    CanonicalPredicate("located_at", "structural"),
    CanonicalPredicate("part_of", "structural"),
    CanonicalPredicate("plays_role", "participation"),
    CanonicalPredicate("places", "participation"),
    CanonicalPredicate("receives", "participation"),
    CanonicalPredicate("executes", "participation"),
    CanonicalPredicate("establishes", "lifecycle"),
    CanonicalPredicate("changes", "lifecycle"),
    CanonicalPredicate("moves_to", "flow"),
    CanonicalPredicate("supplies", "flow"),
    CanonicalPredicate("consumes", "flow"),
)


def is_canonical_predicate(value: object) -> bool:
    return isinstance(value, CanonicalPredicate)
