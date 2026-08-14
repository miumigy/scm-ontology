# S133 — Decision Reasoning

S133 defines the semantic contract for moving from evaluated alternatives to a Recommendation or Decision without collapsing the two.

## Reasoning contract

```text
Observation / Evaluation
        ↓
Objectives + Constraints + Policy + Preferences
        ↓
Alternatives / What-if Results
        ↓
Decision Evaluation
        ↓
Recommendation (optional)
        ↓
Decision (authorized commitment)
        ↓
Action (execution)
```

## Core boundaries

- Objective ≠ Constraint
- Policy ≠ Rule
- Alternative ≠ Recommendation
- Recommendation ≠ Decision
- Decision ≠ Action
- What-if Result ≠ Actual Outcome

A reasoning engine may generate a Recommendation. It must not represent that Recommendation as a Decision unless a distinct decision event/record establishes the decision.

## Decision evaluation

A decision evaluation compares one or more alternatives against an explicit decision context.

The context may include:

- objectives
- constraints
- policies
- preferences
- evidence
- metric/KPI assessments
- causal assessments
- what-if results
- uncertainty

The evaluation should preserve which inputs were used and their epistemic status.

## Recommendation

A Recommendation is a proposed alternative produced by reasoning. It may include rationale, expected outcomes, trade-offs, evidence, and uncertainty.

A Recommendation has no execution authority by itself.

## Decision

A Decision represents an explicit selection/commitment by an authorized decision-maker or decision authority. The canonical model should preserve:

- selected alternative
- decision authority / actor
- decision time
- decision context
- supporting evidence
- rationale where available
- superseded decision where applicable

## Uncertainty

Uncertain evidence remains uncertain during reasoning. The reasoning layer must not convert `unknown`, `estimated`, `predicted`, or `simulated` inputs into `actual` facts merely because an alternative was selected.

## Constraint handling

Constraint evaluations from S130 inform decision reasoning but do not become Decisions. An alternative with violated mandatory constraints should be distinguishable from an alternative that merely has a lower preference or objective score.

## What-if connection

S132 results may provide expected or hypothetical outcomes for alternatives. They remain scenario-scoped and must not overwrite actual history.

## Causal connection

S131 causal assessments may support rationale or expected effect analysis. Causal assessment remains distinct from Decision.

## Provenance

A recommendation or decision should retain references to material evidence and reasoning inputs where available. This supports explainability and later audit.

## Non-goals

S133 does not define an optimization algorithm, decision authority hierarchy, workflow engine, approval UI, or autonomous-agent policy. Those remain implementation/application concerns above the canonical semantic model.
