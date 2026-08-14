"""Canonical constraints for validating SCM relationship endpoints."""
from __future__ import annotations

from dataclasses import dataclass


class RelationshipConstraintError(ValueError):
    """Raised when a relationship violates its canonical constraint."""


@dataclass(frozen=True)
class RelationshipConstraint:
    """Allowed endpoint categories for a canonical predicate."""

    predicate: str
    allowed_from: tuple[str, ...]
    allowed_to: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.predicate.strip():
            raise RelationshipConstraintError("predicate must be non-empty")
        if not self.allowed_from:
            raise RelationshipConstraintError("allowed_from must be non-empty")
        if not self.allowed_to:
            raise RelationshipConstraintError("allowed_to must be non-empty")

    def allows(self, from_type: str, to_type: str) -> bool:
        return from_type in self.allowed_from and to_type in self.allowed_to


CANONICAL_RELATIONSHIP_CONSTRAINTS = (
    RelationshipConstraint("places", ("Party", "Customer"), ("CustomerOrder",)),
    RelationshipConstraint("receives", ("Party", "Supplier"), ("PurchaseOrder",)),
    RelationshipConstraint("executes", ("Party", "Carrier"), ("Shipment",)),
    RelationshipConstraint("establishes", ("Event",), ("State",)),
    RelationshipConstraint("changes", ("Event",), ("State",)),
    RelationshipConstraint("located_at", ("Item", "Party", "Inventory"), ("Location",)),
    RelationshipConstraint("moves_to", ("PhysicalFlow", "Shipment"), ("Location",)),
    RelationshipConstraint("supplies", ("Party", "PurchaseOrder", "ProductionOrder"), ("Supply",)),
    RelationshipConstraint("consumes", ("ProductionOrder", "Demand", "PhysicalFlow"), ("Supply", "Item")),
)


def get_relationship_constraint(predicate: str) -> RelationshipConstraint | None:
    return next((c for c in CANONICAL_RELATIONSHIP_CONSTRAINTS if c.predicate == predicate), None)


def validate_relationship(predicate: str, from_type: str, to_type: str) -> None:
    constraint = get_relationship_constraint(predicate)
    if constraint is None:
        return
    if not constraint.allows(from_type, to_type):
        raise RelationshipConstraintError(
            f"invalid endpoints for {predicate}: {from_type} -> {to_type}"
        )
