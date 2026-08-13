# SCM Simulation Causal Contract v0.1

## Purpose

S4 defines deterministic event-to-event causal propagation inside the simulation runtime.

The runtime does not invent new canonical ontology semantics. A `CausalRule` explicitly maps one event type to another derived event type.

## Model

```text
Event
  ↓
CausalRule
  ↓
Derived Event
  ↓
EventProvenance
```

A derived event carries:

- `causedByEventId`
- `ruleId`
- `causalDepth`

These fields provide deterministic causal lineage.

## Rules

A rule is identified by `ruleId` and contains:

```text
sourceEventType
 targetEventType
```

Propagation is rejected when:

1. the source event type does not match the rule;
2. more than one rule matches the source event type;
3. the same rule is already present in the event lineage.

The adapter therefore fails explicitly instead of choosing an arbitrary causal path.

## Example

```text
SUPPLIER_DELAY
      │
      │ RULE-001
      ▼
MATERIAL_SHORTAGE_RISK
```

The derived event records:

```text
causedByEventId = EVT-001
ruleId          = RULE-001
causalDepth     = 1
```

## Determinism

Given the same source event, causal rule, and derived event id, the resulting event and provenance are identical.

No random value, wall-clock value, or external runtime state is used to determine causal propagation.

## Scope

S4 currently covers event-to-event causal propagation only.

It does not yet calculate inventory depletion, production quantities, shipment dates, KPI impacts, risk scores, optimization results, or Monte Carlo distributions.
