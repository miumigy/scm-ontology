# SCM Ontology Agent Contract

## Mission
Preserve the framework-independent canonical SCM semantic model and connect it to enterprise data, simulation, graph reasoning, and AI.

## Rules
1. Prefer canonical concepts over ERP/vendor terminology.
2. Do not introduce an Entity when the concept is better represented as a Relationship, Event, State, Constraint, Decision, KPI, or Risk.
3. Respect `extends` inheritance and relationship signatures.
4. Keep APICS/SCOR mappings as crosswalks; do not reproduce proprietary training content.
5. Every schema change must have validation and tests.
6. Validate example datasets against the ontology.
7. Do not weaken validation merely to make CI green.
8. Preserve temporal and source-system semantics as the model evolves.

## Development loop
inspect -> model -> implement -> validate -> test -> document -> PR

## Current priority
Complete Semantic Integrity v0.1 before expanding graph reasoning capabilities.
