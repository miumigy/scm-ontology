"""Canonical, framework-independent state semantics."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


class CanonicalStateError(ValueError):
    """Raised when a canonical state violates its semantic contract."""


@dataclass(frozen=True)
class CanonicalState:
    """A condition or configuration that holds for an entity over a period."""

    entity_id: str
    state_type: str
    attributes: Mapping[str, object]

    def __post_init__(self) -> None:
        if not self.entity_id:
            raise CanonicalStateError("entity_id must be non-empty")
        if not self.state_type:
            raise CanonicalStateError("state_type must be non-empty")
        if self.attributes is None:
            raise CanonicalStateError("attributes must be provided")


def is_state(value: object) -> bool:
    """Return whether a value is explicitly a CanonicalState."""
    return isinstance(value, CanonicalState)
