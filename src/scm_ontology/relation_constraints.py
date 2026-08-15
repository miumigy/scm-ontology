from __future__ import annotations

from dataclasses import dataclass


class RelationConstraintError(ValueError):
    """Raised when a relation domain/range constraint is invalid."""


@dataclass(frozen=True)
class RelationConstraint:
    predicate_ref: str
    domain: tuple[str, ...]
    range: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.predicate_ref.strip():
            raise RelationConstraintError("predicate_ref is required")
        if not self.domain or not self.range:
            raise RelationConstraintError("domain and range must not be empty")


CANONICAL_RELATION_CONSTRAINTS: tuple[RelationConstraint, ...] = (
    RelationConstraint("located_at", ("PhysicalEntity",), ("Location", "Node")),
    RelationConstraint("contains", ("Location", "Node", "Facility"), ("PhysicalEntity",)),
    RelationConstraint("part_of", ("Entity",), ("Entity",)),
    RelationConstraint("transforms", ("Node", "Facility", "Transformation"), ("Product", "Material", "Item")),
    RelationConstraint("consumes", ("Transformation", "Execution"), ("Material", "Item", "Resource")),
    RelationConstraint("produces", ("Transformation", "Execution"), ("Product", "Material", "Item")),
    RelationConstraint("supplies", ("Organization", "Node", "Supply"), ("Demand", "Order", "Inventory")),
    RelationConstraint("fulfills", ("Supply", "Order", "Execution"), ("Demand", "Order", "Commitment")),
    RelationConstraint("allocated_to", ("Inventory", "Capacity", "Supply"), ("Demand", "Order")),
    RelationConstraint("reserved_for", ("Inventory", "Capacity"), ("Demand", "Order", "Commitment")),
    RelationConstraint("committed_to", ("Commitment", "Plan", "Schedule"), ("Demand", "Order")),
    RelationConstraint("planned_for", ("Plan", "Schedule"), ("Demand", "Supply", "Execution")),
    RelationConstraint("scheduled_for", ("Schedule",), ("Execution", "Flow")),
    RelationConstraint("executes", ("Organization", "Resource", "Execution"), ("Action", "Plan", "Schedule")),
    RelationConstraint("flows_through", ("Flow",), ("Node", "Location", "Lane", "Route")),
    RelationConstraint("measured_by", ("Entity", "Event", "State"), ("Measurement", "Metric")),
    RelationConstraint("evaluated_by", ("Entity", "Performance"), ("KPI", "Metric", "PerformanceAssessment")),
    RelationConstraint("decided_by", ("Decision", "Action"), ("Organization", "Actor", "Policy")),
)

_CONSTRAINTS = {item.predicate_ref: item for item in CANONICAL_RELATION_CONSTRAINTS}


def relation_constraint(predicate_ref: str) -> RelationConstraint:
    try:
        return _CONSTRAINTS[predicate_ref]
    except KeyError as exc:
        raise RelationConstraintError(f"no canonical domain/range constraint: {predicate_ref}") from exc
