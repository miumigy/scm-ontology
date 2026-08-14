# S53 — Semantic Provenance / Explanation

## Purpose

S53 defines the smallest canonical contract for explaining why a derived semantic fact exists.

The contract preserves machine-readable provenance without making natural-language generation part of the ontology.

## Model

```text
Derived Fact
├─ provenance
│  ├─ rule_id
│  └─ source_relationship_ids
└─ explanation
   └─ ordered steps
```

### Provenance

`Provenance` identifies:

- the inference rule that produced the fact
- the source relationship instances used by that rule

This is evidence metadata. It is not an audit log, event history, or database lineage model.

### Semantic explanation

`SemanticExplanation` contains ordered `ExplanationStep` values. A step is a deterministic semantic statement, not an LLM-generated narrative.

For example:

```text
Order-1 contains Line-1
Line-1 references Product-A
Therefore Order-1 concerns Product-A
```

The ontology does not prescribe how these statements are rendered for a human.

## Boundaries

S53 does not define:

- natural-language generation
- LLM prompts or models
- audit logging
- event sourcing
- confidence or probability
- temporal provenance
- recursive explanation graphs
- persistence format
- a general provenance standard

## Relationship to S52

S52 already preserves `rule_id` and source relationship IDs on derived relationships. S53 gives those concepts a reusable canonical representation and adds a minimal structured explanation boundary.

```text
S52 Semantic Inference
        ↓
Derived Fact
        ↓
S53 Provenance
        ↓
Future AI / human explanation
```

The explanation layer remains separate from the reasoning engine itself.
