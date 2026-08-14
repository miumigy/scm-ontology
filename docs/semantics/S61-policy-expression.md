# S61 — Canonical Policy Expression

## Purpose

S61 gives policies a structural expression without turning the policy into an executable selector or optimizer objective.

## Canonical forms

`PolicyExpression` supports four structural forms:

- `atomic` — one policy condition or preference
- `all` — all child expressions apply together
- `any` — one or more alternatives are represented
- `not` — negation of one child expression

## Boundary

`PolicyExpression` describes semantic structure. It does not evaluate conditions, rank alternatives, select an action, or optimize an objective.

Therefore:

`PolicyExpression != ConstraintExpression`

although the two may have structurally similar logical forms, because their semantic roles differ.

Also:

`Policy != Constraint != OptimizationObjective != Decision`.

## Priority

S61 intentionally does **not** introduce a numeric priority field or a universal ranking scale. Preference strength and ordering are domain- and policy-runtime concerns until a later canonical contract establishes their semantics.

## Example

```text
Policy
  preference: supplier A
  applicability:
    all
    ├─ domestic
    └─ available
```

The expression records structure only; an external policy runtime determines how it is interpreted.
