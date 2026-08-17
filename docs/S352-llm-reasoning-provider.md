# S352 — LLM Reasoning Provider

## Purpose

S352 connects an injected, transport-neutral language-model client to the S368
reasoning-provider boundary (Phase R2). It proves a large-language-model
provider can participate in the governed decision loop without coupling the
ontology to any specific vendor SDK.

The ontology does **not** import GPT, Claude, Gemini, or any other SDK. The
`LlmClient` boundary is supplied by the caller.

## Contract

`LLMReasoningProvider` wraps an injected `LlmClient` which exposes only:

- `provider_id` — the engine name;
- `complete(prompt) -> str` — raw model text for a prompt.

`build_reasoning_prompt(...)` constructs a deterministic prompt from the
`ReasoningInput` scope: `context_id`, observations, `evidence_ids`, and
`provenance_ids`. The provider requests a strict JSON response
(`proposal` object, `rationale` string, `confidence` in `[0, 1]`).

`parse_reasoning_response(...)` enforces the S343 output contract on the raw
model text:

- the response must be valid JSON (code fences tolerated);
- `proposal` must be non-empty;
- `rationale` must be a non-empty string;
- the output `context_id` is always the input `context_id`;
- evidence and provenance are always taken from the input scope, so a model
  that tries to invent identifiers is ignored;
- failures raise fail-closed rather than producing an ungrounded proposal.

## Non-goals

S352 does not:

- call a specific model vendor directly;
- hard-code a vendor API, key, or schema;
- mutate Canonical Truth or execute the resulting command;
- treat model output as truth, authorization, or execution.
