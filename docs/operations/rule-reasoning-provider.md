# S351 — Rule-Based Reasoning Provider

## Purpose

S351 is the first **Real Reasoning Provider** milestone (Phase R2). It
implements the S368 reasoning-provider boundary with a deterministic,
side-effect-free rule engine, so a governed decision can be produced from
explicit rules rather than a fixed mock proposal.

It introduces no new canonical semantics. The provider consumes the same
`ReasoningInput` (S342) and returns the same `ReasoningOutput` (S343) as the
S348 mock provider.

## Contract

A `RuleReasoningProvider` holds an ordered, immutable set of `ReasoningRule`
values. Each rule carries:

- `rule_id` — auditable identity (unique within a provider);
- `proposal` — the machine-readable proposed result;
- `rationale` — explicit explanation;
- `matches` — a pure predicate over the input observations;
- `condition_description` — human-readable condition for audit;
- `confidence` — optional numeric confidence in `[0, 1]`.

Rules are evaluated in declaration order. The first rule whose predicate
matches the `ReasoningInput` observations fires and produces the
`ReasoningOutput`, preserving the input `context_id`, `evidence_ids`,
and `provenance_ids`. `when_measurement_below(...)` provides a reusable,
auditable condition builder for threshold checks.

## Fail-closed behavior

When no rule matches, the provider **MUST NOT** invent a proposal. It raises,
and the S368 boundary normalizes the failure so the governed loop (S348) stops
rather than proposing an ungrounded action.

## Non-goals

S351 does not:

- infer rules from data or history;
- evaluate probabilities or optimize;
- call LLM, ERP, WMS, TMS, or other external systems;
- mutate Canonical Truth or execute the resulting command.
