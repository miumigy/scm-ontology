# S115 — Canonical Identifier / Reference Model

S115 consolidates the identity semantics of S105 into a canonical model that can later be serialized by S116.

## 1. Scope

```text
Entity
  ↑
Identifier Assignment
  ↑
Identifier
  ├─ Namespace
  └─ Issuer
```

References connect information to canonical entities without making an identifier itself the entity.

## 2. Identifier versus identity

An `Identifier` is a contextual reference token. `Identity` is the semantic continuity of the Entity.

Therefore:

```text
same lexical value ≠ same Entity
different lexical value ≠ different Entity
identifier change ≠ necessarily identity change
```

Interpretation requires at least the relevant namespace and, where material, issuer and temporal context.

## 3. Identifier namespace

A namespace defines the context in which identifier values are interpreted.

Examples:

```text
ERP-A/customer
ERP-B/customer
WMS/site
TMS/shipment
```

The raw value `12345` must not be promoted to a globally canonical identity merely because it is unique in one source.

## 4. Identifier assignment

An `IdentifierAssignment` connects an Identifier to an Entity reference and may carry validity and source context.

```text
Identifier
   ↓ assigned-to
Entity
```

Assignments are temporal. An expired identifier remains useful for historical reconstruction.

## 5. Issuer

The issuer is the authority or system responsible for assigning or asserting an identifier. Namespace and issuer may coincide in simple systems, but they are not semantically identical.

## 6. Alias

An Alias is an alternate name or representation of an Entity. It is not automatically a formally issued identifier.

```text
Entity E1
 ├─ Identifier: ERP-A / 12345
 └─ Alias: "Acme"
```

Lexical similarity does not establish identity.

## 7. Canonical reference

A `CanonicalReference` points to a canonical target while preserving the status of the resolution.

```text
Reference
 ├─ target
 ├─ resolution status
 ├─ confidence (optional)
 └─ provenance (optional)
```

A probable or unresolved reference must not be interpreted as a confirmed identity.

## 8. Entity-resolution assertion

An `IdentityResolutionAssertion` records an explicit determination about two references.

Statuses are:

- confirmed
- probable
- possible
- unresolved
- contradicted

This is an epistemic assertion, not an intrinsic property of either Identifier.

Matching method, confidence, validity, and provenance may be retained without prescribing a universal matching algorithm.

## 9. Confidence

Confidence follows S103 epistemic semantics. It does not transform an uncertain match into a fact.

```text
status = probable
confidence = 0.92
```

is materially different from:

```text
status = confirmed
```

## 10. Temporal identity

Identifier validity and resolution validity are temporal.

```text
Identifier I1
  valid: 2024–2025

Identifier I2
  valid: 2025–

Entity E1
  identity continuity preserved
```

Historical source references must remain reconstructable even when current mappings change.

## 11. Provenance

S104 provenance remains authoritative for source/evidence semantics. S115 only provides hooks such as `source_ref` and `provenance_ref`; it does not duplicate the provenance model.

Likewise, S103 remains authoritative for uncertainty and confidence semantics.

## 12. Reference versus relationship

A reference answers:

> Which canonical target does this value refer to?

A relationship answers:

> What semantic relationship exists between two concepts?

References may participate in relationships but should not be collapsed into generic relationship predicates.

## 13. Historical preservation

Never rewrite a historical source reference solely because a later entity-resolution decision changes.

```text
Source Record R1
  2025 → unresolved
  2026 → probable E1
  2027 → confirmed E1
```

The resolution history itself is semantic data.

## 14. Non-goals

S115 does not define:

- a universal UUID policy;
- database primary keys;
- an MDM product architecture;
- a universal entity-resolution algorithm;
- a global master-data authority;
- identifier serialization;
- RDF/JSON-LD/JSON Schema/SQL representation.

Those concerns belong to later implementation layers.

## 15. S115 exit criteria

S115 is complete when:

- identifiers are explicitly contextual;
- namespace and issuer are distinguishable;
- identifier assignment is separate from identity;
- temporal validity is representable;
- aliases are distinct from formal identifiers;
- references preserve resolution status;
- uncertainty and provenance remain delegated to S103/S104;
- historical resolution is reconstructable;
- serialization remains deferred to S116.
