# S82 — Measurement / Value Boundary

S82 defines the semantic boundary between Observation, a measured or observed value, Measurement, Unit, Quantity, and Claim.

## Canonical decision

S82 does **not** add `value`, `unit`, `quantity`, or `measurement` fields to the canonical `Observation` primitive, and it does not introduce a new canonical Measurement or Value primitive.

The current Observation remains:

```text
Observation
├─ observation_id
├─ observed_at
└─ subject_id
```

This follows S80 and S81: Observation is a temporal observation reference, while the concrete interpretation of what was observed and its value belongs to a domain/application semantic layer unless a future cross-domain contract demonstrates a stable canonical need.

## Distinctions

```text
Observation
    = temporal observation reference

Measurement
    = a domain interpretation in which an observation expresses a measurable quantity

Value
    = the value component of such an interpretation

Unit
    = the semantic unit associated with a value when applicable

Quantity
    = value + unit semantics when the domain requires them

Claim
    = semantic assertion
```

These concepts must not be collapsed merely because an application commonly stores them together.

## Example

An application may interpret an observation as:

```text
subject    = Warehouse-A
phenomenon = inventory_level
value      = 120
unit       = pieces
```

This interpretation is valid without requiring the canonical Observation primitive to contain those fields.

Likewise:

```text
subject    = Sensor-17
phenomenon = temperature
value      = 28.4
unit       = °C
```

is a possible measurement interpretation of an Observation, not a redefinition of Observation itself.

## Why Measurement is not canonical yet

A generic Measurement primitive would immediately require decisions about:

- value datatypes and numeric precision;
- units and conversion rules;
- quantities and dimensional analysis;
- qualifiers, ranges, intervals, uncertainty, and significant figures;
- categorical versus numeric values;
- missing, estimated, imputed, or censored values.

Those concerns are real but are not required to preserve the current canonical ontology semantics. Introducing them prematurely would make the core model an implementation/data schema rather than a stable semantic contract.

## Relationship to Claim

A measured value does not become a Claim merely because it has a value.

```text
Observation + interpretation
    → may support a Claim

Observation
    ≠ Claim
```

For example, `temperature = 28.4°C` may support the Claim `temperature_above_threshold = true`, but the measurement and the assertion remain semantically distinct.

## Relationship to Evidence

A measurement interpretation may be represented or referenced as Evidence for a Claim. Evidence remains the epistemic role defined by S69/S76; Measurement remains the content interpretation.

```text
Measurement interpretation
        │
        │ may be referenced as
        ▼
Evidence
        │
        │ supports / contradicts / ...
        ▼
Claim
```

No automatic evidence generation is implied.

## Open extension point

A future canonical Measurement/Quantity model may be introduced if cross-domain requirements demonstrate that the same semantics recur across SCM observations and cannot be adequately expressed by domain/application mappings.

Any such extension must preserve:

```text
Observation ≠ Measurement
Measurement ≠ Value
Value ≠ Unit
Measurement ≠ Claim
```

and must not silently change the meaning of existing Observation identifiers.

## Non-goals

S82 does not define a unit ontology, conversion engine, quantity/dimensional-analysis model, uncertainty model, value datatype registry, automatic measurement extraction, or automatic Claim inference.
