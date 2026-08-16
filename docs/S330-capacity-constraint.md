# S330 — Canonical Capacity Constraint

## Purpose

S330 is a Phase 4 business-question vertical slice that compares already-canonical capacity facts with explicit capacity requirements for an exact resource/unit scope.

## Contract

`headroom = capacity - required`

`utilization = required / capacity` when capacity is positive. When capacity is zero, utilization is explicitly `null` because the ratio is undefined.

`feasible = required <= capacity`

An infeasible result is an observed constraint state, not a recommendation to add capacity, reallocate work, expedite, outsource, or change a plan.

## Semantic boundary

S330 MUST NOT:

- infer resource relationships;
- perform identity resolution;
- allocate demand or supply;
- optimize production or transport;
- recommend mitigation;
- mutate Canonical Truth or graph storage;
- manufacture evidence or provenance.

Capacity and requirement facts, including lineage identifiers, are caller-supplied canonical facts.

## Scope

The aggregation key is exactly `(resource_id, unit)`. S330 does not silently combine different units or resources.

## Result

The runtime emits `contract_version: S330.1` and deterministic UTF-8 JSON. Evidence and provenance identifiers are sorted and preserved in the derived result.
