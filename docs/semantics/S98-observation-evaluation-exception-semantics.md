# S98 — Observation Evaluation & Exception Semantics

S98 defines the semantic boundary between an Observation, an evaluation result, an operational alert, an exception, an incident, and escalation.

## Canonical decision

Evaluation, Exception, Alert, Incident, and Escalation are distinct semantic artifacts. None is an intrinsic identity attribute of an Observation.

```text
Observation / Comparison Result
          │
          ▼
      Evaluation
          │
          ├─ normal
          ├─ warning
          └─ breach
          │
          ▼
   Exception / Alert / Incident
          │
          ▼
      Escalation / Action
```

The canonical Observation primitive remains unchanged.

## Evaluation

An Evaluation applies an explicit rule to an Observation or derived comparison result.

```text
input
rule
condition
outcome
```

For example:

```text
Inventory = 700
Upper limit = 500
        ↓
Evaluation = breach
```

The breach is an evaluation outcome, not a mutation of the inventory Observation.

## Normal

`Normal` indicates that an evaluated condition satisfies the applicable rule.

Normal is contextual to the rule being applied.

```text
inventory = 480
upper_limit = 500
→ normal
```

The same Observation could be normal under one rule and a warning or breach under another rule.

## Warning

A Warning is an operational evaluation outcome indicating a condition that may require attention without necessarily constituting a formal exception or incident.

```text
Evaluation
    ↓
warning
```

A warning does not inherently require escalation.

## Breach

A Breach indicates that an evaluated rule condition has been violated.

```text
inventory = 700
upper_limit = 500
→ breach
```

A breach may produce an Exception, Alert, Incident, or no further operational object depending on the applicable domain/process rules.

## Exception

An Exception is an operational representation that a condition requires attention because it deviates from an expected, permitted, or controlled state.

An exception is therefore broader than a numerical breach.

Examples may include:

```text
service-level breach
unexpected demand pattern
missing critical data
transport disruption
capacity constraint
```

An Exception may originate from an Evaluation, but not every Evaluation result must become an Exception.

## Alert

An Alert is a notification or signaling artifact intended to make a condition visible to a person, system, or workflow.

```text
Breach
  ↓
Alert
```

is one possible process, but an Alert is not synonymous with a Breach.

An Alert may be generated from a warning, anomaly, operational rule, or other trigger.

## Incident

An Incident is an operational event or case requiring coordinated management according to a defined process.

An incident normally has stronger operational semantics than an alert:

```text
Alert
  → may contribute to
Incident
```

but neither transition is universal.

An Incident may also originate from human assessment or external operational events rather than directly from an Observation Evaluation.

## Escalation

Escalation is a process transition in which responsibility, priority, notification scope, or response level is increased.

```text
Exception
    ↓ escalation rule
higher response level
```

Escalation is not a property of the Observation and is not identical to an Alert or Incident.

## Evaluation outcome versus operational object

S98 explicitly separates analytical evaluation from operational management.

```text
Evaluation outcome
    = semantic judgment under a rule

Exception
    = operational deviation requiring attention

Alert
    = signal / notification

Incident
    = managed operational case

Escalation
    = change in response level
```

These may be linked, but they should not be collapsed into one generic `status` field.

## Not every breach is an exception

A breach may be intentionally tolerated, already acknowledged, or outside an operational workflow.

Therefore:

```text
breach
  ≠ automatically exception
```

The applicable operational policy determines whether and how a breach becomes an Exception.

## Not every exception is an observation breach

Exceptions can originate from non-observational conditions.

Examples:

```text
missing required master data
workflow failure
policy violation
supplier notification
external disruption
```

An Exception model must therefore not require an Observation as its only possible source.

## Alert deduplication and suppression

Operational systems may suppress, group, deduplicate, or throttle Alerts.

Such behavior does not alter the underlying Observation or Evaluation.

```text
Observation
   ↓
Evaluation = breach
   ↓
Alert generated
   ↓
suppressed / deduplicated
```

The suppression of an Alert does not mean that the evaluated condition did not occur.

## Acknowledgement and resolution

An operational Exception, Alert, or Incident may have lifecycle states such as:

```text
open
acknowledged
in_progress
resolved
closed
```

These are lifecycle semantics of the operational artifact, not states of the source Observation.

Resolution of an Exception does not rewrite the historical Observation that caused it.

## Temporal semantics

The following times may differ:

```text
observed_at
recorded_at
identified_at
evaluated_at
alerted_at
acknowledged_at
resolved_at
```

S86 and S92 temporal semantics remain applicable. An operational response time must not overwrite the domain time of the original Observation.

## Rule versioning

S97 establishes that evaluation rules may change over time.

Therefore an Evaluation should retain or reference the applicable rule/version when reproducibility matters.

```text
Observation O1 = 102
Rule v1 → normal
Rule v2 → breach
```

The change in outcome is attributable to the evaluation context, not to a change in O1.

## Relationship to State

An Evaluation or Exception may trigger a State transition, but the artifacts remain distinct.

```text
Observation
   ↓
Evaluation
   ↓
Exception
   ↓
State transition
```

A State represents the applicable condition of a domain entity or process; an Exception represents an operational deviation requiring attention.

## Relationship to Claim and Evidence

An Evaluation or Exception may provide Evidence for a Claim, but neither automatically becomes a Claim.

```text
Observation
   ↓
Evaluation / Exception
   ↓
Evidence
   ↓
Claim / Decision
```

Epistemic and operational semantics remain separate.

## No mandatory status field on Observation

S98 does not add fields such as:

```text
status
alert_level
exception
incident
escalated
```

to the canonical Observation primitive.

These belong to evaluation, operational workflow, incident, or exception-management models.

## Non-goals

S98 does not define a universal incident-management framework, alert severity taxonomy, escalation matrix, workflow engine, ITIL mapping, or exception-management product model.
