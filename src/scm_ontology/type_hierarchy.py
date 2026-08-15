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


def is_subtype_of(type_ref: str, expected_type: str) -> bool:
    """Return whether type_ref is equal to or below expected_type."""
    if not is_known_type(type_ref) or not is_known_type(expected_type):
        return False
    if type_ref == expected_type:
        return True
    visited: set[str] = set()
    stack = list(direct_parents(type_ref))
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        if current == expected_type:
            return True
        stack.extend(direct_parents(current))
    return False
