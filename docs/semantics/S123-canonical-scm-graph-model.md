# S123 — Canonical SCM Graph Model

## Purpose

S123 defines a graph projection of the Canonical Semantic Model. The graph is a representation of SCM semantics, not a replacement for the ontology.

## Projection model

```text
Canonical Entity
      ↓
Graph Node

Canonical Relationship
      ↓
Graph Edge
```

Node identity is based on canonical identity/reference semantics from S115. Source identifiers remain attached as provenance/reference metadata rather than replacing canonical identity.

## Node categories

The projection distinguishes:

- `entity`: persistent or identifiable SCM object
- `event`: occurrence/change in time
- `state`: contextual condition at a time
- `observation`: observation record
- `measurement`: measured value
- `decision`: decision record
- `action`: execution/action record
- `scenario`: hypothetical or alternative world

Value objects do not become independent graph entities unless they require identity, provenance, or relationship traversal.

## Edge semantics

Canonical predicates such as `contains`, `consumes`, `produces`, `fulfills`, `planned_for`, `executes`, `causes`, `derived_from`, and `measured_by` remain explicit graph edge predicates.

Do not collapse semantically distinct predicates into generic `RELATED_TO` edges.

## Metadata

Where applicable, graph nodes and edges preserve:

- canonical identifier
- source identity/reference
- valid/effective time
- transaction/recording time
- observation time
- provenance
- epistemic status
- scenario/world reference
- mapping reference

## Temporal graph

A graph snapshot is not assumed to represent eternal truth.

```text
Entity
  ├─ valid_from / valid_to
  ├─ transaction_time
  └─ observed_at
```

Events and state transitions remain distinct. Historical reconstruction must be possible without overwriting previous semantic states.

## Provenance graph

Mapped or derived values retain lineage:

```text
Source Value
   ↓ derived_from / mapped_from
Transformation / Mapping
   ↓
Canonical Value
```

Provenance is graph-addressable but is not reduced to a generic source label.

## Causal graph

Causal predicates such as `causes` and `affects` must remain distinct from correlation, attribution, or ordinary operational relationships. Causal uncertainty and evidence can be represented as metadata/linked assertions.

## Scenario graph

Scenario nodes provide a boundary for hypothetical states and decisions. Scenario edges must not be interpreted as actual historical events.

```text
Actual World
Scenario A
Scenario B
```

Counterfactual results remain distinguishable from observed outcomes.

## Property-graph neutrality

Neo4j, RDF, SQL-backed graphs, or another implementation may be used later. S123 specifies projection semantics independently of storage syntax.

## Non-goals

S123 does not define:

- a Neo4j-specific physical schema
- Cypher query conventions
- graph database indexing
- a universal event store
- causal inference algorithms
- graph analytics algorithms

## Exit criteria

A graph implementation can project canonical concepts and relations while preserving identity, temporal, provenance, epistemic, causal, and scenario semantics without introducing vendor-specific ontology concepts.
