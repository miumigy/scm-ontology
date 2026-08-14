"""Canonical relationship contract for SCM domain semantics."""
from __future__ import annotations

from dataclasses import dataclass


class RelationshipContractError(ValueError):
    """Raised when a relationship contract is invalid."""


@dataclass(frozen=True)
class CanonicalRelationship:
    """A typed semantic relation between two canonical concepts."""

    source_type: str
    predicate: str
    target_type: str

    def __post_init__(self) -> None:
        if not self.source_type.strip():
            raise RelationshipContractError("source_type must be non-empty")
        if not self.predicate.strip():
            raise RelationshipContractError("predicate must be non-empty")
        if not self.target_type.strip():
            raise RelationshipContractError("target_type must be non-empty")


CORE_SCM_RELATIONSHIPS = (
    CanonicalRelationship("Inventory", "for_item", "Item"),
    CanonicalRelationship("Inventory", "held_at", "Location"),
    CanonicalRelationship("Demand", "for_item", "Item"),
)


def is_relationship(value: object) -> bool:
    return isinstance(value, CanonicalRelationship)
