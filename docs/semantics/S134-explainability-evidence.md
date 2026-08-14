# S134 — Explainability / Evidence

S134 defines how SCM reasoning results remain explainable, auditable, and traceable from source evidence through evaluation to recommendation and decision.

## Reasoning chain

```text
Source / Evidence
      ↓
Observation / Measurement
      ↓
Provenance / Derivation
      ↓
Evaluation
      ↓
Causal / What-if Assessment
      ↓
Recommendation
      ↓
Decision
      ↓
Action
      ↓
Outcome / Measurement
```

The chain is a traceability model, not a claim that every decision must have every intermediate node.

## Explanation vs Evidence

Evidence supports a claim or reasoning step. An Explanation describes how inputs, rules, constraints, assumptions, or assessments contributed to a result.

```text
Evidence ≠ Explanation
Provenance ≠ Explanation
Explanation ≠ Decision
```

An explanation must not invent evidence that is absent from the provenance chain.

## Evidence roles

Evidence may be associated with a reasoning step using an explicit role, for example:

- supporting
- contradicting
- contextual
- derived
- baseline
- scenario-input

Evidence strength or authority remains separate from the evidence object itself.

## Reasoning trace

A reasoning trace identifies the material inputs and intermediate assessments used to produce a result.

It may reference:

- source identities
- observations
- measurements
- metric values
- constraints and evaluations
- causal assessments
- what-if results
- alternatives
- recommendations
- decisions

The trace should preserve order where order is semantically meaningful.

## Epistemic preservation

The explanation layer must preserve the epistemic status of inputs and results.

```text
Observed → observed
Estimated → estimated
Predicted → predicted
Simulated → simulated
Inferred → inferred
Unknown → unknown
```

It must not transform an inference into a Fact merely because it appears in an explanation.

## Decision explanation

A Decision may reference a Recommendation and its supporting reasoning, but the existence of a Recommendation does not prove that the Decision followed it.

```text
Recommendation
      ↓ considered_by
Decision
```

is distinct from:

```text
Recommendation
      ↓ became
Decision
```

unless the canonical data explicitly establishes that relationship.

## Counterfactual explanation

A what-if result remains scenario-scoped. Explanations may compare actual and hypothetical outcomes, but must not merge them into one historical result.

## Causal explanation

A causal assessment may be included in an explanation. Its uncertainty, confounders, and evidence references remain visible.

```text
Causal Assessment
  ├─ Evidence
  ├─ Confounders
  └─ Uncertainty
```

The explanation must not upgrade a causal hypothesis into a proven causal fact.

## Reproducibility

Where available, a reasoning trace should retain enough references to reconstruct the relevant reasoning context:

- input references
- semantic definition/version
- rule/constraint references
- scenario reference
- model/method reference
- timestamps
- provenance references

Reproducibility does not require a specific implementation technology.

## Non-goals

S134 does not define a natural-language explanation generator, UI, LLM prompt format, or mandatory evidence scoring algorithm. Those are implementation layers above the canonical semantics.
