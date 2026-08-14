# S135 — SCM State Engine

S135 defines the semantic contract for reconstructing and maintaining a canonical SCM state from events, observations, plans, commitments, and executions.

## State engine role

```text
Events / Observations / Plans / Executions
                  ↓
          State Reconstruction
                  ↓
            SCM State
                  ↓
      Observe → Diagnose → Plan → Decide
                  ↓
          Execute → Measure → Learn
```

The State Engine is a semantic layer, not an ERP transaction processor or workflow engine.

## State vs Event

- Event represents something that happened or was recorded.
- State represents the condition that holds for a scoped entity during a validity interval.

An event may cause a state transition, but the event and resulting state remain distinct.

## State dimensions

Canonical state should preserve, where applicable:

- subject/entity reference
- state type
- state value
- effective time / validity interval
- observation or transaction time
- scenario/world reference
- provenance references
- epistemic status

## Actual vs planned state

Planned, scheduled, committed, observed, measured, estimated, predicted, and actual states remain distinct semantic claims.

A plan must not overwrite actual history. A late-arriving observation may revise knowledge about a state without rewriting the historical event itself.

## State reconstruction

A historical state is reconstructed from temporally ordered events and observations plus the applicable semantic definitions. Reconstruction must retain provenance to the inputs used.

```text
Event(t1) → State(t1)
Event(t2) → State(t2)
Observation(t3) → State knowledge at t3
```

Transaction time and effective time remain separate.

## Scenario state

Scenario and counterfactual states are isolated from the actual world. A scenario may derive from an actual baseline, but scenario transitions cannot silently mutate actual state.

## Identity

State subjects reference canonical identities. Source-specific identifiers are resolved through the Identity / Resolution layer rather than embedded as competing canonical entities.

## State transitions

A transition may reference:

- prior state
- triggering event
- resulting state
- actor/system
- effective time
- evidence/provenance

A transition is not itself a Decision or Action, although a Decision or Action may trigger one.

## Uncertainty

If available evidence is insufficient to establish a state, the engine must preserve `unknown` or another epistemic status rather than infer a zero/default value.

## Non-goals

S135 does not define a persistence database, event-stream technology, workflow engine, or real-time architecture. It defines the canonical semantic contract needed by such implementations.
