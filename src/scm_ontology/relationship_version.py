"""Canonical version and validity semantics for SCM relationships."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


class RelationshipVersionError(ValueError):
    """Raised when a canonical relationship version is invalid."""


@dataclass(frozen=True)
class RelationshipVersion:
    """A temporal semantic version of a relationship instance.

    ``valid_from`` and ``valid_to`` define when this version is semantically
    applicable.  Version identity, persistence, and interval arithmetic are
    intentionally outside this contract.
    """

    valid_from: str
    valid_to: str | None = None
    qualifiers: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        if not self.valid_from.strip():
            raise RelationshipVersionError("valid_from must be non-empty")
        if self.valid_to is not None and not self.valid_to.strip():
            raise RelationshipVersionError("valid_to must be non-empty when provided")
        if self.qualifiers is not None and not isinstance(self.qualifiers, Mapping):
            raise RelationshipVersionError("qualifiers must be a mapping when provided")


def is_relationship_version(value: object) -> bool:
    return isinstance(value, RelationshipVersion)
