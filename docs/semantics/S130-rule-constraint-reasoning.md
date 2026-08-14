# S130 — Rule / Constraint Reasoning

## Purpose

S130 defines the reasoning contract for evaluating canonical SCM facts against Rules, Constraints, Policies, Objectives, and Preferences established in S107.

The reasoning layer evaluates applicability and violations; it does not silently create Decisions or Actions.

## Semantic boundary

```text
Fact / Observation / State
        ↓
Rule / Constraint / Policy
        ↓
Evaluation
        ↓
Violation / Satisfaction / Applicability
        ↓
Recommendation (optional)
        ↓
Decision (separate)
        ↓
Action (separate)
```

The following distinctions remain mandatory:

- Constraint ≠ Objective
- Policy ≠ Rule
- Rule Evaluation ≠ Decision
- Recommendation ≠ Decision
- Decision ≠ Action

## Constraint evaluation

A constraint expresses a condition that must hold within a defined context.

```text
Constraint
  + Context
  + Evidence
  + State
       ↓
Constraint Evaluation
       ↓
Satisfied | Violated | Unknown | Not Applicable
```

`Unknown` must not be interpreted as `Satisfied`.

## Rule evaluation

A Rule defines a semantic condition and an associated implication or classification.
It may produce an evaluation result without producing an operational action.

```text
Rule
 + Preconditions
 + Evidence
      ↓
Rule Evaluation
      ↓
Result / Explanation
```

## Epistemic requirements

Reasoning must retain epistemic status from S103.

A rule evaluated against an Estimate or Prediction cannot silently produce a Fact about the actual world.

```text
Prediction
   ↓ evaluated_by
Rule
   ↓
Prediction-based Evaluation
```

not:

```text
Prediction → Actual Fact
```

## Temporal requirements

Applicability is evaluated against an explicit temporal context. Effective, transaction, observation, planned, promised, and actual times retain their S106 semantics.

A rule that was effective in the past must not be retroactively applied as if it had always been active.

## Scenario requirements

A rule evaluation in a Scenario remains scenario-scoped.

```text
Actual State
   ↓
Scenario State
   ↓
Rule Evaluation
```

Scenario results do not overwrite Actual outcomes.

## Provenance requirements

Every material reasoning result should be traceable to:

```text
Input Evidence
   ↓
Rule / Constraint
   ↓
Evaluation
```

This connects S130 with S104/S125.

## Output categories

The canonical evaluation result may be:

- `satisfied`
- `violated`
- `unknown`
- `not_applicable`

Optional severity and explanation may be attached, but severity is not itself a Decision.

## Non-goals

S130 does not define:

- optimization algorithms
- solver implementations
- automated decision authority
- workflow execution
- vendor-specific rule engines
- a universal business-rule language

Those are implementation layers above this semantic contract.
