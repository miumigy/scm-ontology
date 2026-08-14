# S87 — Observation Subject Semantics

S87 defines the semantic boundary of `subject_id` in the canonical Observation primitive and its relationship to domain entities and source-record identities.

## Canonical decision

`subject_id` identifies the domain entity or object that the Observation is about.

```text
Observation
├─ observation_id
├─ observed_at
└─ subject_id   ← observed subject
```

`subject_id` is a reference to a domain object; it is not a source-system record identifier and does not imply a new universal `Subject` entity type.

## Subject is a role, not a universal primitive

"Subject" describes the role played by an object in an Observation:

```text
Observation
      │
      │ observes
      ▼
Domain Object
```

The observed object may be an existing domain entity such as:

```text
Supplier
Plant
Warehouse
Store
SKU
Material
Shipment
Vehicle
Order
Customer
```

S87 does not require all such objects to inherit from a common canonical `Subject` primitive.

## Entity identity boundary

`subject_id` refers to the identity of the observed domain object.

It is distinct from source-record identity:

```text
subject_id
    ≠ source_record_id
    ≠ observation_id
```

For example:

```text
subject_id       = WH-A
source_record_id = WMS:INV-123
observation_id   = OBS-001
```

These three identifiers answer different questions:

```text
What object was observed?
    → subject_id

Which Observation instance is this?
    → observation_id

Which source record supplied or represented the information?
    → source_record_id
```

## Subject versus observed semantic content

The subject is not necessarily the phenomenon or value being observed.

For example:

```text
subject    = Warehouse-A
phenomenon = inventory_level
value      = 120
unit       = pieces
```

Here Warehouse-A is the subject; inventory level is the domain semantic describing what is observed; 120 pieces is the interpreted value.

S81 and S82 keep phenomenon and value outside the canonical Observation primitive, and S87 preserves that boundary.

## Composite and contextual subjects

An Observation may concern a domain object whose identity is already represented elsewhere in the ontology.

For example:

```text
Observation
  subject = Shipment-123
```

or:

```text
Observation
  subject = Warehouse-A
```

If the domain requires a contextual object such as "inventory-at-Warehouse-A" or "temperature-of-Sensor-17", that contextual object should be modeled according to the relevant domain semantics rather than forcing `subject_id` to encode a compound natural key.

## Source-system mapping

A source system may use a different identifier for the same domain object:

```text
WMS warehouse code = 0017
SCM ontology entity = WH-A
```

The mapping between source identifiers and canonical domain identities belongs to the entity-resolution / integration layer.

S87 does not define an automatic identifier-matching algorithm.

## Multiple subjects

The canonical Observation primitive has a single `subject_id` reference. An observation involving multiple domain objects should use an explicit domain relationship, contextual object, or multiple Observation instances as appropriate.

S87 does not introduce `subject_ids[]` into the core Observation contract.

## Relationship to provenance and derivation

S84 and S85 establish that source records and derivation inputs are separate from Observation identity. S87 adds that they are also separate from the observed subject.

```text
Source Record
      │ provenance
      ▼
Observation ── observes ──→ Subject

Observation O1 ── derivation ──→ Observation O2
```

A source record can describe an observation about a subject without becoming that subject.

## Non-goals

S87 does not define a universal Subject superclass, entity-resolution algorithm, source-ID registry, multi-subject Observation model, compound-key convention, or domain-specific entity taxonomy.
