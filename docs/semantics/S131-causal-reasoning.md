# S131 — Causal Reasoning

S131 defines how a causal claim may be evaluated without collapsing correlation, attribution, uncertainty, or counterfactuals into facts.

## Reasoning contract

```text
Causal Graph
  + Evidence
  + Context
  + Causal Claim
       ↓
Causal Assessment
       ↓
Supported | Unsupported | Uncertain | Confounded | Not Assessable
```

A causal assessment is not itself a Decision.

## Claim boundary

A causal claim must identify:

- cause reference
- effect reference
- causal relationship reference
- evidence references
- temporal/context scope
- uncertainty/confounding information where known

## Evidence strength

Evidence supports a claim but does not automatically make the claim true. A missing or weak evidence basis should result in `uncertain` or `not_assessable`, not fabricated certainty.

## Attribution boundary

Attribution can describe contribution to an outcome. It must not be silently promoted to a causal claim.

```text
Attribution
    ≠
Causation
```

## Confounding

A known or suspected confounder remains explicit in the assessment. The existence of a confounder does not prove that the proposed cause is false; it limits causal certainty unless appropriately addressed.

## Temporal ordering

Causal reasoning must respect temporal ordering. A proposed cause cannot semantically occur after the effect it is claimed to cause within the same causal context.

## Counterfactual boundary

Counterfactual reasoning remains scenario-scoped:

```text
Actual Cause → Actual Effect

Alternative Cause / Decision
        ↓
Counterfactual Scenario
        ↓
Hypothetical Effect
```

Counterfactual assessment must not rewrite actual history.

## Provenance

Causal assessments retain provenance to the evidence and causal claim. This enables later explanation and audit.

## Non-goals

S131 does not implement statistical causal inference, econometrics, machine-learning causal discovery, or a universal identification algorithm. It defines the semantic contract for representing and assessing causal claims so those implementations can remain replaceable.
