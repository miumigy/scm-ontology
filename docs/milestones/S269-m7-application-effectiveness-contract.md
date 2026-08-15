# S269 — M7 Governance Decision Application Effectiveness Contract

## Purpose

Define how the effect of an applied Governance Decision is evaluated without converting observed downstream behavior into an automatic Canonical Fact.

## Effectiveness boundary

```text
Applied Governance Decision
        ↓
Subsequent Canonicalization Runs
        ↓
Observed Mapping Outcomes
        ↓
★ Effectiveness Assessment
        ↓
Review / Governance Signal
```

An Effectiveness Assessment evaluates adapter behavior against the approved decision scope. It does not establish the truth of the underlying business reality.

## Assessment identity

An assessment SHOULD preserve:

- `assessment_id`
- `decision_id`
- effective configuration version
- observed execution references
- assessment scope
- assessment criteria
- assessment result
- assessed_at

The assessment MUST remain traceable to the applied Governance Decision and the executions from which observations were obtained.

## Assessment outcomes

An assessment MAY classify the observed application as:

- `effective`
- `partially_effective`
- `ineffective`
- `inconclusive`
- `not_evaluable`

An outcome MUST be interpreted within the approved scope and criteria. It MUST NOT be generalized to unrelated enterprise representations.

## Evidence boundary

Observed mapping outcomes are evidence about adapter behavior. They MAY support a Governance Signal or a subsequent controlled review.

They MUST NOT automatically become Canonical Facts merely because the mapping produced a stable or successful result.

## Canonical Truth boundary

Effectiveness assessment:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts;
- MUST NOT infer a canonical fact from effectiveness alone;
- MUST NOT rewrite historical audit records;
- MUST NOT silently alter the approved Governance Decision or its scope.

A finding that an approved mapping is ineffective is a governance signal, not permission to silently replace the mapping.

## Change control

If an assessment indicates that the approved mapping should change, the change MUST proceed through a new controlled Governance Decision. The original decision and its application history remain intact.

## Explainability

An assessment SHOULD identify the observed executions, criteria, relevant versions, scope, and evidence supporting its outcome. `inconclusive` and `not_evaluable` outcomes SHOULD state why the available evidence was insufficient.

## Non-goals

S269 does not define automated optimization, automatic rule replacement, Canonical Fact ingestion, ontology learning, vendor connectors, or graph mutation.
