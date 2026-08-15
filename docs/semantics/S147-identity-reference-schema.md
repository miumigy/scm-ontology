# S147 — Identity / Reference Schema

S147 promotes the S105 identity and resolution semantics into the machine-readable schema layer.

## Canonical distinction

```text
Identifier
   ≠
Identity
   ≠
Entity Reference
   ≠
Canonical Entity
```

An identifier is a contextual token. An entity reference is a typed assertion about what the token refers to. Resolution is explicit and evidence/provenance-bearing.

## Identifier context

Every identifier is interpreted through its namespace. The same lexical value in two namespaces is not automatically the same entity.

```text
ERP-A / Material / 12345
ERP-B / Material / 12345
          ≠
        Same Entity
```

`IdentifierAssignment` provides the temporal association between an identifier and an entity reference.

## Resolution

Resolution status remains explicit:

- confirmed
- probable
- possible
- unresolved
- contradicted

A confirmed reference requires an explicit canonical entity reference. Unresolved or possible references must never be silently treated as confirmed identity.

## Provenance and confidence

Resolution can retain confidence and provenance. Matching algorithms are outside the ontology; the ontology records the semantic result and its evidence hooks.

## Aliases

An alias is not automatically an identifier with the same semantics. Alias identity remains contextual and temporal.

## Mapping

Enterprise mapping therefore follows:

```text
Source Identifier
      ↓
Identifier Assignment / Resolution Assertion
      ↓
Entity Reference
      ↓
Canonical Entity
```

The source identifier and source-system semantics are retained rather than discarded.

## Temporal semantics

Identifier assignments and resolution assertions may have validity intervals. This permits historical identity reconstruction without rewriting past mappings.

## Non-goals

S147 does not define a matching algorithm, master-data-management product, database key strategy, or vendor-specific identifier format.
