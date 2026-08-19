# S336 — Reference SCM OS Flow

S336 composes existing canonical boundaries into one minimal end-to-end reference flow.

```text
Source Record
  ↓ S335 governed canonicalization
Canonical Record
  ↓ explicit observation
S333 Decision Context
  ↓ proposal only
S334 Decision Proposal
  ↓
Deterministic Reference Output
```

## Contract

- Canonicalization is explicit and fail-closed.
- A canonicalization failure prevents downstream context/proposal creation.
- The flow composes existing S335, S333, and S334 contracts; it does not redefine them.
- Decision Proposal is not approval and does not execute an action.
- Evidence and provenance identifiers are carried through unchanged.
- JSON is deterministic and preserves UTF-8 characters.
- No graph mutation, identity resolution, optimization, or execution occurs.

## Purpose

This is a reference integration boundary for future ERP/WMS/TMS adapters and SCM OS reasoning. Enterprise adapters can replace the fixture input while preserving the downstream canonical contracts.
