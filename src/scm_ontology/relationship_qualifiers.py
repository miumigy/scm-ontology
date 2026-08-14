"""Canonical qualifiers attached to SCM relationships."""
from __future__ import annotations

from dataclasses import dataclass


class RelationshipQualifierError(ValueError):
    """Raised when a relationship qualifier is invalid."""


@dataclass(frozen=True)
class RelationshipQualifier:
    """A typed semantic qualifier whose meaning belongs to a relationship."""

    name: str
    value_type: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise RelationshipQualifierError("qualifier name must be non-empty")
        if not self.value_type.strip():
            raise RelationshipQualifierError("qualifier value_type must be non-empty")


CANONICAL_RELATIONSHIP_QUALIFIERS = (
    RelationshipQualifier("valid_from", "time_reference"),
    RelationshipQualifier("valid_to", "time_reference"),
    RelationshipQualifier("sequence", "integer"),
    RelationshipQualifier("priority", "integer"),
    RelationshipQualifier("allocation_ratio", "decimal"),
)


def is_relationship_qualifier(value: object) -> bool:
    return isinstance(value, RelationshipQualifier)
