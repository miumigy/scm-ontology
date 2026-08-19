# S284 — M8 Governed Canonical Application Boundary

## Purpose

Define the explicit application boundary through which an approved resolution decision may be applied to Canonical Graph state.

## Application flow

```text
Approved Decision Record
        ↓
Application Request
        ↓
Governance / Preconditions Check
        ↓
Explicit Canonical Application
        ↓
Application Record
        ↓
Updated Canonical State
```

An Approved Decision Record MUST NOT itself mutate Canonical Graph state.

## Preconditions

Before application, the system MUST verify:

- the referenced Decision Record is Approved;
- the decision has not been superseded or revoked;
- all affected Canonical identities and facts are explicitly identified;
- required provenance and evidence references are present;
- the application scope is explicit;
- the application actor or governing authority is recorded.

## Safety invariants

1. Canonical mutation MUST occur only through an explicit governed application step.
2. Application scope MUST be explicit and bounded.
3. Application MUST be attributable to a recorded actor or authority.
4. The source assertions, evidence, provenance, and Decision Record MUST remain traceable after application.
5. Application MUST NOT silently create a new canonical entity, attribute, or predicate.
6. Application MUST NOT silently overwrite unrelated Canonical Facts.
7. Failed or rejected application attempts MUST remain auditable.
8. Application history MUST be append-only and replayable.
9. Reasoning MUST remain read-only; reasoning output alone MUST NOT authorize application.
10. Vendor-specific semantics MUST NOT be introduced into the Canonical Ontology through application.

## Boundary semantics

The application step is a governed state transition, not an inference step. Mapping success, identity similarity, provenance, evidence, or model confidence alone MUST NOT authorize Canonical mutation.

An application record describes what was explicitly applied, why it was authorized, which decision authorized it, and what Canonical state was affected. It does not replace the underlying provenance or evidence.

## Non-goals

S284 does not implement authorization infrastructure, production graph mutation, automatic conflict resolution, autonomous application, or vendor-specific synchronization connectors.
