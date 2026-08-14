# S99 — Exception Lifecycle & Resolution Semantics

S99 defines the lifecycle semantics of operational Exceptions and separates lifecycle management from the historical Observation, Evaluation, Alert, and Incident that may have contributed to the Exception.

## Canonical decision

An Exception is an operational artifact with its own lifecycle. Resolving or closing an Exception does not modify the historical Observation or Evaluation that originated it.

```text
Historical Observation
        │
        ▼
     Evaluation
        │
        ▼
     Exception
        │
        ▼
  operational lifecycle
```

The canonical Observation primitive remains unchanged.

## Lifecycle is separate from Observation state

A useful conceptual lifecycle is:

```text
Detected
   ↓
Opened
   ↓
Acknowledged
   ↓
Assigned
   ↓
Investigating
   ↓
Mitigating
   ↓
Resolved
   ↓
Closed
```

This is a reference lifecycle, not a mandatory universal state machine.

A domain may omit, combine, repeat, or add states while preserving the semantic distinction between the source observation and the operational case.

## Detected

`Detected` indicates that a condition has been identified by a rule, system, person, or external source.

Detection does not necessarily mean that an Exception has been formally opened.

```text
condition detected
    ↓
possible Exception creation
```

## Opened

`Opened` indicates that an Exception case has been created or formally entered into an operational workflow.

Opening an Exception does not alter the Observation that caused it.

## Acknowledged

`Acknowledged` indicates that the Exception has been recognized by an assigned operational actor or process.

Acknowledgement is not resolution.

```text
acknowledged
    ≠
resolved
```

## Assigned

`Assigned` identifies that responsibility for investigation or response has been allocated to an actor, team, role, or workflow.

Ownership may change during the lifecycle.

## Investigating

`Investigating` indicates that the cause, scope, impact, or appropriate response is being assessed.

Investigation may determine that the original evaluation was correct, incorrect, incomplete, or no longer operationally relevant. Such findings should not rewrite immutable historical observations.

## Mitigating

`Mitigating` indicates that actions are being taken to reduce the impact or restore an acceptable operating condition.

Mitigation does not imply that the root cause has been eliminated.

## Resolved

`Resolved` indicates that the operational condition represented by the Exception satisfies the applicable resolution criteria.

Resolution is contextual to the Exception and its rule/process.

```text
Exception resolved
    ≠
source Observation changed
```

For example:

```text
Inventory Observation = 700
Upper limit = 500
Exception = excess inventory

Later inventory = 480
Exception → resolved

Historical Observation = 700 remains unchanged
```

## Closed

`Closed` indicates that the Exception lifecycle has been formally completed according to the applicable process.

Closure may require additional criteria beyond the operational condition being resolved, such as documentation, approval, or verification.

Therefore:

```text
resolved
    ≠ necessarily closed
```

## Reopen

A previously resolved or closed Exception may be reopened when the condition recurs, resolution criteria are invalidated, or new evidence requires renewed investigation.

Reopening creates a new lifecycle transition; it does not change the historical fact that the Exception was previously resolved or closed.

## Recurrence

Repeated occurrences of a condition must not automatically overwrite the previous Exception.

Possible models include:

```text
one Exception
  └─ multiple occurrences

or

Exception 1
Exception 2
Exception 3
```

The applicable domain/process contract determines whether recurrence is modeled as repeated occurrences of one case or as separate cases.

## Root cause

Root cause is an investigative conclusion about why an Exception occurred or persisted.

It is not equivalent to the triggering Observation.

```text
Observation
   ↓
Evaluation
   ↓
Exception
   ↓
Investigation
   ↓
Root Cause
```

Root cause may remain unknown even after an Exception is resolved.

## Corrective action

A Corrective Action is an operational intervention intended to remove or reduce a cause of an Exception.

```text
Exception
   ↓
Corrective Action
   ↓
Condition improved
```

A corrective action is not the same as resolution, and resolution does not prove that the corrective action eliminated the root cause.

## Containment versus correction

Operational response may distinguish:

```text
Containment
  = limit immediate impact

Corrective Action
  = address an identified cause or mechanism

Preventive Action
  = reduce likelihood of recurrence
```

S99 does not mandate these as separate workflow objects, but preserves the semantic distinction where the domain requires it.

## SLA and response timing

Exception lifecycle may have service-level expectations such as:

```text
detection-to-acknowledgement
acknowledgement-to-assignment
assignment-to-mitigation
mitigation-to-resolution
resolution-to-closure
```

These durations are lifecycle metrics, not Observation timestamps.

The original Observation's `observed_at` remains distinct from:

```text
detected_at
opened_at
acknowledged_at
assigned_at
resolved_at
closed_at
```

## Ownership

Ownership may change over the lifecycle.

```text
Exception
  ↓
Team A
  ↓
Team B
  ↓
Team C
```

Historical ownership transitions should remain auditable where required.

## Resolution reason

A resolution should have an interpretable reason when the domain requires auditability.

Examples:

```text
condition corrected
condition naturally recovered
false positive
rule superseded
duplicate
accepted risk
external dependency resolved
```

A resolution reason is not itself a modification to the source Observation.

## Verification

Resolution may require verification before closure.

```text
Mitigated
   ↓
Verification
   ↓
Resolved
   ↓
Closed
```

The verification rule is domain-specific.

## False positive

An Exception may be determined to have been incorrectly triggered.

A false-positive resolution should preserve the fact that the Exception was generated under the then-applicable rule/context.

The historical Evaluation should not be silently rewritten merely because subsequent investigation reached a different conclusion.

## Rule versioning

S97 and S98 establish that evaluation rules may be versioned.

An Exception should retain or reference the relevant Evaluation and rule/version when reproducibility matters.

```text
Observation O1
Rule v1
Evaluation = breach
Exception E1

Rule v2 later changes

E1 remains historically linked to Rule v1
```

## Alert relationship

An Alert may be generated from an Exception, but alert delivery and alert lifecycle are separate from Exception lifecycle.

```text
Exception
   ├─ Alert A1
   ├─ Alert A2
   └─ no alert
```

An Alert may be suppressed, deduplicated, or acknowledged without changing the Exception's historical lifecycle.

## Incident relationship

An Exception may contribute to an Incident, and one Incident may aggregate multiple Exceptions.

```text
Exception E1 ─┐
Exception E2 ─┼─→ Incident I1
Exception E3 ─┘
```

The relationship is domain/process-specific and does not imply that Exception and Incident are synonyms.

## Evidence and auditability

Lifecycle transitions, ownership changes, resolution reasons, and verification evidence may be retained as operational provenance.

This information should support reconstruction of:

```text
what happened
when it happened
under which rule
who responded
what changed
why it was resolved
```

without rewriting the source Observation.

## No mandatory lifecycle fields on Observation

S99 does not add fields such as:

```text
exception_status
assigned_to
resolved_at
root_cause
resolution_reason
sla_status
```

to the canonical Observation primitive.

These belong to Exception, operational workflow, incident, action, or audit models.

## Non-goals

S99 does not define a universal ITSM/ITIL lifecycle, SLA policy, root-cause-analysis method, workflow engine, escalation matrix, incident taxonomy, or mandatory Exception state machine.
