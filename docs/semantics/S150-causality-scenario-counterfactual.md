# S150 — Causality / Scenario / Counterfactual Schema

S150 promotes S101 and S102 semantics into the machine-readable layer.

## Causality

A causal relationship explicitly connects a cause to an effect. It may carry evidence and causal uncertainty.

```text
Cause ──causes/contributes_to/prevents/modifies──> Effect
```

The ontology does not equate causal attribution with causation, and does not infer causation merely from correlation.

## Scenario

A scenario is an alternative modeled world anchored to a parent world. The actual world is not itself represented as a scenario.

```text
Actual World
   ├── Alternative Scenario
   ├── Hypothetical Scenario
   └── Counterfactual Scenario
```

A scenario can explicitly record assumptions and changes from its parent world.

## Counterfactual

A counterfactual compares an observed outcome with an alternative outcome under an explicit intervention and causal basis.

```text
Observed World
   ↓ intervention
Counterfactual Scenario
   ↓
Counterfactual Outcome
```

Therefore:

- Counterfactual ≠ Forecast
- Counterfactual ≠ Actual History
- Scenario ≠ Actual World
- Alternative Decision ≠ Executed Decision
- Causal Relationship ≠ Correlation

## Integration

S150 references, rather than duplicates, the existing S146 value semantics, S148 temporal semantics, and S149 evidence/provenance semantics.

A future reasoning engine can therefore distinguish:

```text
Observed fact
   ↓
Causal hypothesis / relationship
   ↓
Scenario intervention
   ↓
Counterfactual outcome
```

without silently converting a modeled alternative into historical fact.

## Non-goals

S150 does not implement a causal discovery algorithm, forecast model, simulation engine, optimizer, or probabilistic inference engine. Those are consumers of the canonical semantic model.
