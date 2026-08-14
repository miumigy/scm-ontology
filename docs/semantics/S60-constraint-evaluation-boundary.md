# S60 — Constraint Evaluation Boundary

## Purpose

S60 defines the canonical boundary between a constraint expression and an external evaluator.

## Canonical primitives

### EvaluationContext

`EvaluationContext` represents the facts supplied to an evaluation runtime.

### ConstraintResult

The canonical result vocabulary is:

- `satisfied` — the constraint is supported as satisfied by the supplied context.
- `violated` — the constraint is supported as violated by the supplied context.
- `unknown` — the available information is insufficient to establish either state.

`unknown` is intentionally distinct from `violated`.

### ConstraintEvaluation

`ConstraintEvaluation` contains the result and an optional reason. It records an evaluation outcome; it does not perform evaluation.

## Boundary

```text
ConstraintExpression
        ↓
EvaluationContext
        ↓
External Evaluator
        ↓
ConstraintEvaluation
```

The evaluator itself remains outside the Canonical Semantic Model.

S60 does not define:

- an evaluator algorithm
- Boolean three-valued logic implementation
- data fetching
- type coercion rules
- solver integration
- optimization
- policy selection
- persistence
- LLM reasoning

## Important semantic distinction

```text
VIOLATED != UNKNOWN
```

For example, if a supplier's capacity is absent from the available facts, the statement `capacity >= 100` is not necessarily false. The canonical outcome may be `unknown`.

This distinction is required for incomplete enterprise data and downstream AI reasoning.
