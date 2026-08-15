# S257 — M7 Enterprise Attribute Mapping Contract

## Purpose

Define a safe mapping boundary from an enterprise source field to an existing canonical attribute. S257 maps **attribute meaning**, not merely field names or values.

## Directional boundary

```text
Enterprise Field
      ↓
Source Value + Source Metadata
      ↓
Attribute Mapping Decision
      ↓
Canonical Attribute
      ↓
(optional) Explicit Value Transformation
```

The mapping MUST remain one-way from enterprise representation to canonical semantics.

## Mapping record

Each attribute mapping MUST preserve at least:

- `source_system`
- `source_entity_type`
- `source_entity_id`
- `source_field`
- `source_value`
- `canonical_entity_id` when applicable
- `canonical_attribute`
- `mapping_status`
- `mapping_confidence`
- `provenance`
- `transformation` when a value transformation is explicitly defined
- `canonical_mutation=false`

## Mapping status

- `mapped`: source field meaning is sufficiently evidenced to correspond to an existing canonical attribute.
- `ambiguous`: more than one canonical attribute or interpretation remains plausible; no canonical attribute fact is asserted.
- `unmappable`: the existing canonical model has no justified target attribute.
- `rejected`: the source field is intentionally excluded, such as a vendor-only classification or UI/control field.

## Field name is not semantics

A syntactically similar field name MUST NOT be treated as sufficient evidence. For example, an enterprise field named `lead_time`, `LT`, or `transit_days` does not automatically establish the Canonical Lead Time concept. Source definition, unit, scope, temporal meaning, calculation method, and provenance may be required to establish semantic equivalence.

## Value transformation

A transformation MAY normalize representation without changing semantic meaning, for example:

- unit conversion when source and target units are explicitly known;
- controlled-code translation when the source and target code systems have an evidenced equivalence;
- datatype normalization.

A transformation MUST NOT invent business meaning. A calculation that introduces derived business semantics MUST remain a derived artifact rather than being silently promoted to a canonical fact.

## Attribute confidence vs fact confidence

`mapping_confidence` expresses confidence that the source field represents the selected canonical attribute. It MUST NOT be interpreted as confidence that the source value itself is true, current, complete, or authoritative.

## Provenance

The mapping retains source provenance so that a downstream consumer can explain:

```text
Canonical Attribute
    ← mapping decision
Enterprise Field
    ← source record
Source System / Version / Timestamp
```

Provenance supports explainability; it does not convert source representation into canonical truth by itself.

## Vendor isolation

Vendor-specific field names, data types, codes, flags, and classifications remain source representation. They MUST NOT become canonical attributes or predicates merely because an adapter encounters them.

## Semantic gaps

An ambiguous or unmappable attribute MUST be classified as a semantic gap. The adapter MUST NOT create a new canonical attribute automatically to accommodate an enterprise field.

## Canonical graph safety

Attribute mapping is read-only with respect to canonical ontology structure and graph semantics. S257 MUST NOT:

- create canonical entity types;
- create canonical attributes;
- create canonical predicates;
- mutate canonical facts;
- infer facts from mapping confidence alone.

In particular, the adapter MUST NOT create or mutate canonical facts as a side effect of attribute mapping. Attribute mapping alone is never sufficient evidence for a canonical fact assertion.

## Non-goals

S257 does not define predicate/relation mapping, vendor connectors, automatic ontology learning, or automatic canonical-fact generation.
