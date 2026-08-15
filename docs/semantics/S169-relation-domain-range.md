# S169 — Relation Domain / Range Constraints

S169 adds a lightweight semantic constraint layer for canonical relations.

## Purpose

A canonical predicate should not be treated as universally applicable to every entity. Domain/range constraints provide machine-readable expectations for graph validation and mapping.

Examples:

```text
located_at(PhysicalEntity, Location|Node)
fulfills(Supply|Order|Execution, Demand|Order|Commitment)
flows_through(Flow, Node|Location|Lane|Route)
measured_by(Entity|Event|State, Measurement|Metric)
```

## Important boundary

These are **typing constraints**, not runtime proof of truth.

A source record may fail a constraint because of mapping error, an extension concept, or incomplete ontology coverage. Such a failure must not silently become a semantic assertion.

S169 does not introduce automatic coercion, subclass reasoning, cardinality, or inference.
