# S137 — Diagnose

S137 defines the SCM OS Diagnose semantic: turning observed state, performance deviation, exceptions, and evidence into an explicit diagnostic assessment without confusing diagnosis with cause, decision, or action.

## Diagnose contract

```text
Observe
  ↓
State / Measurement / Metric / KPI
  ↓
Deviation / Exception
  ↓
Evidence + Causal Assessment + Context
  ↓
Diagnosis
  ↓
Recommendation / Decision
```

Diagnosis is an assessment of a condition or explanation of an observed deviation. It is not itself a Decision or Action.

## Core boundaries

- Observation ≠ Diagnosis
- Deviation ≠ Cause
- Exception ≠ Diagnosis
- Diagnosis ≠ Causal Fact
- Diagnosis ≠ Recommendation
- Recommendation ≠ Decision
- Decision ≠ Action

A diagnosis may contain one or more candidate causes and an uncertainty assessment. A suspected cause must not be represented as proven causation without adequate causal evidence.

## Diagnostic subject

A Diagnosis may apply to a canonical entity, relationship, process, state, metric, KPI, or scenario-scoped object. The subject and scope must remain explicit.

## Deviation and exception

Deviation describes a difference from a reference such as target, baseline, plan, benchmark, threshold, or expected value.

Exception identifies a condition requiring attention according to an applicable threshold, rule, policy, or context.

Neither implies a root cause.

```text
Target / Baseline / Expected
          ↓ compare
Observed / Actual
          ↓
       Deviation
          ↓ threshold/policy
       Exception
```

## Causal assessment

S131 causal assessments may support a Diagnosis. The diagnostic object should retain references to causal assessments, evidence, and competing hypotheses where available.

```text
Diagnosis
 ├─ evidence
 ├─ causal assessments
 ├─ hypotheses
 └─ uncertainty
```

## Multiple causes

SCM problems are frequently multi-causal. The model must allow multiple candidate causes and causal relationships rather than forcing a single root-cause field.

## Epistemic status

Diagnosis must preserve whether it is observed, inferred, hypothesized, estimated, or otherwise uncertain. A diagnostic statement does not become a Fact merely because it is operationally useful.

## Temporal scope

Diagnosis must identify the relevant period or state context when known. Historical diagnosis must not rewrite historical events or states.

## Scenario diagnosis

A Diagnosis may be scoped to a Scenario or Counterfactual. Such a diagnosis remains hypothetical and must not be merged with an actual-world diagnosis.

## Explainability

S134 reasoning traces and evidence references may support a Diagnosis so that downstream Recommendation and Decision objects can explain why the condition was assessed as significant and what evidence supported candidate causes.

## Non-goals

S137 does not define a root-cause-analysis algorithm, statistical test, anomaly-detection engine, workflow, or LLM diagnosis prompt. Those are implementation methods above the canonical semantic layer.
