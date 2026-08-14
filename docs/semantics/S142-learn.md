# S142 — Learn

S142 defines the SCM OS Learn semantic: using observed outcomes and evaluated evidence to produce an explicit learning result that may update knowledge, assumptions, policies, rules, models, or future decision context without rewriting historical truth.

## Learn contract

```text
Measure
   ↓
Outcome / Performance
   ↓
Evidence + Diagnosis
   ↓
Learning Assessment
   ↓
Knowledge / Assumption / Policy / Rule / Model Update
   ↓
Future Observe → Diagnose → Plan → Decide
```

Learning is an explicit semantic act or result of incorporating evidence into future knowledge or decision context. A historical record, inference, or observation is not automatically a learning result.

## Core boundaries

- Observation ≠ Learning
- Measurement ≠ Learning
- Inference ≠ Learning
- Hypothesis ≠ Learning
- Learning ≠ Outcome
- Learning ≠ Decision
- Learning ≠ Policy
- Learning ≠ Rule
- Learning ≠ Model
- Historical truth ≠ Updated knowledge

A learning result may lead to a Decision or update a Policy/Rule/Model, but these remain separate concepts.

## Learning context

A learning record should preserve, where applicable:

- subject and scope
- source evidence references
- outcome / performance references
- diagnosis or causal assessment references
- prior knowledge / assumption / model references
- learned conclusion or change
- affected knowledge target
- confidence / uncertainty
- effective time
- learning time
- provenance
- scenario or world scope

## What changed

Learning should describe the semantic delta where possible:

```text
Prior Knowledge / Assumption / Model
              ↓
        New Evidence
              ↓
        Learning Result
              ↓
Updated Knowledge / Assumption / Model
```

The previous state is retained and the update is lineage-linked. Learning does not silently mutate historical observations, decisions, executions, or outcomes.

## Evidence does not equal learning

A new Measurement may contradict a prior expectation. That contradiction is evidence; learning occurs only when the evidence is incorporated into a revised understanding, assumption, model, policy, or other explicitly identified knowledge target.

```text
Evidence → Assessment → Learning
```

The intermediate assessment remains traceable.

## Learning and causality

A learning result may reference causal assessment, but causal attribution must remain distinct from learning. The model must not infer causality merely because an outcome followed an action.

## Learning and uncertainty

Learning may increase, decrease, or redirect confidence. It must preserve uncertainty when evidence is incomplete or conflicting. A learned conclusion is not necessarily a Fact.

## Learning and policy / rule / model updates

A learning result can propose or justify an update to a Policy, Rule, Assumption, or Model. The update itself remains a separate semantic object and requires its own provenance and effective-time semantics.

```text
Learning
   ↓ informs
Policy / Rule / Model Change
   ↓ affects
Future Decision / Plan
```

This prevents the system from treating every learned insight as immediately authoritative.

## Scenario and counterfactual learning

Learning derived from a Scenario or Counterfactual remains scoped to that world unless explicitly adopted into actual-world knowledge. Simulated success is not actual-world evidence.

## Closed-loop connection

```text
Observe
  ↓
Diagnose
  ↓
Plan
  ↓
Decide
  ↓
Execute
  ↓
Measure
  ↓
Learn
  ↺
```

Learn closes the semantic loop by making experience reusable while preserving provenance, temporal history, epistemic status, and the distinction between evidence and interpretation.

## Non-goals

S142 does not define machine-learning algorithms, model-training pipelines, reinforcement-learning implementations, knowledge-graph storage, or organizational knowledge-management workflows. It defines the canonical semantics of learning as an SCM OS loop operation.
