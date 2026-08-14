# SCM Ontology

Canonical Semantic Model for Supply Chain Management.

This repository defines a framework-independent ontology for SCM entities, relationships, events, states, constraints, policies, decisions, and performance semantics, with validation and Neo4j implementation artifacts.

## Semantic foundation

S101–S112 establish the semantic contracts for:

- closed-loop decision semantics
- causality and outcomes
- scenarios and counterfactuals
- epistemic status and uncertainty
- provenance and lineage
- identity and entity resolution
- temporal/state/event semantics
- constraints, policies, rules, and decisions
- plan, schedule, commitment, execution
- demand, order, supply, inventory, capacity, and fulfillment
- network, node, lane, route, and location
- product, material, item, and transformation
- measurement, metric, KPI, and performance

S113 consolidates those contracts into a canonical concept and relationship registry. It explicitly separates primitive, core, derived, and contextual concepts and distinguishes physical, information, decision, and semantic dimensions.

## Development status

**v0.1 experimental — semantic consolidation in progress.**

The next milestones turn the canonical model into a machine-readable ontology while preserving temporal, epistemic, causal, provenance, and planned/actual boundaries.

See `docs/semantics/` for the semantic contracts and `BACKLOG.yaml` for the active implementation backlog.
