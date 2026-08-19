# S362 — Distribution Decision Application

## Purpose

S362 is an **SCM Application** milestone (Phase R5). It resolves a shipment
requirement against available transportation capacity into a distribution
decision and, when shipment is feasible, drives it through the governed loop
to an authorized `ExecutionCommand` and an S353 dry run.

It reuses the S348 governed loop, the S351 rule-based provider, and the S353
execution runtime. It reuses the canonical shipment concept
(`CanonicalShipment`) for physical movement of items between origin and
destination locations. It introduces no new canonical semantics and performs
no external side effect.

Together with S358 (replenishment), S360 (procurement), and S361 (production),
S362 completes the first **Phase R5 application set** across the physical
material flow: replenish -> procure -> produce -> distribute.

## Contract

`run_distribution_application(observation, *, context_id, actor_id, authority,
authorized_at, command_id, dry_ran_at, adapter)` accepts a
`DistributionObservation` (shipment id, item, required quantity, transportation
capacity, origin/destination location, unit, evidence, provenance) and returns
an immutable `DistributionDecision` with `contract_version: S362.1`.

When the shipment requirement **exceeds** transportation capacity
(infeasible), the application returns an `escalate` decision with no command
and no dry run. When the requirement is within capacity (feasible, including
exact fit), it builds a deterministic rule provider
(`ship-within-capacity`) and runs the full governed loop:

```text
observation -> ReasoningInput -> Rule provider -> ReasoningOutput
    -> Validation -> Authorization -> Command -> Dry Run -> Result
```

## Fail-closed behavior

The application MUST reject:

- empty shipment/item/unit/origin/destination or missing context;
- identical origin and destination;
- non-numeric or negative required/capacity;
- a value that is not a `DistributionObservation`.

It returns `escalate` without creating a command when the requirement is not
feasible.

## Non-goals

S362 does not:

- mutate Canonical Truth or external systems;
- physically move, dispatch, or deliver goods;
- allocate vehicles or optimize routes;
- negotiate carrier selection or freight terms;
- execute the command.
