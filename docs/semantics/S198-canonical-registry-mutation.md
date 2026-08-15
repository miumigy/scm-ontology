# S198 — Canonical Registry Mutation

S198 crosses the final governed mutation boundary for relation extensions.

An accepted, preflighted proposal is applied functionally to a supplied canonical relation registry snapshot. The original tuple remains unchanged and a new registry snapshot is returned.

Invariants include:

- predicate references must not collide with existing predicate or inverse references;
- inverse references must not collide with existing predicate or inverse references;
- a relation cannot use itself as its inverse;
- the mutation requires the S197 guard;
- no graph or assertion data is mutated by this operation.

This keeps registry application deterministic and auditable while preserving the existing canonical relation registry as an immutable snapshot.
