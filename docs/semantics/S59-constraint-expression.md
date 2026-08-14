# S59 — Canonical Constraint Expression

## Purpose

S59 defines the structural semantics of compound constraints without defining how those expressions are evaluated.

## Canonical forms

`ConstraintExpression` has four canonical forms:

- `atomic` — one atomic constraint condition
- `all` — all child expressions are required
- `any` — at least one child expression is applicable
- `not` — negation of one child expression

An expression is a semantic structure, not an executable program.

## Example

```text
all
├─ atomic: capacity >= demand
├─ atomic: lead_time <= required_lead_time
└─ atomic: status = active
```

## Boundary

S59 does not define:

- a Boolean expression DSL
- operator evaluation
- SQL, Python, CEL, JSONLogic, or OPA syntax
- solver integration
- optimization semantics
- policy selection
- persistence
- LLM reasoning

The canonical model records the logical structure. An external validation or policy runtime may interpret it.

## Design rule

`ConstraintExpression != ConstraintEvaluator`.

This preserves the distinction between semantic representation and implementation/runtime behavior.
