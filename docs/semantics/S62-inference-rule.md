# S62 — Canonical Inference Rule

## Purpose

S62 defines the semantic identity of an inference rule separately from its runtime application.

An inference rule describes how one or more premise semantics support a conclusion semantics.

```text
Fact A + Fact B
      ↓
InferenceRule
      ↓
Derived Fact C
```

## Canonical primitive

`InferenceRule` contains:

- `rule_id`
- `premise_types`
- `conclusion_type`

The premise and conclusion values are semantic references, not concrete fact instance IDs.

Concrete fact instances belong to a `Derivation` / `InferenceStep`. The existing S54 derivation model records `rule_id`, input fact IDs, and output fact ID, preserving the distinction between a rule definition and its application. 

## Boundaries

`InferenceRule != Derivation`

`InferenceRule != Constraint`

`InferenceRule != Policy`

`InferenceRule != ConstraintEvaluator`

`Derived Fact != Observed Fact`

S62 does not define rule execution, pattern matching, a rule language, conflict resolution, probabilities, optimization, or LLM reasoning.

## Acyclicity

A rule itself does not impose execution order. The existing S54 `Derivation` contract is responsible for ordered application and forward-reference validation.

This prevents the canonical rule definition from becoming an execution engine.
