# S17 — Observation / State / Event Semantic Boundary

## Canonical distinction

- **Observation**: a measured fact about an entity at an observation instant.
- **State**: a condition or configuration that holds for an entity over a period.
- **Event**: an occurrence that happens at a point or over an interval in time.

## Boundary rule

An observation does not automatically become a state or an event. A metric value may provide evidence for reasoning about a state or event, but the ontology must not infer a semantic relationship merely from the presence of an observation.

## Consequence

S17 intentionally introduces no `Observation → State` or `Observation → Event` relationship and no new State/Event entity implementation. Such relationships require an explicit domain semantic contract in a later milestone.
