"""First-class identity for canonical SCM relationships."""
from __future__ import annotations

from dataclasses import dataclass


class RelationshipIdentityError(ValueError):
    """Raised when a relationship identity is invalid."""


@dataclass(frozen=True)
class RelationshipInstance:
    """A uniquely referenceable semantic relationship instance."""

    relationship_id: str
    from_id: str
    predicate: str
    to_id: str

    def __post_init__(self) -> None:
        for field_name in ("relationship_id", "from_id", "predicate", "to_id"):
            if not getattr(self, field_name).strip():
                raise RelationshipIdentityError(f"{field_name} must be non-empty")

    @property
    def identity(self) -> str:
        return self.relationship_id

    def endpoints(self) -> tuple[str, str]:
        return self.from_id, self.to_id


def is_relationship_instance(value: object) -> bool:
    return isinstance(value, RelationshipInstance)
