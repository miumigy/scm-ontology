# S178 — Relation Registry Structural Integrity

S178 strengthens regression coverage around the canonical relation registry.

## Invariants

- `predicate_ref` values are unique.
- An `inverse_ref` may refer to a canonical predicate when the inverse relation is explicitly registered.
- Inverse metadata alone never creates an assertion or a new predicate.

These checks protect the registry as it grows without introducing inference or automatic ontology mutation.
