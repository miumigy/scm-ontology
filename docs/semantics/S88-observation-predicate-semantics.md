# S88 — Observation Predicate Semantics

S88 defines how the semantic meaning of what is observed relates to the canonical Observation primitive.

## Canonical decision

The canonical Observation does **not** add a `predicate`, `property`, or `phenomenon` field.

```text
Observation
├─ observation_id
├─ observed_at
└─ subject_id
```

The semantic interpretation of the observation is supplied by a separate domain semantic layer.

Conceptually:

```text
Observation
      │
      ├── subject ──→ Domain Object
      │
      └── semantic interpretation
               ├── property / phenomenon
               ├── value
               └── unit / measurement semantics
```

## Subject–property–value distinction

For an observation such as:

```text
Warehouse-A
inventory_level
120
pieces
```

these components answer different questions:

```text
subject
  = what domain object is being observed?

property / phenomenon
  = what characteristic or phenomenon is being observed?

value
  = what value is associated with that semantic interpretation?

unit
  = how the value is quantified, when applicable
```

None of these distinctions changes Observation identity.

## Property and phenomenon

S88 intentionally does not declare `property` and `phenomenon` to be universally identical concepts.

A domain may use a phenomenon vocabulary for measurable or observable phenomena, while another domain may use a property vocabulary for characteristics of an entity. The semantic layer may establish their relationship where needed.

The canonical Observation primitive remains agnostic to that vocabulary choice.

## No predicate field in the core

Adding a predicate directly to Observation would turn the primitive into a Subject–Predicate–Object statement and risk conflating Observation with a general semantic assertion.

S88 therefore keeps the distinction:

```text
Observation
    = an observation instance

Property / Phenomenon
    = what is being observed

Claim
    = an assertion that may be supported or challenged
```

A property/phenomenon interpretation may participate in a Claim, but it is not itself a Claim.

## Example

```text
Observation O1
  subject_id  = WH-A
  observed_at = 10:00

Semantic interpretation
  property = inventory_level
  value    = 120
  unit     = pieces
```

This means that O1 is an observation about WH-A at 10:00 whose semantic interpretation concerns inventory level and yields a value of 120 pieces.

The interpretation may be represented by application/domain structures without changing the canonical Observation contract.

## Relationship to Measurement and Value

S82 established the boundary between Observation and measurable value semantics.

S88 preserves that boundary:

```text
Observation
      │
      └── semantic interpretation
              ├── property / phenomenon
              ├── measurement
              └── value / unit
```

A property does not imply that the result is numeric. Some observations may concern qualitative or categorical characteristics.

## Domain expansion

SCM domains may later define canonical properties such as:

```text
inventory_level
capacity
utilization
throughput
lead_time
temperature
```

S88 does not define those domain vocabularies. It only defines where such semantics belong relative to Observation.

## Non-goals

S88 does not define a universal property ontology, RDF-style predicate model, measurement vocabulary, value type system, domain property catalog, or Claim schema.
