# S71 — Canonical Claim Object Semantics

## Purpose

Define the minimum canonical distinction between an object that references an entity and an object that carries a literal value.

## Contract

`ClaimObject` has:

- `kind`: `reference` or `value`
- `reference`: an opaque reference when `kind=reference`
- `value`: a literal/application value when `kind=value`

Exactly one semantic form is selected by `kind`.

## Examples

Entity relationship:

```text
Order-001 --supplied_by--> Supplier-A
object = ClaimObject(reference="Supplier-A")
```

Literal assertion:

```text
Shipment-001 --quantity--> 100
object = ClaimObject(value=100)
```

## Boundaries

`ClaimObject` is not an RDF term model, database value schema, URI model, datatype system, or persistence identifier.

A reference remains opaque. URI, UUID, database-key, and dereferencing semantics are outside this contract.

`ClaimObject` also does not decide whether a reference identifies a canonical entity or an external resource; that resolution remains outside the canonical object contract.

## Relationship to Claim

Existing `Claim.object_value` remains backward-compatible. S71 introduces the explicit object semantic primitive without requiring an immediate migration of the Claim constructor.

This milestone therefore distinguishes:

```text
Claim
  ≠ RDF Triple
  ≠ Database Row

ClaimObject
  ≠ RDF term
  ≠ Database column type
```

## Non-goals

S71 does not define:

- datatypes
- URI/IRI syntax
- UUID generation
- entity registry or identity resolution
- literal validation
- units of measure
- language tags
- persistence
- graph serialization
