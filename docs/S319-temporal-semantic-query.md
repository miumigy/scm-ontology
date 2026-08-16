# S319 — Temporal Semantic Supply Chain Query

S319 establishes a governed read-only query boundary over the temporal semantic graph.

## Contract

A query explicitly supplies:

- `at`: the semantic observation instant;
- `from_id` and `to_id`: path endpoints;
- optional explicit `predicates`;
- `max_hops` to bound traversal.

The runtime resolves only relationship versions that are valid at `at`. Returned
steps preserve their canonical relationship identity, predicate, endpoints, and
explicit qualifiers.

## Determinism

Results are ordered by node sequence and relationship sequence. The response
also exposes a SHA-256 digest of the canonical graph representation used for the
query. This makes the query result reproducible against a known graph snapshot.

## Provenance

Each returned path carries query-level provenance consisting of:

- the canonical graph digest;
- the relationship IDs traversed by the path.

This is snapshot/path provenance, not a claim that the ontology has inferred a
source-system provenance chain. Source-level provenance remains the responsibility
of the relevant fact/assertion contracts.

## Safety boundary

- read-only: no graph mutation is performed;
- no identity resolution or fuzzy matching;
- no inferred relationships or missing qualifiers;
- temporal validity is evaluated from explicit relationship versions;
- feasibility remains the S318 concern;
- optimization, allocation, and execution remain outside the ontology runtime.

S319 therefore exposes a stable semantic query surface that downstream planning
or scenario systems can consume without coupling those systems to a graph-store
vendor or storage representation.
