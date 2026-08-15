# S164 — End-to-End SCM Reference Fixture

S164 expands the reference fixture across several core SCM object domains without introducing new ontology concepts.

```text
Demand → Order → Supply → Inventory
```

The fixture intentionally represents each object through canonical assertions. It does not assert that these objects are one-to-one linked; relationship semantics remain the responsibility of canonical relations and their assertions.

## Purpose

- exercise cross-domain use of the canonical assertion envelope
- provide a stable regression fixture for SCM-wide examples
- expose modeling gaps before graph adapters are introduced

## Non-goals

No inferred causality, fulfillment linkage, allocation logic, graph storage, or business-process semantics are invented by the fixture.
