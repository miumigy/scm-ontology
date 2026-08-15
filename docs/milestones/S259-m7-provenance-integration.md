# S259 — M7 Provenance Integration Contract

## Purpose

Make provenance a first-class, preserved part of enterprise canonicalization without treating provenance as canonical truth.

## Provenance boundary

```text
Enterprise Representation
        ↓
 Mapping Decision
        ↓
 Provenance Record
        ↓
Canonicalization Result
```

Every canonicalization result MUST retain enough provenance to answer:

> Which enterprise representation caused this mapping decision, under which mapping context, and when?

## Minimum provenance record

A provenance record SHOULD preserve, where available:

- `source_system`
- `source_dataset`
- `source_record_id`
- `source_field_or_relation`
- `source_entity_id`
- `source_snapshot_or_version`
- `observed_at`
- `ingested_at`
- `adapter_version`
- `mapping_rule_id`
- `mapping_decision_id`

The exact identifiers are source-specific; the canonicalization layer MUST NOT reinterpret a vendor identifier as a canonical semantic identifier merely because it is retained in provenance.

## Provenance is not truth

Provenance establishes lineage of a representation or mapping decision. It does NOT establish that the represented business fact is true, current, complete, authoritative, or approved.

Therefore:

- provenance confidence MUST NOT be treated as fact confidence;
- mapping confidence MUST NOT be treated as fact confidence;
- source-system authority MUST NOT be inferred merely from source-system identity;
- provenance MUST NOT silently promote Evidence into a Canonical Fact.

## Preservation invariant

Canonicalization MUST preserve provenance across Entity, Attribute, and Predicate mapping results. A downstream canonical graph or reasoning layer MUST be able to distinguish:

1. canonical semantic identity;
2. enterprise source representation;
3. mapping decision;
4. provenance/evidence lineage.

## Transformation lineage

If a source value is normalized or transformed before mapping, the provenance record MUST retain the original representation reference and the transformation context. A transformation MUST NOT erase the source lineage.

For example:

```text
ERP field value
      ↓
unit normalization
      ↓
canonical attribute value
```

The normalized value may be canonicalized, but its source representation and transformation context remain traceable.

## Versioning and temporal scope

When source snapshots, effective dates, or adapter versions are available, provenance SHOULD preserve them. A later source observation MUST NOT overwrite the lineage of an earlier mapping decision without retaining version history.

## Read-only invariant

Provenance integration is metadata preservation, not graph mutation. S259 MUST NOT:

- create a new canonical entity, attribute, or predicate;
- mutate canonical facts;
- infer a canonical fact from provenance alone;
- rewrite provenance to conceal an ambiguous or rejected mapping;
- replace an existing source lineage merely because another source appears more convenient.

The contract explicitly states: **MUST NOT mutate canonical facts**.

## Semantic gaps

Provenance MUST be retained for `mapped`, `ambiguous`, `unmappable`, and `rejected` mapping decisions whenever a source representation exists. An ambiguous or unmappable result is still valuable lineage and MUST NOT be discarded merely because canonicalization did not succeed.

## Non-goals

S259 does not define vendor connectors, evidence scoring, automatic ontology learning, canonical fact ingestion, or graph mutation.
