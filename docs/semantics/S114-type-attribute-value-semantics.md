# S114 — Type / Attribute / Value Semantics

S114 defines how canonical concepts carry semantic values without prematurely coupling the ontology to JSON, SQL, RDF, Neo4j, or a vendor schema.

## 1. Scope

S113 established canonical concepts and relationship signatures. S114 establishes the next contract:

```text
Canonical Concept
      ↓
Attribute
      ↓
Value Type
      ↓
Value
```

An attribute is not merely a database column. A value type is not merely a programming-language datatype.

## 2. Value kinds

The core value-kind vocabulary is intentionally small:

- `scalar` — atomic value with a canonical scalar datatype.
- `quantity` — numeric magnitude whose meaning requires unit semantics.
- `code` — source/domain controlled symbolic value; the code system is contextual.
- `reference` — reference to another canonical concept/entity.
- `enumeration` — value selected from a governed finite vocabulary.
- `interval` — value representing an ordered temporal or semantic interval.
- `range` — bounded or partially bounded value domain.
- `collection` — multiple values of a common or governed type.
- `structured` — composed value with its own semantic structure.

These are semantic categories, not storage formats.

## 3. Scalar types

The canonical scalar set is:

- string
- boolean
- integer
- decimal
- date
- datetime
- duration

Do not introduce `float`, database-specific numeric types, or vendor-specific serialization types into Core merely for implementation convenience.

## 4. Quantity semantics

A quantity is not equivalent to a naked decimal.

```text
Quantity
 ├─ magnitude
 └─ unit
```

Examples:

- 100 kg
- 12 pallets
- 500 pieces
- 2.5 hours

The same numeric value with different units is not semantically equivalent. Unit conversion belongs to a later measurement/unit contract, while S114 requires unit semantics to be present.

## 5. Code vs Enumeration

`Code` represents a symbolic value whose vocabulary may originate in a source or governed external code system.

`Enumeration` represents a finite, explicitly governed value set.

Do not assume that two identical strings are equivalent merely because their lexical values match.

```text
Source code "01"
      ≠ automatically
Canonical enumeration member "01"
```

Mapping and provenance preserve the source vocabulary.

## 6. Reference semantics

A reference expresses a semantic link to another canonical concept.

```text
Inventory
   └─ item → Item
```

A reference is not the same as copying an entity's attributes into the owner. Canonical references should preserve identity and allow graph traversal.

## 7. Attribute roles

Attributes are classified by semantic role:

- `identity` — participates in canonical identity.
- `descriptive` — describes a concept without defining identity.
- `qualifier` — narrows or contextualizes meaning.
- `measure` — carries a measured/quantitative value.
- `temporal` — carries temporal qualification.
- `epistemic` — describes knowledge status, uncertainty, validity, or confidence.
- `provenance` — identifies origin/evidence/source context.
- `derivation` — describes how a value was derived.
- `governance` — carries ownership, authority, policy, or control semantics.
- `reference` — points to another canonical concept.

The role must not be inferred solely from the attribute name.

## 8. Cardinality

Canonical cardinalities are:

- `1`
- `0..1`
- `0..*`
- `1..*`

Cardinality is semantic. A source database `NOT NULL` constraint does not automatically mean that a value is semantically mandatory in the Canonical Model.

## 9. Planned / actual / observed boundary

Type semantics must not collapse epistemic or temporal status into a datatype.

For example:

```text
planned_delivery_date : Date
actual_delivery_date  : Date
observed_at            : DateTime
predicted_delivery     : Date
```

These may share scalar datatypes while remaining different semantic attributes because their roles and provenance differ.

Likewise:

```text
quantity = 100
```

does not by itself tell us whether 100 is requested, promised, allocated, fulfilled, actual, estimated, or predicted. That distinction belongs to the semantic contract, not the numeric datatype.

## 10. Primitive vs derived values

A datatype does not make a concept primitive.

For example:

- `Inventory.quantity` can be a core value.
- `DaysOfSupply` is derived even if represented as a decimal.
- `KPI.score` is derived even if represented as an integer.
- `RiskScore` is derived even if represented as a decimal.

Derived status follows semantic dependency, not physical representation.

## 11. Modeling rules

1. Do not make storage types part of the Canonical Model.
2. Do not represent quantities as naked numbers without unit semantics.
3. Do not confuse code values with canonical identities.
4. Do not infer semantic equivalence from lexical equality.
5. Do not copy references into descriptive attributes when graph identity matters.
6. Do not encode Planned / Actual / Predicted / Observed solely through datatypes.
7. Do not promote derived metrics to primitive value semantics.
8. Preserve provenance when values originate in source systems.
9. Treat cardinality as a semantic constraint, not merely a database constraint.
10. Keep value semantics independent from serialization; S116 will define machine-readable ontology serialization.

## 12. S114 exit criteria

S114 is complete when:

- value kinds are explicit;
- scalar datatypes are canonical and implementation-neutral;
- quantities require unit semantics;
- references are distinguished from copied values;
- attributes have explicit semantic roles;
- cardinality is machine-readable;
- planned/actual/epistemic distinctions remain independent from datatype representation.
