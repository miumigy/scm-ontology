# S100 — Decision & Action Semantics

S100 defines the semantic boundary between Decision, Action, Outcome, and the Observations that provide feedback after execution.

## Canonical decision

Decision, Action, Outcome, and Observation are distinct artifacts in a closed-loop operational process.

```text
Observation
    ↓
Evaluation
    ↓
Exception / Context
    ↓
Decision
    ↓
Action
    ↓
Outcome
    ↓
Observation
```

The loop is causal and temporal, but the artifacts must not be collapsed into one object.

## Decision

A Decision is a selected course of action, policy choice, or commitment made under a defined context.

A Decision may consider:

```text
observations
evaluations
exceptions
constraints
objectives
policies
forecasts
alternatives
risk
```

A Decision is not the same as the Action that may later implement it.

## Decision versus recommendation

A recommendation proposes an alternative or course of action.

A Decision indicates that an authorized actor or process selected an option.

```text
Recommendation
    ↓
Decision
```

The transition is not automatic.

An LLM-generated suggestion, optimization result, or planning proposal remains a recommendation until the applicable decision authority accepts it as a Decision.

## Decision context

A Decision should be interpretable in terms of the context available at decision time where auditability matters.

Conceptually:

```text
Decision Context
├─ observations / evidence
├─ evaluation results
├─ constraints
├─ objectives
├─ alternatives considered
├─ selected option
├─ authority / actor
├─ decision time
└─ rationale
```

S100 does not require every field for every domain.

## Decision authority

A Decision may be made by:

```text
human
role
team
system
algorithm
workflow
hybrid human + system process
```

Authority semantics should remain distinct from mere technical authorship.

For example, a system may calculate a recommendation while a planner retains decision authority.

## Action

An Action is an intentional operation performed or initiated to change a condition, execute a Decision, or pursue an objective.

Examples:

```text
release purchase order
change production schedule
expedite shipment
allocate inventory
adjust safety stock
change transport mode
```

An Action may implement a Decision, but an Action can also occur without a preceding formal Decision where the domain permits autonomous execution.

## Planned versus executed Action

The intended action and the executed action are distinct when execution can diverge from intent.

```text
Decision
   ↓
Planned Action
   ↓
Execution
   ↓
Actual Action
```

For example, a Decision may request shipment via Route A while operational constraints cause execution via Route B.

The executed Action should preserve that divergence rather than rewriting the Decision.

## Action status

An Action may have its own lifecycle, for example:

```text
planned
approved
scheduled
started
partially_completed
completed
failed
cancelled
```

This lifecycle belongs to the Action/execution layer, not to the source Observation.

## Outcome

An Outcome is the resulting condition, effect, or consequence attributable to an Action or process.

```text
Action
   ↓
Outcome
```

An Outcome is not automatically a new Observation.

It becomes observable through one or more subsequent Observations when the domain measures the resulting condition.

## Outcome versus Observation

Consider:

```text
Action:
  expedite shipment

Outcome:
  delivery was accelerated

Observation:
  actual delivery timestamp = 2026-08-14T15:20
```

The Outcome describes the consequence semantically; the Observation records an observable fact according to the applicable observation semantics.

## Causal linkage

Where provenance matters, the following chain should be representable:

```text
Observation O1
    ↓ informs
Decision D1
    ↓ authorizes / selects
Action A1
    ↓ produces
Outcome R1
    ↓ observed by
Observation O2
```

This creates a traceable closed loop without making the objects identical.

## Decision rationale

A rationale explains why a Decision was selected among alternatives or under constraints.

Rationale may reference:

```text
Evidence
Objective
Constraint
Policy
Risk assessment
Optimization result
Human judgement
```

Rationale is not itself the Decision and should not be confused with the underlying Evidence.

## Alternatives

A Decision may select one alternative from a set of candidates.

```text
Alternatives
├─ expedite
├─ defer
├─ reallocate
└─ substitute
        ↓
Selected alternative = reallocate
```

The existence of alternatives does not require that every alternative be persisted, but the distinction is useful for decision provenance and explainability.

## Constraints

A Decision or Action may be constrained by:

```text
capacity
inventory
lead time
budget
service requirements
regulatory rules
resource availability
policy
```

Constraints should be represented separately from the selected Decision where they are reusable or independently governed.

## Authorization

Authorization answers whether a Decision or Action is permitted by the applicable authority or policy.

```text
Decision
   ↓
Authorization
   ↓
Action permitted / rejected
```

Authorization is distinct from Decision itself.

A person may decide an action but lack authority to execute it.

## Action execution versus completion

Initiating an Action does not guarantee completion.

```text
Action requested
    ↓
Execution attempted
    ↓
Completed / Failed / Partial
```

Operational systems should preserve execution outcome rather than assuming that a Decision implies successful execution.

## Failure and deviation

An Action may fail or deviate from the Decision.

```text
Decision: produce 1,000 units
Action: production order for 1,000
Outcome: only 800 produced
```

The Decision remains the selected intent; the Outcome records the result.

A subsequent Observation can measure the actual 800 units.

## Closed-loop feedback

The fundamental SCM pattern is a feedback loop:

```text
Observe
   ↓
Interpret / Evaluate
   ↓
Decide
   ↓
Act
   ↓
Observe outcome
   ↓
Evaluate again
   ↓
Decide again
```

S100 treats this loop as a process relationship, not as a recursive Observation object.

## Relationship to Exception

An Exception may trigger a Decision, but a Decision does not require an Exception.

```text
Exception → Decision
```

is common for exception management, while normal planning and optimization also produce Decisions without any breach.

## Relationship to Policy

Policy can constrain or guide Decisions and Actions.

```text
Policy
  ↓ constrains
Decision
  ↓ authorizes
Action
```

Policy is not equivalent to a Decision because it may apply repeatedly across many Decisions.

## Relationship to Evidence and Claim

Evidence may support a Decision directly or through a Claim.

```text
Observation
   ↓
Evidence
   ↓
Claim / Assessment
   ↓
Decision
```

A Decision is an operational choice, not an epistemic Claim.

## Relationship to Plan

A Plan may contain intended Decisions and Actions, but a Plan is not identical to either.

```text
Plan
├─ intended Decisions
└─ intended Actions
```

Execution can diverge from the Plan and should preserve actual execution semantics.

## No mutation of historical Observation

Executing an Action must not rewrite the Observation that motivated the Decision.

```text
Observation O1 = 700
Decision D1 = reduce replenishment
Action A1 = change PO
Observation O2 = 480
```

O1 remains historically true even after O2 demonstrates improvement.

## No mandatory fields on Observation

S100 does not add fields such as:

```text
decision
action
decision_status
action_status
outcome
rationale
assigned_to
```

to the canonical Observation primitive.

These belong to Decision, Action, Outcome, workflow, execution, or provenance models.

## Non-goals

S100 does not define a universal decision-rights matrix, approval workflow, optimization algorithm, action execution engine, policy language, planning model, or process-mining standard.
