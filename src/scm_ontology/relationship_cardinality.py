"""Selected cardinality constraints for canonical SCM relationships."""
from __future__ import annotations

from dataclasses import dataclass

from .cardinality import ONE, ZERO_OR_MANY, Cardinality


@dataclass(frozen=True)
class RelationshipCardinality:
    predicate: str
    from_cardinality: Cardinality
    to_cardinality: Cardinality


CANONICAL_RELATIONSHIP_CARDINALITIES = (
    RelationshipCardinality("plays_role", ONE, ZERO_OR_MANY),
    RelationshipCardinality("places", ZERO_OR_MANY, ONE),
    RelationshipCardinality("receives", ZERO_OR_MANY, ONE),
    RelationshipCardinality("executes", ZERO_OR_MANY, ONE),
    RelationshipCardinality("located_at", ZERO_OR_MANY, ONE),
    RelationshipCardinality("establishes", ZERO_OR_MANY, ZERO_OR_MANY),
    RelationshipCardinality("changes", ZERO_OR_MANY, ZERO_OR_MANY),
)


def get_relationship_cardinality(predicate: str) -> RelationshipCardinality | None:
    return next(
        (item for item in CANONICAL_RELATIONSHIP_CARDINALITIES if item.predicate == predicate),
        None,
    )
