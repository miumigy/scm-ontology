# S138 — Plan

S138 defines the SCM OS Plan semantic: expressing intended future actions and outcomes under objectives, constraints, policies, resources, and scenarios.

## Plan contract

```text
Diagnosis / Demand / State / Commitments
              ↓
Objectives + Constraints + Policy
              ↓
Alternatives / Scenario Evaluation
              ↓
Plan
 ↓
Schedule / Commitment
 ↓
Execution
```

A Plan is an intentional specification of a future course of action or intended state. It is not a Schedule, Commitment, Decision, or Actual outcome.

## Core boundaries

- Plan ≠ Forecast
- Plan ≠ Schedule
- Plan ≠ Commitment
- Plan ≠ Decision
- Plan ≠ Execution
- Planned ≠ Actual
- Scenario Plan ≠ Actual History

A plan may be created because of a Decision, but the plan and decision remain distinct semantic objects.

## Plan context

A Plan may reference:

- objective(s)
- constraint(s)
- policy/rule references
- subject/network scope
- demand and supply context
- resource/capacity assumptions
- alternative/scenario references
- decision reference
- provenance and reasoning trace

## Plan alternatives

Multiple Plans or Plan Alternatives may represent different feasible courses of action. A plan should not imply that it is optimal unless an explicit evaluation supports that claim.

```text
Alternative A ─┐
Alternative B ─┼→ Evaluation → selected Plan
Alternative C ─┘
```

## Temporal semantics

Plan validity and intended execution times are separate from the time the plan was created or recorded. Planned time must not overwrite actual execution time.

## Versioning and revision

Plan revisions create new plan versions or explicit successor relationships. Historical plans remain reconstructable.

A revised plan does not rewrite the fact that an earlier plan existed.

## Scenario planning

Scenario plans are scoped to their scenario and may be compared with actual or other scenarios without becoming actual-world plans.

## Constraints and feasibility

A plan may reference constraints and feasibility evaluations. Constraint satisfaction is an assessment, not a guarantee of execution.

## Decision connection

A Decision may authorize, select, or establish a Plan. The semantic relationship must remain explicit:

```text
Decision
   ↓ establishes / selects
Plan
   ↓ intended_for
Schedule / Execution
```

A Plan can also exist as a draft or candidate before a Decision.

## Non-goals

S138 does not define an optimization algorithm, APS implementation, scheduling engine, solver, or workflow system. It defines the canonical meaning of a plan independently of implementation technology.
