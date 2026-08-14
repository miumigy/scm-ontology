"""Canonical semantic primitive registry for SCM Ontology v0.2."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

PrimitiveKind = Literal["entity", "observation", "state", "event", "definition", "context"]

@dataclass(frozen=True)
class SemanticPrimitive:
    name: str
    kind: PrimitiveKind
    definition: str
    non_goals: tuple[str, ...]

CORE_SEMANTIC_PRIMITIVES = (
    SemanticPrimitive("Entity", "entity", "A canonical identifiable thing within the SCM semantic model.", ("Do not encode source records as canonical identity by default.",)),
    SemanticPrimitive("MetricDefinition", "definition", "A definition of what a metric means and how its value is interpreted.", ("Do not equate a metric definition with an observation value.",)),
    SemanticPrimitive("MetricObservation", "observation", "A measured fact for an entity at a timezone-aware instant with provenance.", ("Do not infer State or Event automatically from an observation.",)),
    SemanticPrimitive("CanonicalState", "state", "A condition or configuration that holds for an entity.", ("Do not model an occurrence as a state.",)),
    SemanticPrimitive("CanonicalEvent", "event", "An occurrence associated with an entity at a timezone-aware instant.", ("Do not prescribe event-to-state causality in the core model.",)),
    SemanticPrimitive("Impact", "context", "A canonical representation of an effect or influence.", ("Do not make impact propagation implicit on every relationship.",)),
    SemanticPrimitive("Target", "context", "The canonical object or scope toward which an impact is directed.", ("Do not assume every entity is an impact target without an explicit relation.",)),
    SemanticPrimitive("Provenance", "context", "Reference semantics describing where an observation originates.", ("Do not introduce a mandatory Source entity or authority semantics in Core.",)),
    SemanticPrimitive("Time", "context", "Temporal semantics represented as timezone-aware instants.", ("Do not introduce a redundant Time entity for an instant.",)),
)

def get_core_semantic_primitive(name: str) -> SemanticPrimitive:
    for primitive in CORE_SEMANTIC_PRIMITIVES:
        if primitive.name == name:
            return primitive
    raise KeyError(f"unknown semantic primitive: {name}")
