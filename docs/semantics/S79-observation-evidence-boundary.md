# S79 — Observation–Evidence Boundary

S79 defines the semantic boundary between Observation, Evidence, and Claim.

## Canonical layers

```text
Observation
    │
    │ may serve as evidence
    ▼
Evidence
    │
    │ supports / contradicts / corroborates / qualifies
    ▼
Claim
```

These are distinct semantic roles:

- **Observation** represents something observed at a point in time. The current canonical primitive contains `observation_id`, `observed_at`, and `subject_id`.
- **Evidence** represents a reference to something used as epistemic support for a Claim. `EvidenceReference` contains `evidence_id`, `evidence_type`, and an opaque `reference`.
- **Claim** represents an assertion with Subject, Predicate, and Object semantics.

The existing Observation primitive confirms that temporal observation semantics belong to Observation itself, not to Evidence. Evidence independently carries its own identity, type, and opaque reference.

## Observation is not an Evidence subtype

An Observation may be used as or referenced by Evidence, but this does not make Observation a subtype of Evidence and does not collapse the two primitives.

```text
Observation ≠ Evidence ≠ Claim
```

Likewise, `evidence_type = "observation"` is permitted under S78, but it is a classification of the Evidence item; it does not establish type identity with the Observation primitive.

## Semantic chain

A common pattern is:

```text
Observation
  Truck-001 observed_at T
  temperature = 28.4°C
        │
        │ referenced/represented as evidence
        ▼
Evidence
  Sensor Record #123
        │
        │ supports
        ▼
Claim
  Shipment-001 → temperature_above_threshold → true
```

This is a possible semantic chain, not an automatic inference or transformation rule. An Observation does not become Evidence merely because it exists, and Evidence does not become a Claim merely because it is referenced by one.

## Boundaries

```text
Observation
    ≠ measurement value
    ≠ EvidenceReference
    ≠ Claim

Evidence
    ≠ truth
    ≠ source system
    ≠ provenance log

Claim
    ≠ fact
    ≠ Evidence
    ≠ Relationship
```

Evidence can support or contradict a Claim without making the Claim true or false automatically.

## Non-goals

S79 does not introduce inheritance between Observation and Evidence, automatic Observation-to-Evidence conversion, automatic Claim inference, truth resolution, confidence scoring, or a provenance storage model.
