# S318 — Constraint-aware Supply Chain Reasoning

S318 evaluates temporal semantic paths against explicit operational constraints.

## Supported constraints

- `max_total_lead_time_days`: sum of explicit `lead_time_days` qualifiers must not exceed the limit.
- `min_total_capacity`: the path bottleneck, defined as the minimum explicit `capacity` qualifier, must meet the limit.

## Safety contract

Constraint reasoning is deliberately conservative:

- missing qualifier data causes the relevant check to fail;
- values are never inferred from adjacent nodes, predicates, or defaults;
- the CanonicalGraph is read-only;
- feasibility is not optimization;
- feasibility is not a commitment to execute a plan.

This establishes a clean boundary for future planning integration: the ontology runtime can answer whether an explicitly represented path satisfies constraints, while a planning engine remains responsible for allocation, optimization, and execution decisions.
