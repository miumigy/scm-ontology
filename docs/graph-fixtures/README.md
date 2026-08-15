# M6 — Canonical Graph Fixtures

A graph fixture is a small, deterministic, executable representation of SCM facts used to validate end-to-end reasoning.

## Fixture contract

Each fixture must contain:

- canonical entities
- canonical relations
- source/provenance metadata where applicable
- deterministic identifiers
- expected query results
- expected evidence/explanation coverage

Fixtures must not encode vendor-specific semantics as canonical predicates.

## Initial fixture families

1. supply dependency chain
2. inventory/capacity chain
3. multi-hop supply-risk chain

The fixtures are intentionally small. Their purpose is semantic and reasoning validation, not realistic enterprise-data volume simulation.
