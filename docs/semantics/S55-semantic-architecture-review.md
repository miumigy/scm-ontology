# S55 — Semantic Architecture Review & Canonical Consolidation

## Status

Architecture checkpoint after S54. This milestone introduces no new runtime primitive.

## Purpose

S41–S54 established a canonical semantic stack for relationship semantics, graph representation, validation, query, inference, provenance, and derivation composition. S55 records the responsibility boundaries that should govern the next phase.

The governing rule remains:

> Canonical Semantic Model != implementation schema != graph database schema != API schema.

## 1. Current semantic stack

```text
Canonical domain semantics
  Entity / Event / State / Time / domain concepts
            |
            v
Relationship semantics
  predicate / endpoints / cardinality / qualifiers
            |
            v
Relationship identity and validity
  relationship_id / versions / validity
            |
            v
Canonical Graph
  nodes / relationships
            |
            v
Validation
  relationship-level / cross-entity
            |
            v
Semantic Query
  explicit graph facts
            |
            v
Inference
  rules / derived facts
            |
            v
Provenance / Derivation
  evidence / ordered inference chain
            |
            v
Future AI Reasoning layer
```

The graph and reasoning layers are execution-oriented representations of canonical semantics, not replacements for the ontology.

## 2. Canonical object boundaries

### Entity
A canonical identifiable thing. Source-system record keys must not automatically become canonical identity.

### RelationshipInstance
Answers **which particular relationship is this?** It is identified by `relationship_id` and contains `from_id`, `predicate`, and `to_id`. Identity is independent of endpoint type, cardinality, qualifiers, and temporal validity.

### RelationshipVersion
Answers **when does this semantic version apply?** `valid_from` is required and `valid_to` may be open-ended. Persistence identity and interval arithmetic remain outside the contract.

### Qualifier
A relationship-specific semantic dimension. A qualifier must not silently become an entity attribute merely because an implementation stores it there.

### CanonicalGraph
The transport-neutral representation of canonical nodes and relationships. JSON is a serialization format, not the ontology; RDF/OWL and property-graph implementations remain mappings.

### Derived Fact
A fact produced by inference, distinct from an explicitly asserted fact, with provenance retained.

### Provenance
Structured evidence describing the rule and source facts behind a derived result. It is not an audit-log implementation or an LLM explanation.

### Derivation
An ordered acyclic composition of inference steps. Recursive closure and rule scheduling are outside S54.

## 3. Validation responsibility

Relationship-level validation checks predicate, endpoint constraints, cardinality when sufficient context exists, identity shape, and validity shape.

Cross-entity validation checks endpoint resolution, node-type consistency, and relationship identity consistency.

Neither validation layer is a closed-world registry. Unknown/domain-specific vocabulary remains admissible unless a declared canonical constraint is violated.

## 4. Query vs inference

```text
query(graph) -> explicit facts
infer(facts, rules) -> derived facts
```

A query must not silently infer. Inference must preserve the distinction between explicit and derived facts.

## 5. Inference vs provenance vs explanation

```text
Inference   = WHAT is derivable
Provenance  = FROM WHICH rule/evidence it was derived
Explanation = HOW the derivation is communicated
```

Natural-language explanation and LLM prompting remain outside the canonical layer.

## 6. S54 derivation boundary

```text
Explicit facts
   -> Rule A -> Derived fact 1
                   -> Rule B -> Derived fact 2
```

A step may consume explicit facts or facts produced by preceding steps. Forward references, self-reference, and duplicate outputs are invalid. Recursive closure, fixed-point semantics, conflict resolution, scheduling, and probabilistic inference remain deferred.

## 7. Event / State / causal boundary

The repository already contains canonical Event and State primitives plus earlier causal/transition modules. Future work must integrate these rather than create parallel abstractions:

- Event = an occurrence.
- State = a condition/configuration that holds.
- Transition/causal semantics = relationships among events and states.
- Relationship semantics = graph connections among canonical objects.
- Inference = derivation of semantic facts.

## 8. Implementation boundary

The canonical layer remains independent of SQL temporal tables, ERP/WMS/TMS schemas, Neo4j labels/indexes/Cypher, JSON Schema as ontology definition, RDF/OWL as a mandatory representation, API DTOs, persistence IDs, UUID-generation policy, and audit/event-sourcing implementations.

## 9. Risks identified

1. **Primitive duplication** — prefer consolidation or adapters over parallel representations.
2. **Inference leakage** — traversal/query must not silently become reasoning.
3. **Derived-fact contamination** — derived facts must remain distinguishable from explicit facts.
4. **Temporal leakage** — validity must not silently become database versioning or audit history.
5. **Closed-world drift** — unknown predicates and domain extensions should remain admissible unless constrained.
6. **AI coupling** — expose structured facts and provenance without embedding prompts, model IDs, or response formats in the canonical layer.

## 10. Architecture checkpoint

```text
                    SCM Ontology
                         |
          +--------------+--------------+
          |                             |
       Semantics                    Constraints
          |                             |
          +--------------+--------------+
                         |
                  Canonical Graph
                         |
             +-----------+-----------+
             |                       |
        Semantic Query          Validation
             |
        Explicit Facts
             |
          Inference
             |
        Derived Facts
             |
     Provenance / Derivation
             |
       Future AI Reasoning
```

## 11. Non-goals

S55 does not add graph-database integration, RDF/OWL serialization, LLM integration, recursive rule closure, policy engines, event sourcing, audit logging, or persistence.

## 12. Next-phase recommendation

Reassess the roadmap after this checkpoint. Prefer the missing SCM-native semantics before adding more reasoning machinery:

1. Event/State integration with the current graph model
2. SCM constraint/policy semantics
3. Temporal semantics across entities, events, states, and relationships
4. SCM-specific reasoning patterns
5. AI Reasoning adapter

Each should remain a separate Semantic Contract until its boundary is stable.
