"""Canonical relationships between party roles and SCM transactions."""
from __future__ import annotations

from dataclasses import dataclass


class PartyTransactionRelationshipError(ValueError):
    """Raised when a party-transaction relationship is invalid."""


@dataclass(frozen=True)
class PartyTransactionRelationship:
    """A contextual role relationship between a Party and a transaction."""

    party_role: str
    predicate: str
    transaction_type: str

    def __post_init__(self) -> None:
        if not self.party_role.strip():
            raise PartyTransactionRelationshipError("party_role must be non-empty")
        if not self.predicate.strip():
            raise PartyTransactionRelationshipError("predicate must be non-empty")
        if not self.transaction_type.strip():
            raise PartyTransactionRelationshipError("transaction_type must be non-empty")


CANONICAL_PARTY_TRANSACTION_RELATIONSHIPS = (
    PartyTransactionRelationship("customer", "places", "CustomerOrder"),
    PartyTransactionRelationship("supplier", "receives", "PurchaseOrder"),
    PartyTransactionRelationship("manufacturer", "creates", "ProductionOrder"),
    PartyTransactionRelationship("carrier", "executes", "Shipment"),
)


def is_party_transaction_relationship(value: object) -> bool:
    return isinstance(value, PartyTransactionRelationship)
