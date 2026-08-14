# S101 — Outcome & Causal Feedback Semantics

S101 defines the semantic boundary between Outcome, Effect, Cause, Causal Link, Attribution, Feedback, and subsequent Observations in the SCM closed loop.

## Canonical decision

An Outcome describes a consequence or resulting condition associated with an Action or process. A subsequent Observation records an observable fact about that condition. A causal relationship expresses a claimed or supported relationship between events, actions, and outcomes; it must not be inferred merely from temporal succession.

```text
Decision
   ↓
Action
   ↓
Outcome / Effect
   ↓
Observation
   ↓
Evaluation
   ↓
Feedback
   ↓
Decision
```

The canonical Observation primitive remains unchanged.

## Outcome

An Outcome is a resulting condition, effect, or consequence associated with an Action, Decision, or process.

Examples:

```text
Action: increase safety stock
Outcome: inventory availability increased

Action: expedite shipment
Outcome: delivery delay reduced
```

An Outcome is semantic process information; it is not automatically an Observation.

## Intended Outcome

An Intended Outcome is the result that a Decision or Action was expected to produce.

```text
Decision
   ↓
Intended Outcome
```

For example:

```text
Intended Outcome:
  service level ≥ 98%
```

An Intended Outcome expresses expectation, not evidence that the result actually occurred.

## Actual Outcome

An Actual Outcome is the resulting condition believed to have occurred after execution.

It should be distinguished from the intended outcome when execution may diverge.

```text
Intended Outcome = service level ≥ 98%
Actual Outcome   = service level = 96.5%
```

The Actual Outcome does not by itself prove causality.

## Outcome measurement

An Outcome may be measured by one or more Observations.

```text
Action A1
   ↓
Outcome R1
   ↓ measured by
Observation O2
```

A measurement is evidence about the Outcome, not the Outcome itself.

## Cause

A Cause is a factor, event, condition, mechanism, or intervention asserted to contribute to an Effect or Outcome.

A Cause is relational: something is a cause **of** something else.

```text
Cause C1 ──causes/contributes to──→ Effect E1
```

Cause should not be modeled as an intrinsic property of an Observation without the relevant relationship context.

## Effect

An Effect is a consequence or change associated with one or more causes.

In operational contexts, an Effect may correspond to an Outcome, but the terms are not universally interchangeable.

```text
Cause → Effect
Action → Outcome
```

S101 preserves both distinctions because causality and operational result semantics answer different questions.

## Causal Link

A Causal Link represents a semantic assertion or modeled relationship that one entity, event, action, or condition caused or contributed to another.

Conceptually:

```text
Source
  ↓ causal relation
Effect / Outcome
```

A Causal Link should preserve its direction.

```text
A → B
```

is not equivalent to:

```text
B → A
```

## Temporal succession is not causality

S101 explicitly rejects the inference:

```text
A happened before B
therefore
A caused B
```

Temporal ordering may be evidence relevant to causal analysis, but it is not sufficient by itself to establish causation.

## Attribution

Attribution expresses how strongly an Outcome or Effect is assigned to a particular Cause, Action, or Decision under a defined method.

Possible conceptual outcomes include:

```text
fully attributed
partially attributed
contributory
uncertain
not attributable
```

S101 does not mandate a universal attribution scale.

## Confounding

A confounder is a factor that influences both the presumed cause and the observed outcome, potentially creating a misleading causal association.

```text
C → O
↑   ↑
└─ X ─┘
```

The existence of an Action followed by an Outcome therefore does not prove that the Action produced the Outcome.

## Causal uncertainty

Causal conclusions may carry uncertainty independent of measurement uncertainty.

```text
Measurement uncertainty
    ≠
Causal uncertainty
```

An Observation may be precise while the causal attribution remains uncertain.

## Side effect

A Side Effect is an additional Outcome associated with an Action that was not the primary Intended Outcome.

Example:

```text
Action:
  reduce inventory

Intended Outcome:
  lower carrying cost

Side Effect:
  increased stockout risk
```

Side Effects may be positive, negative, or neutral depending on the domain objective.

## Unintended Outcome

An Unintended Outcome is a resulting condition that was not part of the intended result of the Decision or Action.

An Unintended Outcome is not necessarily a Side Effect in every domain model; Side Effect emphasizes the relationship to an Action, while unintendedness emphasizes the difference from intent.

