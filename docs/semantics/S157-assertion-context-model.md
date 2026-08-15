# S157 — Canonical Assertion Context Model

S157 connects the S155 instance layer with the S154 cross-cutting semantic context.

## Model

```text
Canonical Relation
       ↓
Assertion Context
       ├─ Epistemic
       ├─ Temporal
       ├─ Provenance
       └─ Qualifiers
```

The relation remains the structural statement. Context describes the circumstances under which that assertion is held.

## Invariants

1. Assertion context identity must match the relation it contextualizes.
2. Temporal, epistemic, and provenance dimensions remain separate; context does not collapse them into one status.
3. No inference or identity resolution occurs during context attachment.
4. Context is storage-neutral and does not impose a graph database representation.

## Example

```text
Material:001 --stored_at--> Site:001
        │
        └── assertion context
             epistemic = observation
             temporal  = observation time / validity
             provenance = WMS source
```

This allows the same canonical relation shape to be retained while preserving *when*, *how known*, and *from where* the assertion originated.

## Non-goals

S157 does not add a new epistemic taxonomy, temporal model, provenance model, or scenario engine. It composes the already-established S154 semantics.
