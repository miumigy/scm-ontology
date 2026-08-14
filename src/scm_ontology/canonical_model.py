"""Canonical SCM entity and relationship model established by S113.

This module is intentionally a semantic registry, not the final serialized ontology
schema. S114+ will define richer attribute/value semantics and machine-readable
serialization on top of these contracts.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ConceptLayer(StrEnum):
    PRIMITIVE = "primitive"
    CORE = "core"
    DERIVED = "derived"
    CONTEXTUAL = "contextual"


class WorldLayer(StrEnum):
    PHYSICAL = "physical"
    INFORMATION = "information"
    DECISION = "decision"
    SEMANTIC = "semantic"


class RelationshipCategory(StrEnum):
    STRUCTURAL = "structural"
    PARTICIPATION = "participation"
    FLOW = "flow"
    TRANSFORMATION = "transformation"
    FULFILLMENT = "fulfillment"
    PLANNING = "planning"
    COMMITMENT = "commitment"
    LIFECYCLE = "lifecycle"
    GOVERNANCE = "governance"
    DECISION = "decision"
    EPISTEMIC = "epistemic"
    MEASUREMENT = "measurement"
    DERIVATION = "derivation"
    EVALUATION = "evaluation"
    PROVENANCE = "provenance"
    CAUSAL = "causal"
    DEPENDENCY = "dependency"


@dataclass(frozen=True)
class CanonicalConcept:
    name: str
    layer: ConceptLayer
    worlds: tuple[WorldLayer, ...]
    description: str
    abstract: bool = False


@dataclass(frozen=True)
class RelationshipSignature:
    predicate: str
    source: str
    target: str
    category: RelationshipCategory


CANONICAL_CONCEPTS: tuple[CanonicalConcept, ...] = (
    CanonicalConcept("Entity", ConceptLayer.PRIMITIVE, (WorldLayer.SEMANTIC,), "Canonical identifiable thing.", True),
    CanonicalConcept("Event", ConceptLayer.PRIMITIVE, (WorldLayer.SEMANTIC,), "Occurrence associated with a context."),
    CanonicalConcept("State", ConceptLayer.PRIMITIVE, (WorldLayer.SEMANTIC,), "Condition or configuration that holds."),
    CanonicalConcept("Observation", ConceptLayer.PRIMITIVE, (WorldLayer.INFORMATION,), "Assertion about something observed."),
    CanonicalConcept("Time", ConceptLayer.PRIMITIVE, (WorldLayer.SEMANTIC,), "Temporal semantics; not a required entity for an instant."),
    CanonicalConcept("Actor", ConceptLayer.CORE, (WorldLayer.PHYSICAL, WorldLayer.DECISION), "Participant capable of roles or decisions."),
    CanonicalConcept("Organization", ConceptLayer.CORE, (WorldLayer.PHYSICAL, WorldLayer.DECISION), "Organizational actor."),
    CanonicalConcept("Location", ConceptLayer.CORE, (WorldLayer.PHYSICAL,), "Geographic or logical place."),
    CanonicalConcept("Node", ConceptLayer.CORE, (WorldLayer.PHYSICAL,), "Operational role in a supply-chain network."),
    CanonicalConcept("Product", ConceptLayer.CORE, (WorldLayer.PHYSICAL,), "Intended output or sellable supply-chain item."),
    CanonicalConcept("Material", ConceptLayer.CORE, (WorldLayer.PHYSICAL,), "Input or component used by transformation."),
    CanonicalConcept("Resource", ConceptLayer.CORE, (WorldLayer.PHYSICAL,), "Capacity-bearing means used by operations."),
    CanonicalConcept("Inventory", ConceptLayer.CORE, (WorldLayer.PHYSICAL,), "Stock position in an item/context/time."),
    CanonicalConcept("Demand", ConceptLayer.CORE, (WorldLayer.INFORMATION,), "Requirement or expected need."),
    CanonicalConcept("Order", ConceptLayer.CORE, (WorldLayer.INFORMATION,), "Business request or transaction."),
    CanonicalConcept("Supply", ConceptLayer.CORE, (WorldLayer.PHYSICAL, WorldLayer.INFORMATION), "Provision or availability of supply-chain capability."),
    CanonicalConcept("Capacity", ConceptLayer.CORE, (WorldLayer.PHYSICAL,), "Available or usable capability over a scope and period."),
    CanonicalConcept("Flow", ConceptLayer.CORE, (WorldLayer.PHYSICAL,), "Movement or transformation through the supply chain."),
    CanonicalConcept("Fulfillment", ConceptLayer.CORE, (WorldLayer.PHYSICAL, WorldLayer.INFORMATION), "Satisfaction of demand or order requirements."),
    CanonicalConcept("Plan", ConceptLayer.CORE, (WorldLayer.DECISION,), "Intended future configuration or action set."),
    CanonicalConcept("Schedule", ConceptLayer.CORE, (WorldLayer.DECISION,), "Time-positioned plan or activity commitment."),
    CanonicalConcept("Commitment", ConceptLayer.CORE, (WorldLayer.DECISION,), "Explicit promise or obligation."),
    CanonicalConcept("Objective", ConceptLayer.CORE, (WorldLayer.DECISION,), "Desired outcome or optimization direction."),
    CanonicalConcept("Constraint", ConceptLayer.CORE, (WorldLayer.DECISION,), "Boundary limiting feasible decisions or actions."),
    CanonicalConcept("Policy", ConceptLayer.CORE, (WorldLayer.DECISION,), "Governing decision rule or preference structure."),
    CanonicalConcept("Decision", ConceptLayer.CORE, (WorldLayer.DECISION,), "Selected course of action."),
    CanonicalConcept("Action", ConceptLayer.CORE, (WorldLayer.PHYSICAL, WorldLayer.DECISION), "Executed intervention intended to change the world."),
    CanonicalConcept("Outcome", ConceptLayer.CORE, (WorldLayer.SEMANTIC,), "Result associated with action, decision, or context."),
    CanonicalConcept("Measurement", ConceptLayer.CORE, (WorldLayer.INFORMATION,), "Measured value with unit, method, and context."),
    CanonicalConcept("MetricDefinition", ConceptLayer.CORE, (WorldLayer.INFORMATION,), "Meaning and calculation definition of a metric."),
    CanonicalConcept("MetricValue", ConceptLayer.CORE, (WorldLayer.INFORMATION,), "Evaluated value of a MetricDefinition in context."),
    CanonicalConcept("KPI", ConceptLayer.DERIVED, (WorldLayer.INFORMATION, WorldLayer.DECISION), "Governed selection of one or more metrics for an objective or decision context."),
    CanonicalConcept("PerformanceAssessment", ConceptLayer.DERIVED, (WorldLayer.INFORMATION, WorldLayer.DECISION), "Contextual assessment against a reference."),
    CanonicalConcept("Variance", ConceptLayer.DERIVED, (WorldLayer.INFORMATION,), "Defined difference between comparable values."),
    CanonicalConcept("RiskScore", ConceptLayer.DERIVED, (WorldLayer.INFORMATION, WorldLayer.DECISION), "Derived risk representation."),
    CanonicalConcept("Identity", ConceptLayer.CONTEXTUAL, (WorldLayer.SEMANTIC,), "Canonical identity and source-reference context."),
    CanonicalConcept("Provenance", ConceptLayer.CONTEXTUAL, (WorldLayer.SEMANTIC,), "Origin and derivation context."),
    CanonicalConcept("Evidence", ConceptLayer.CONTEXTUAL, (WorldLayer.SEMANTIC,), "Evidence supporting an assertion, derivation, or assessment."),
    CanonicalConcept("Scenario", ConceptLayer.CONTEXTUAL, (WorldLayer.SEMANTIC,), "Alternative contextual world or assumption set."),
    CanonicalConcept("UnitOfMeasure", ConceptLayer.CONTEXTUAL, (WorldLayer.SEMANTIC,), "Measurement dimensional context."),
    CanonicalConcept("Target", ConceptLayer.CONTEXTUAL, (WorldLayer.DECISION,), "Desired or governed reference value/range."),
    CanonicalConcept("Threshold", ConceptLayer.CONTEXTUAL, (WorldLayer.DECISION,), "Boundary affecting status or rule evaluation."),
)


CANONICAL_RELATIONSHIPS: tuple[RelationshipSignature, ...] = (
    RelationshipSignature("contains", "Entity", "Entity", RelationshipCategory.STRUCTURAL),
    RelationshipSignature("part_of", "Entity", "Entity", RelationshipCategory.STRUCTURAL),
    RelationshipSignature("located_at", "Entity", "Location", RelationshipCategory.STRUCTURAL),
    RelationshipSignature("plays_role", "Actor", "Entity", RelationshipCategory.PARTICIPATION),
    RelationshipSignature("places", "Actor", "Order", RelationshipCategory.PARTICIPATION),
    RelationshipSignature("receives", "Actor", "Entity", RelationshipCategory.PARTICIPATION),
    RelationshipSignature("executes", "Actor", "Action", RelationshipCategory.PARTICIPATION),
    RelationshipSignature("moves_through", "Flow", "Node", RelationshipCategory.FLOW),
    RelationshipSignature("flows_to", "Flow", "Node", RelationshipCategory.FLOW),
    RelationshipSignature("supplies", "Actor", "Supply", RelationshipCategory.FLOW),
    RelationshipSignature("consumes", "Flow", "Material", RelationshipCategory.FLOW),
    RelationshipSignature("produces", "Flow", "Product", RelationshipCategory.TRANSFORMATION),
    RelationshipSignature("transforms", "Flow", "Product", RelationshipCategory.TRANSFORMATION),
    RelationshipSignature("fulfills", "Fulfillment", "Demand", RelationshipCategory.FULFILLMENT),
    RelationshipSignature("allocated_to", "Supply", "Demand", RelationshipCategory.FULFILLMENT),
    RelationshipSignature("reserved_for", "Supply", "Demand", RelationshipCategory.FULFILLMENT),
    RelationshipSignature("planned_for", "Plan", "Entity", RelationshipCategory.PLANNING),
    RelationshipSignature("scheduled_for", "Schedule", "Entity", RelationshipCategory.PLANNING),
    RelationshipSignature("committed_to", "Commitment", "Entity", RelationshipCategory.COMMITMENT),
    RelationshipSignature("results_in", "Action", "Outcome", RelationshipCategory.LIFECYCLE),
    RelationshipSignature("has_objective", "Decision", "Objective", RelationshipCategory.GOVERNANCE),
    RelationshipSignature("constrained_by", "Decision", "Constraint", RelationshipCategory.GOVERNANCE),
    RelationshipSignature("governed_by", "Decision", "Policy", RelationshipCategory.GOVERNANCE),
    RelationshipSignature("considers", "Decision", "Entity", RelationshipCategory.DECISION),
    RelationshipSignature("selects", "Decision", "Entity", RelationshipCategory.DECISION),
    RelationshipSignature("observes", "Observation", "Entity", RelationshipCategory.EPISTEMIC),
    RelationshipSignature("derived_from", "Entity", "Entity", RelationshipCategory.DERIVATION),
    RelationshipSignature("evaluated_by", "PerformanceAssessment", "MetricDefinition", RelationshipCategory.EVALUATION),
    RelationshipSignature("supported_by", "Entity", "Evidence", RelationshipCategory.PROVENANCE),
    RelationshipSignature("causes", "Entity", "Entity", RelationshipCategory.CAUSAL),
    RelationshipSignature("affects", "Entity", "Entity", RelationshipCategory.CAUSAL),
    RelationshipSignature("depends_on", "Entity", "Entity", RelationshipCategory.DEPENDENCY),
)


def concepts_by_layer(layer: ConceptLayer) -> tuple[CanonicalConcept, ...]:
    return tuple(concept for concept in CANONICAL_CONCEPTS if concept.layer == layer)


def concept_names() -> frozenset[str]:
    return frozenset(concept.name for concept in CANONICAL_CONCEPTS)


def relationship_predicates() -> frozenset[str]:
    return frozenset(relation.predicate for relation in CANONICAL_RELATIONSHIPS)


def get_concept(name: str) -> CanonicalConcept:
    for concept in CANONICAL_CONCEPTS:
        if concept.name == name:
            return concept
    raise KeyError(f"unknown canonical concept: {name}")