## Delayed effect

An Effect may occur substantially later than the Action that contributed to it.

```text
Action A1
   │
   └──────────────→ Outcome R1
          delay
```

Causal models must not assume that effects occur immediately after actions.

This is especially relevant to:

```text
inventory policy changes
supplier development
capacity investment
network redesign
contract changes
```

## Feedback

Feedback is information about the result of prior Decisions or Actions that becomes input to subsequent evaluation or decision-making.

```text
Action
   ↓
Outcome
   ↓
Observation
   ↓
Evaluation
   ↓
Feedback
   ↓
Decision
```

Feedback is therefore a process relationship, not merely a numeric value.

## Feedback versus Outcome

An Outcome is what resulted from an Action or process.

Feedback is information returned to the decision process about that result.

```text
Outcome
   ↓ observed/interpreted as
Feedback
```

The same Outcome may generate different Feedback depending on objectives, context, and evaluation rules.

## Positive and negative feedback

`Positive` and `negative` feedback are context-dependent terms and should not automatically be interpreted as good or bad.

In control contexts they may describe whether feedback reinforces or counteracts a deviation.

A domain contract should define the intended meaning.

## Counterfactual semantics

Causal attribution often depends on a counterfactual question:

```text
What would have happened if Action A had not occurred?
```

An observed Outcome alone does not answer this question.

Counterfactual estimates, simulations, experiments, or analytical models may provide supporting evidence, but they remain distinct from the historical Observation.

## Intended versus observed result

Consider:

```text
Decision:
  increase safety stock from 100 to 150

Intended Outcome:
  service level reaches 98%

Actual Outcome:
  service level reaches 96.5%

Observation:
  measured service level = 96.5%
```

The distinction preserves the difference between planning intent and empirical result.

## Causal chain

A causal chain may be represented conceptually as:

```text
Condition C1
   ↓
Decision D1
   ↓
Action A1
   ↓
Intermediate Effect E1
   ↓
Outcome R1
   ↓
Observation O1
```

Each link may have different confidence and provenance.

## Multiple causes

An Outcome may have multiple contributing causes.

```text
Demand surge ─────┐
Supplier delay ───┼→ Stockout
Forecast error ───┘
```

A causal model should therefore not require a single root cause.

## Root cause versus contributing cause

A Root Cause is an explanatory cause designated as sufficiently fundamental under a particular analysis method.

A Contributing Cause is a factor that materially contributed without necessarily being designated the root cause.

These labels are analytical conclusions, not raw Observations.

## Causal provenance

Where causal assertions affect operational decisions, provenance should make it possible to distinguish:

```text
observed fact
inference
causal hypothesis
validated causal conclusion
```

This protects the ontology from treating an analyst's hypothesis as an observed fact.

## Relationship to Evidence

Observations can provide Evidence for a causal hypothesis, but evidence is not identical to causality.

```text
Observation
   ↓
Evidence
   ↓
Causal Hypothesis
   ↓
Analysis
   ↓
Causal Conclusion
```

The strength of the conclusion depends on the applicable analytical method.

## Relationship to Evaluation

Evaluation may determine whether an Outcome met an intended target, but evaluation alone does not establish why the Outcome occurred.

```text
Outcome
   ↓
Evaluation → met / failed

Outcome
   ↓
Causal Analysis → why
```

These are distinct questions.

## Relationship to Decision

A causal conclusion may inform a subsequent Decision, but it does not automatically determine the Decision.

```text
Causal Evidence
   ↓
Assessment
   ↓
Decision
```

Decision authority remains governed by S100 semantics.

## Historical Observation immutability

Subsequent causal analysis must not rewrite the historical Observation merely because a new causal explanation is discovered.

```text
Observation O1 = inventory 700

Later analysis:
  supplier delay contributed to excess inventory

O1 remains unchanged.
```

The causal interpretation is an additional semantic layer.

## No mandatory causal fields on Observation

S101 does not add fields such as:

```text
cause
effect
outcome
feedback
attribution
causal_confidence
root_cause
```

to the canonical Observation primitive.

These belong to causal relations, Outcome, Feedback, analysis, provenance, or domain-specific models.

## Non-goals

S101 does not define a universal causal inference algorithm, statistical causal model, root-cause-analysis framework, experiment design standard, counterfactual engine, or attribution scoring system.
