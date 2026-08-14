"""Canonical party concept for the SCM domain layer."""
from __future__ import annotations

from dataclasses import dataclass


class PartyConceptError(ValueError):
    """Raised when a canonical party is invalid."""


@dataclass(frozen=True)
class CanonicalParty:
    """An organization or actor participating in a supply-chain context."""

    party_id: str
    name: str
    party_type: str = "organization"

    def __post_init__(self) -> None:
        if not self.party_id.strip():
            raise PartyConceptError("party_id must be non-empty")
        if not self.name.strip():
            raise PartyConceptError("name must be non-empty")
        if not self.party_type.strip():
            raise PartyConceptError("party_type must be non-empty")


def is_party(value: object) -> bool:
    return isinstance(value, CanonicalParty)
