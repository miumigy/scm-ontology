# S177 — Relation Registry Completeness Guards

S177 adds regression checks for structural integrity of the canonical relation registry.

The registry must maintain:

- unique canonical predicate identifiers
- unique inverse identifiers
- no self-inverse relation declarations

These are structural invariants only. S177 does not infer missing inverse predicates or create graph assertions automatically.
