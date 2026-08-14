"""Canonical party role contract for SCM semantics."""
from __future__ import annotations

from dataclasses import dataclass


class PartyRoleContractError(ValueError):
    """Raised when a party role contract is invalid."""


@dataclass(frozen=True)
class CanonicalPartyRole:
    """A role played by a Party within an explicit SCM context."""

    party_id: str
    role: str
    context: str = "supply_chain"

    def __post_init__(self) -> None:
        if not self.party_id.strip():
            raise PartyRoleContractError("party_id must be non-empty")
        if not self.role.strip():
            raise PartyRoleContractError("role must be non-empty")
        if not self.context.strip():
            raise PartyRoleContractError("context must be non-empty")


CANONICAL_PARTY_ROLES = (
    "supplier",
    "customer",
    "manufacturer",
    "carrier",
    "logistics_provider",
)


def is_party_role(value: object) -> bool:
    return isinstance(value, CanonicalPartyRole)
