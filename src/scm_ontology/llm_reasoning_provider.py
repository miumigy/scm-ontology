"""LLM-backed S368 reasoning provider (Phase R2).

This module connects an injected, transport-neutral ``LlmClient`` to the
existing reasoning-provider boundary. It does **not** import or depend on any
specific LLM SDK, so GPT, Claude, Gemini, or other engines can be supplied by
the caller without changing the ontology. The wrapper builds a deterministic
prompt from the ``ReasoningInput``, parses the model's JSON response, and
enforces the S343 output contract fail-closed.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any, Protocol

from .reasoning_input import ReasoningInput
from .reasoning_output import ReasoningOutput


class LlmProviderError(ValueError):
    """Raised when an LLM provider cannot produce a conformant reasoning output."""


class LlmClient(Protocol):
    """Minimal injected boundary to an external language model.

    Implementations supply ``provider_id`` (the engine name) and ``complete``,
    which returns raw model text for a prompt. No SDK is imported here.
    """

    provider_id: str

    def complete(self, prompt: str) -> str: ...


def build_reasoning_prompt(reasoning_input: ReasoningInput) -> str:
    """Build a deterministic prompt that fully scopes the request to the input."""
    observations = [
        {
            "question_id": observation.question_id,
            "value": observation.value,
            "evidence_ids": list(observation.evidence_ids),
            "provenance_ids": list(observation.provenance_ids),
        }
        for observation in reasoning_input.observations
    ]
    payload = {
        "context_id": reasoning_input.context_id,
        "observations": observations,
        "evidence_ids": list(reasoning_input.evidence_ids),
        "provenance_ids": list(reasoning_input.provenance_ids),
    }
    instruction = (
        "Propose a single SCM decision as strict JSON with exactly these keys: "
        "proposal (object), rationale (string), confidence (number in [0,1]). "
        "Do not invent evidence. Return only JSON."
    )
    return instruction + "\n" + json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise LlmProviderError(f"model response was not valid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise LlmProviderError("model response must be a JSON object")
    return parsed


def parse_reasoning_response(reasoning_input: ReasoningInput, raw: str) -> ReasoningOutput:
    """Parse and enforce the S343 contract on a model's raw response."""
    parsed = _extract_json(raw)
    proposal = parsed.get("proposal")
    rationale = parsed.get("rationale")
    confidence = parsed.get("confidence")

    if proposal is None or (isinstance(proposal, str) and not proposal.strip()):
        raise LlmProviderError("proposal must be non-empty")
    if not isinstance(rationale, str) or not rationale.strip():
        raise LlmProviderError("rationale must be a non-empty string")
    if confidence is not None and not isinstance(confidence, (int, float)):
        raise LlmProviderError("confidence must be a number")

    try:
        return ReasoningOutput(
            context_id=reasoning_input.context_id,
            proposal=proposal,
            rationale=rationale,
            evidence_ids=reasoning_input.evidence_ids,
            provenance_ids=reasoning_input.provenance_ids,
            confidence=float(confidence) if confidence is not None else None,
        )
    except Exception as exc:
        raise LlmProviderError(f"model response failed reasoning-output validation: {exc}") from exc


@dataclass(frozen=True)
class LLMReasoningProvider:
    """S368 provider that delegates prompting to an injected generic client."""

    client: LlmClient
    provider_id: str = "llm"

    def reason(self, reasoning_input: ReasoningInput) -> ReasoningOutput:
        """Prompt the client, then parse and enforce the output contract."""
        if not getattr(self, "provider_id", "").strip():
            raise LlmProviderError("provider_id must be non-empty")
        prompt = build_reasoning_prompt(reasoning_input)
        raw = self.client.complete(prompt)
        if not isinstance(raw, str) or not raw.strip():
            raise LlmProviderError("model returned an empty response")
        return parse_reasoning_response(reasoning_input, raw)
