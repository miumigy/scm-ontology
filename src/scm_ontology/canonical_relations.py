from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RelationModelError(ValueError):
    """Raised when a canonical relation violates its invariants."""


class RelationKind(str, Enum):
    PHYSICAL = "physical"
    INFORMATIONAL = "informational"
    TEMPORAL = "temporal"
    CAUSAL = "causal"
    EPISTEMIC = "epistemic"
    ORGANIZATIONAL = "organizational"
    OPERATIONAL = "operational"
    GOVERNANCE = "governance"


@dataclass(frozen=True)
class CanonicalRelationType:
    """Transport-neutral definition of a canonical relation predicate."""

    predicate_ref: str
    kind: RelationKind
    inverse_ref: str | None = None
    description: str = ""

    def __post_init__(self) -> None:
        if not self.predicate_ref.strip():
            raise RelationModelError("predicate_ref is required")
        if self.inverse_ref == self.predicate_ref:
            raise RelationModelError("a relation cannot be its own inverse")


CANONICAL_RELATION_TYPES: tuple[CanonicalRelationType, ...] = (
    CanonicalRelationType("causes", RelationKind.CAUSAL, "caused_by"),
    CanonicalRelationType("affects", RelationKind.CAUSAL, "affected_by"),
    CanonicalRelationType("depends_on", RelationKind.OPERATIONAL, "required_by"),
    CanonicalRelationType("derived_from", RelationKind.INFORMATIONAL, "source_of"),
    CanonicalRelationType("located_at", RelationKind.PHYSICAL, "location_of"),
    CanonicalRelationType("contains", RelationKind.PHYSICAL, "contained_in"),
    CanonicalRelationType("part_of", RelationKind.PHYSICAL, "has_part"),
    CanonicalRelationType("transforms", RelationKind.PHYSICAL, "transformed_by"),
    CanonicalRelationType("consumes", RelationKind.PHYSICAL, "consumed_by"),
    CanonicalRelationType("produces", RelationKind.PHYSICAL, "produced_by"),
    CanonicalRelationType("supplies", RelationKind.OPERATIONAL, "supplied_by"),
    CanonicalRelationType("fulfills", RelationKind.OPERATIONAL, "fulfilled_by"),
    CanonicalRelationType("allocated_to", RelationKind.OPERATIONAL, "has_allocation"),
    CanonicalRelationType("reserved_for", RelationKind.OPERATIONAL, "has_reservation"),
    CanonicalRelationType("committed_to", RelationKind.OPERATIONAL, "has_commitment"),
    CanonicalRelationType("planned_for", RelationKind.TEMPORAL, "has_plan"),
    CanonicalRelationType("scheduled_for", RelationKind.TEMPORAL, "has_schedule"),
    CanonicalRelationType("executes", RelationKind.OPERATIONAL, "executed_by"),
    CanonicalRelationType("flows_through", RelationKind.PHYSICAL, "has_flow"),
    CanonicalRelationType("uses", RelationKind.OPERATIONAL, "used_by"),
    CanonicalRelationType("constrained_by", RelationKind.GOVERNANCE, "constrains"),
    CanonicalRelationType("governed_by", RelationKind.GOVERNANCE, "governs"),
    CanonicalRelationType("measured_by", RelationKind.INFORMATIONAL, "measures"),
    CanonicalRelationType("evaluated_by", RelationKind.INFORMATIONAL, "evaluates"),
    CanonicalRelationType("decided_by", RelationKind.GOVERNANCE, "decides"),
    CanonicalRelationType("results_in", RelationKind.CAUSAL, "resulted_from"),
)
