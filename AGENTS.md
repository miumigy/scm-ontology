# SCM Ontology Agent Contract

## Mission

Preserve the framework-independent canonical SCM semantic model and connect it to enterprise data, simulation, graph reasoning, and AI without weakening Canonical Truth, provenance, temporal, lifecycle, or governance boundaries.

## Current status

**M8 — Canonicalization, Projection & Operational Governance: COMPLETE.**

The next phase is implementation against the M8 contracts. Do not invent a new semantic boundary merely because an implementation is easier that way.

## Non-negotiable rules

1. Prefer canonical concepts over ERP/vendor terminology.
2. Do not introduce an Entity when the concept is better represented as a Relationship, Event, State, Constraint, Decision, KPI, or Risk.
3. Respect `extends` inheritance and relationship signatures.
4. Keep APICS/SCOR mappings as crosswalks; do not reproduce proprietary training content.
5. Every schema or contract change must have validation and tests.
6. Validate example datasets against the ontology.
7. Do not weaken validation merely to make CI green.
8. Preserve temporal and source-system semantics as the model evolves.
9. Never infer Canonical Truth from mapping success, similarity, inference, provenance, confidence, projection success, or ingestion success alone.
10. Never silently mutate Canonical Facts outside an explicit governed application step.
11. Preserve provenance, lineage, conflict, uncertainty, and historical records.
12. Keep derived/projection state distinguishable from Canonical Truth.
13. Preserve explicit scope boundaries; never broaden enterprise/tenant/organization/product scope implicitly.
14. Treat M8 normative documents as contracts for future implementations.

## Development loop

inspect → model → contract → implement → validate → test → document → PR → governed merge

## Documentation loop

When a contract or architecture changes:

1. update the normative document;
2. update/add regression tests;
3. update the architecture or milestone index;
4. update README diagrams when the conceptual architecture changes;
5. keep historical milestone documents intact unless the change is genuinely a correction to historical fact.

## Definition of done

A change is not complete merely because it compiles or CI is green. It is complete when the implementation, tests, normative documentation, lineage, and user-facing documentation agree.
