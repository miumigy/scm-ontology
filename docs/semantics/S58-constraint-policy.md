# S58 — Constraint / Policy Semantic Contract

## Purpose

S58 distinguishes constraints and policies from facts, inference rules, and derived facts.

- **Fact** describes what is true.
- **Constraint** restricts what is allowed.
- **Policy** expresses a preference or direction for choosing behavior.
- **Inference Rule** derives a new fact from existing facts.
- **Derived Fact** is the result of inference.

## Canonical primitives

### Constraint

`Constraint` is a first-class semantic object with:

- `constraint_id`
- `subject`
- `operator`
- `value`

The contract intentionally does not define evaluation semantics. A constraint represents a restriction; a solver or validation engine decides whether it is satisfied.

### Policy

`Policy` is a first-class semantic object with:

- `policy_id`
- `subject`
- `directive`
- `value`

A policy expresses preference or direction. It is not equivalent to a hard constraint and does not itself select an action.

## Boundary rules

`Constraint != Policy != InferenceRule != DerivedFact`.

S58 does not introduce a rule engine, optimization solver, Boolean expression language, persistence model, or LLM reasoning layer.

The deliberately small contract leaves implementation-specific expression languages and execution semantics outside the Canonical Semantic Model.
