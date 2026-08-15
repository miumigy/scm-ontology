# S148 — Temporal / State / Event Semantics

S148 promotes the S106 temporal semantics into the machine-readable layer.

## Core distinction

```text
Event  = something that occurs
State  = condition that holds over validity time
Transition = event that connects a prior state to a subsequent state
```

An Event must not be serialized as a State, and a State must not be reconstructed merely from its latest stored value.

## Temporal kinds

The model keeps these meanings distinct:

- Effective — when a fact/state is semantically in force
- Transaction — when the record was captured/committed
- Observation — when the subject was observed
- Planned — intended future timing
- Scheduled — operationally assigned future timing
- Actual — timing of realized execution/occurrence

Therefore:

```text
Effective Time ≠ Transaction Time
Observation Time ≠ Effective Time
Planned Time ≠ Actual Time
Scheduled Time ≠ Actual Time
```

## Historical reconstruction

A State carries a validity interval and may carry a separate recording time. This allows a historical view to be reconstructed without overwriting prior truth.

```text
State(v1) --valid--> [t1, t2)
State(v2) --valid--> [t2, t3)
```

A later record of the earlier state does not change its effective interval.

## Transition

A transition is represented as an Event with explicit `from_state_ref` and `to_state_ref`. It is not itself a State.

```text
State A
   ↓
Transition Event
   ↓
State B
```

## Provenance

Events and states can carry provenance references. Temporal semantics therefore remain compatible with the S104 provenance model.

## Non-goals

S148 does not define:

- a database temporal table implementation;
- a particular event-stream platform;
- timezone policy;
- event sourcing as an implementation requirement.
