# S281 — M8 Cross-Enterprise Identity Resolution Fixture

## Purpose

Provide a deterministic fixture showing how two enterprise representations may refer to the same candidate entity without allowing similarity alone to establish Canonical Identity.

## Fixture

```text
Enterprise A                         Enterprise B
Material ID: MAT-001                Material ID: 7A-42
Description: Steel Coil              Description: Steel coil
Supplier Code: SUP-77                Vendor Code: V077
       │                                     │
       └──────────── Identity Evidence ──────┘
                         ↓
               Candidate Identity Match
                         ↓
                Governed Match Decision
                         ↓
               Canonical Material (if approved)
```

The fixture deliberately contains a plausible match, but the fixture itself does not assert that the two source identities are Canonically Identical.

## Required outcomes

The fixture MUST support these outcomes:

- **Matched** — a governed decision explicitly establishes the correspondence.
- **Ambiguous** — evidence is insufficient or competing candidates exist.
- **Unresolved** — no governed identity correspondence has been established.
- **Conflicted** — relevant evidence or source assertions conflict.

## Safety invariants

1. Identity similarity MUST NOT by itself establish Canonical Identity.
2. Source identity MUST remain distinguishable from Canonical Identity.
3. Evidence and provenance MUST remain attached to the candidate and decision.
4. Ambiguous, unresolved, and conflicted outcomes MUST remain observable.
5. A fixture MUST NOT create or mutate Canonical Facts implicitly.
6. A governed Match Decision MUST be explicit before a Canonical Identity may be applied.
7. The fixture MUST be deterministic and replayable.
8. Reasoning MUST remain read-only.

## Expected path

```text
Source Identity A
      ↓
Evidence
      ↓
Candidate Match
      ↓
Governed Decision
      ↓
Canonical Identity
```

If the governed decision is absent, the path MUST terminate at Candidate Match / unresolved status and MUST NOT cross into Canonical Identity.

## Non-goals

S281 does not implement probabilistic entity resolution, automatic matching thresholds, production master-data synchronization, or autonomous graph mutation.
