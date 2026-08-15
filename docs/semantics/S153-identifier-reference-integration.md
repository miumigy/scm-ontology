# S153 — Identifier / Reference Integration

S153 promotes the established S105/S147 identity semantics into the integrated schema layer.

## Canonical boundary

```text
Identifier
   ≠
Identity
   ≠
Entity Reference
   ≠
Canonical Entity
```

An identifier is a contextual token. A reference records which entity it is intended to denote. Resolution is an explicit assertion, not an implicit consequence of matching a code.

## Resolution

```text
Source Identifier
      ↓
Resolution Assertion
      ↓
UNRESOLVED / POSSIBLE / PROBABLE / CONFIRMED
      ↓
Canonical Entity Reference
```

A `CONFIRMED` resolution must carry a canonical target. Lower-confidence states may remain unresolved.

## Provenance

Resolution records may carry provenance references and confidence. This preserves the S149 epistemic/provenance boundary: a proposed mapping is not silently promoted to fact.

## Type compatibility

Identifier definitions can declare an expected entity type, but the identifier value itself does not become an entity identity. This keeps source-system identifiers usable across ERP/WMS/TMS mappings without making a source code canonical.

## Non-goals

S153 does not define matching algorithms, fuzzy matching, master-data governance workflows, or a vendor-specific identifier format.
