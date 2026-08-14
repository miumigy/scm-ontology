# S54 — Semantic Rule Composition

## Status

Draft semantic contract.

## Purpose

S54 defines how multiple semantic inference steps compose into a derivation without making recursive closure, an inference engine, or an LLM part of the Canonical Semantic Model.

## Boundary

S52 defines an inference rule and a derived fact. S53 defines provenance for derived facts. S54 adds an ordered derivation made of inference steps.

A derivation is a semantic record of rule applications. It is not an execution plan, database transaction, event log, or reasoning engine.

## Canonical model

```text
Derivation
└─ steps[]
   └─ InferenceStep
      ├─ rule_id
      ├─ input_fact_ids[]
      └─ output_fact_id
```

`input_fact_ids` may refer to explicit facts or facts produced by earlier steps. A composed derivation must not require forward references to later derived facts.

## Acyclic composition

The minimum contract is an ordered derivation. A step may consume an output produced by an earlier step, enabling:

```text
explicit facts
  ↓
Rule A → Fact-1
  ↓
Rule B → Fact-2
  ↓
Rule C → Fact-3
```

Recursive closure, fixed-point computation, recursion limits, and rule scheduling are outside S54.

## Identity

`rule_id` identifies the semantic inference rule. `output_fact_id` identifies the derived fact within the derivation. These identifiers are references, not prescriptions for UUID generation or persistence.

## Provenance

S54 composes inference steps; S53 remains the contract for provenance and explanation. A consumer can map each step to its provenance without changing the Canonical Semantic Model.

## Non-goals

- recursive inference
- transitive closure engine
- rule conflict resolution
- confidence scoring
- probabilistic inference
- temporal reasoning
- LLM reasoning
- persistence or event sourcing
- database-specific execution
