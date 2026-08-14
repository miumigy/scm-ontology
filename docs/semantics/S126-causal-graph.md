# S126 — Causal SCM Graph

S126 projects the S101 causal semantics into the SCM Graph.

## Core rule

A causal edge is a semantic claim, not merely a graph adjacency.

```text
Cause --causes--> Effect
```

The claim should retain provenance and causal uncertainty where applicable.

## Causal distinctions

- correlation is not causation
- attribution is not causation
- causal uncertainty is not absence of causality
- actual history is not counterfactual history

## Causal edge metadata

A causal relationship may carry:

- causal status
- confidence / uncertainty
- attribution reference
- confounding reference
- provenance reference
- validity interval
- scenario reference

## Counterfactual boundary

Counterfactual claims are represented in a Scenario distinct from the Actual World.

```text
Actual World
    └── observed effect

Counterfactual Scenario
    └── alternative cause / decision
         └── hypothetical effect
```

A counterfactual result must never overwrite an actual event, state, or outcome.

## Attribution boundary

Performance attribution can identify contribution to an outcome without asserting that the attributed factor is the sole causal mechanism.

## Graph traversal intent

The model should support questions such as:

- What caused this outcome?
- Which effects are downstream of this disruption?
- What evidence supports this causal claim?
- Which confounders were identified?
- How certain is the causal relationship?
- What would happen under an alternative decision?

## Non-goals

S126 does not implement a causal inference engine or statistical identification algorithm. It defines the semantic representation needed by later reasoning layers.
