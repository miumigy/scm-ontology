# S143 — Semantic Integrity Reconciliation

S143 reconciles the canonical registry with the semantic contracts established through S142 before further machine-readable expansion.

## Why S143 exists

S113–S115 established the canonical registry, type/value semantics, and identity/reference semantics. S100–S142 subsequently clarified the SCM OS loop and introduced explicit boundaries for Recommendation, Decision, Action, Execution, Measurement, Performance Assessment, and Learning.

The registry must reflect those boundaries before it becomes the authoritative machine-readable source.

## Canonical lifecycle

```text
Recommendation
      ↓ informs
Decision
      ↓ authorizes
Action
      ↓ execution_of
Execution
      ↓ results_in
Outcome
      ↓ measured through
Observation → Measurement → Metric / KPI
      ↓
Performance Assessment
      ↓
Learning Result
      ↓ updates
Knowledge / Assumption / Policy / Rule / Model / Decision Context
```

These are distinct semantic objects. A relationship between them does not collapse their identities.

## Critical reconciliations

### Action vs Execution

Action expresses intended intervention. Execution records carrying it out.

`Action ≠ Execution`

The canonical registry must not describe Action as already executed.

### Recommendation vs Decision

Recommendation suggests an option; Decision selects or authorizes a course.

`Recommendation ≠ Decision`

### Execution vs Outcome

Execution records the execution process. Outcome records what resulted.

`Execution ≠ Outcome`

A completed execution does not imply a successful outcome.

### Measurement vs Performance

Measurement records observed/measured value. Performance Assessment evaluates it against an explicit reference basis.

`Measurement ≠ Performance Assessment`

### Learning vs Policy/Model

Learning records an explicit change in knowledge or decision context. Any resulting policy, rule, or model update remains a separate object with its own lineage and effective time.

`Learning ≠ Policy ≠ Rule ≠ Model`

## Layer integrity

The registry continues to distinguish:

- `primitive`: semantic building blocks
- `core`: reusable SCM concepts
- `derived`: concepts whose meaning depends on other concepts or calculations
- `contextual`: identity, provenance, evidence, scenario, and other semantic context

Derived metrics must not become primitives merely because they are commonly used KPIs.

## Relationship integrity

Every canonical relationship has:

- predicate
- source concept
- target concept
- semantic category

Relationships do not encode vendor-specific implementation behavior.

## Planned / actual / epistemic integrity

The registry does not encode Planned, Scheduled, Promised, Committed, Actual, Observed, Estimated, Predicted, Inferred, or Counterfactual merely as datatype labels. Their semantic distinctions remain supplied by the surrounding S101–S142 contracts.

## Exit criteria

S143 is complete when the canonical registry:

1. contains the concepts required by the closed-loop semantics;
2. preserves Recommendation/Decision/Action/Execution/Outcome boundaries;
3. preserves Measurement/Performance/Decision boundaries;
4. represents Learning without collapsing it into its update target;
5. exposes canonical relation signatures for those transitions;
6. remains independent of JSON, RDF, Neo4j, SQL, or vendor schemas.

S143 intentionally does not define a final serialized schema. That remains the responsibility of the machine-readable ontology milestone.
