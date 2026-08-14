# S52 — Canonical Semantic Inference

## Purpose

S52 defines the smallest executable boundary between explicit canonical graph facts and derived semantic facts.

The ontology defines **what a derivation means**. A reasoning engine may later decide how rules are scheduled, indexed, persisted, or combined with an LLM.

## Contract

```text
Explicit Graph Facts
        |
        v
   InferenceRule
   /           \
antecedent   antecedent
        |
        v
 DerivedRelationship
        |
        +-- rule_id
        +-- source_relationship_ids
```

An S52 rule is currently a deterministic two-hop composition:

```text
A --p1--> B --p2--> C
            |
            v
        A --p3--> C
```

The derived relationship is a **fact derived from explicit facts**, not an assertion that the relationship was stored in the source graph.

## Provenance

Every derived relationship carries:

- `rule_id`
- ordered `source_relationship_ids`

This establishes minimal provenance without introducing an audit-log or event-sourcing model.

## Open-world boundary

Unknown or domain-specific predicates are not rejected by the inference primitive. A rule may explicitly reference such predicates when an application chooses to do so.

## Deliberate non-goals

S52 does not define:

- an inference language
- recursive closure
- arbitrary rule graphs
- negation or closed-world reasoning
- probabilistic inference
- temporal inference
- conflict resolution
- LLM reasoning
- graph-database execution
- persistence or audit logging

These remain implementation or future semantic contracts.

## Boundary with S51

S51 answers:

> What explicit facts are present in the canonical graph?

S52 answers:

> What derived fact follows from an explicitly declared semantic rule?

Neither contract specifies how an LLM should reason over the graph.

## Boundary with SCM Ontology

```text
SCM Ontology
    |
    +-- defines semantic primitives and valid relationships
    |
    +-- declares inference meaning
    v
Canonical Graph
    |
    +-- explicit facts
    v
Inference Engine
    |
    +-- executes rules
    +-- manages scheduling/indexing
    +-- may later integrate LLMs
```

The execution mechanism must not be allowed to redefine the canonical meaning of the inferred relationship.
