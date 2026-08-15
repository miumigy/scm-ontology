from __future__ import annotations


class TypeHierarchyError(ValueError):
    """Raised when the canonical type hierarchy is malformed."""


# Deliberately small and explicit. This is a vocabulary contract, not inference.
CANONICAL_TYPE_PARENTS: dict[str, tuple[str, ...]] = {
    "PhysicalEntity": ("Entity",),
    "Location": ("Entity",),
    "Node": ("Location",),
    "Facility": ("Node",),
    "Product": ("PhysicalEntity",),
    "Material": ("PhysicalEntity",),
    "Item": ("PhysicalEntity",),
    "Resource": ("PhysicalEntity",),
    "Flow": ("PhysicalEntity",),
    "Demand": ("Entity",),
    "Order": ("Entity",),
    "Supply": ("Entity",),
    "Inventory": ("Entity",),
    "Capacity": ("Entity",),
    "Plan": ("Entity",),
    "Schedule": ("Entity",),
    "Commitment": ("Entity",),
    "Execution": ("Entity",),
    "Measurement": ("Entity",),
    "Metric": ("Entity",),
    "KPI": ("Metric",),
}


def direct_parents(type_ref: str) -> tuple[str, ...]:
    return CANONICAL_TYPE_PARENTS.get(type_ref, ())


def is_known_type(type_ref: str) -> bool:
    return type_ref == "Entity" or type_ref in CANONICAL_TYPE_PARENTS
