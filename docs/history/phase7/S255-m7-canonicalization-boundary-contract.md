# S255 — M7 Canonicalization Boundary Contract

## Purpose

Define the semantic contract between enterprise representations and the canonical SCM model before implementing entity, attribute, or predicate mappings.

S255 is a boundary-definition slice. It does not add canonical ontology concepts and does not implement a vendor connector.

## Directional architecture

```text
Enterprise Representation
        ↓
     Adapter
        ↓
Canonicalization Contract
        ↓
Canonical Semantics
        ↓
Canonical SCM Graph
```

The boundary is strictly directional:

**Enterprise Representation → Canonical Semantics**

Canonical semantics must not be redefined from the structure, naming, codes, classifications, or defaults of an enterprise system.

## Canonicalization record contract

Every adapter mapping decision must be representable with the following semantic components:

| Component | Requirement |
|---|---|
| enterprise_representation | Required source-system representation, including source-system identity and source location/field context where available |
| canonical_target | Required only for an accepted mapping; identifies an existing canonical entity, attribute, or predicate |
| mapping_status | Required decision state: `mapped`, `ambiguous`, `unmappable`, or `rejected` |
| mapping_confidence | Required for accepted or ambiguous decisions; confidence is mapping quality metadata, not canonical truth |
| provenance | Required source/evidence lineage for the mapping decision |
| semantic_gap | Required when the source cannot be safely represented canonically; classifies the gap rather than silently extending the ontology |
| canonical_mutation | Always `false` in the adapter contract; canonical ontology/graph mutation is outside canonicalization |

## Mapping decision rules

### 1. Entity mapping

An enterprise entity may map to a canonical entity only when the enterprise representation is semantically compatible with an existing canonical concept.

Example:

```text
SAP Material Master
        ↓
Adapter
        ↓
Canonical Material
```

The source identifier remains provenance/source-system data. It does not become the canonical meaning of `Material`.

### 2. Attribute mapping

An enterprise field may map to a canonical attribute only when its meaning, scope, unit/representation, and temporal semantics are sufficiently compatible.

A field name alone is insufficient evidence for canonical equivalence.

### 3. Predicate mapping

An enterprise relation may map to an existing canonical predicate only when its source semantics establish the same relationship.

Vendor-specific classifications, codes, status values, or workflow relationships must not be promoted into canonical predicates merely because they are useful in the source system.

Example prohibition:

```text
SAP Material Type = ROH
        ↓
      X
Canonical SCM Predicate
```

`ROH` may remain an enterprise representation or evidence value; it does not define a canonical SCM relationship by itself.

## Decision states

### `mapped`

The adapter has sufficient semantic evidence to produce a canonical representation. The mapping retains provenance and mapping confidence.

### `ambiguous`

Multiple canonical interpretations remain plausible, or the available source context is insufficient to select one safely. No canonical fact is created from the ambiguous mapping.

### `unmappable`

The source representation has no safe existing canonical target. The adapter records the gap instead of inventing a canonical concept.

### `rejected`

The source representation is explicitly incompatible with the requested canonical mapping, including attempts to promote vendor-specific semantics into canonical meaning.

## Semantic Gap boundary

A semantic gap is an adapter outcome, not an automatic ontology-extension request.

At minimum, M7 must distinguish:

- `no_canonical_target` — no existing canonical concept safely represents the source meaning
- `ambiguous_mapping` — more than one canonical interpretation remains plausible
- `vendor_specific_semantics` — meaning depends on source-system/vendor conventions
- `granularity_mismatch` — source and canonical concepts differ in semantic granularity
- `temporal_mismatch` — source and canonical temporal semantics cannot be safely aligned
- `authority_insufficient` — available source/evidence is insufficient to establish the canonical fact

The classification itself does not create a canonical fact.

## Provenance and evidence boundary

Adapter provenance answers **where the mapping came from**. It does not answer **whether the resulting canonical fact is true**.

Therefore:

```text
Enterprise Data
      ↓
Mapping Decision + Provenance
      ↓
Canonical Representation (only if safely mapped)
```

must not be interpreted as:

```text
Enterprise Data
      ↓
Automatic Canonical Truth
```

Existing M6 evidence/provenance contracts remain authoritative for graph assertions and reasoning.

## Read-only and contamination invariants

The adapter/canonicalization layer MUST NOT:

1. mutate the canonical ontology definition;
2. invent a canonical entity, attribute, or predicate because a source field is unmappable;
3. promote planning artifacts to canonical facts;
4. promote vendor classifications to canonical semantics without an independent semantic basis;
5. discard source provenance;
6. treat mapping confidence as fact confidence;
7. use reasoning output to manufacture a missing source mapping;
8. mutate the graph merely to make a downstream business question answerable.

## Acceptance criteria

S255 is complete when:

1. the directional `Enterprise Representation → Canonical Semantics` boundary is explicit;
2. entity, attribute, and predicate mappings are covered by one common contract;
3. provenance and mapping confidence are mandatory metadata;
4. ambiguous and unmappable representations have explicit non-promoting outcomes;
5. semantic gaps are classified without automatic ontology expansion;
6. vendor-specific semantics are isolated from canonical semantics;
7. canonical mutation is explicitly prohibited by the adapter contract;
8. regression tests lock these invariants before S256 begins.

## Next slice

S256 — Entity Mapping will implement the first concrete mapping class while preserving this boundary contract.
