from __future__ import annotations

from typing import Protocol

from .reasoning_input import ReasoningInput
from .reasoning_output import ReasoningOutput


class ReasoningProviderError(ValueError):
    """Raised when a reasoning provider violates the S368 boundary."""


class ReasoningProvider(Protocol):
    """Minimal interface for rules, optimization, LLM, or other providers."""
    provider_id: str
    def reason(self, reasoning_input: ReasoningInput) -> ReasoningOutput: ...


def invoke_reasoning_provider(provider: ReasoningProvider, reasoning_input: ReasoningInput) -> ReasoningOutput:
    """Invoke a provider and enforce the engine-neutral output contract."""
    if not isinstance(reasoning_input, ReasoningInput):
        raise ReasoningProviderError("reasoning_input must be a ReasoningInput")
    provider_id = getattr(provider, "provider_id", None)
    if not isinstance(provider_id, str) or not provider_id.strip():
        raise ReasoningProviderError("provider_id must be non-empty")
    reason = getattr(provider, "reason", None)
    if not callable(reason):
        raise ReasoningProviderError("provider must expose a callable reason method")
    try:
        output = reason(reasoning_input)
    except Exception as exc:
        raise ReasoningProviderError(f"reasoning provider failed: {exc}") from exc
    if not isinstance(output, ReasoningOutput):
        raise ReasoningProviderError("provider must return ReasoningOutput")
    if output.context_id != reasoning_input.context_id:
        raise ReasoningProviderError("provider output context_id must match reasoning input")
    return output
