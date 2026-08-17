"""Rule-based S368 reasoning provider (Phase R2).

A deterministic, side-effect-free implementation of the reasoning-provider
boundary. A rule matches against the immutable observations of a
``ReasoningInput`` and, when it fires, produces a ``ReasoningOutput`` that
preserves the input context, evidence, and provenance. If no rule matches, the
provider fails closed rather than inventing a proposal.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from .reasoning_input import ReasoningInput
from .reasoning_output import ReasoningOutput


class RuleReasoningProviderError(ValueError):
    """Raised when a rule-based provider cannot construct or fire a rule."""


@dataclass(frozen=True)
class ReasoningRule:
    """A deterministic rule from observations to a proposed decision result.

    ``matches`` is a pure predicate over the observation tuple. Its result must
    depend only on the observations so that rule evaluation is reproducible and
    auditable through ``rule_id`` and ``condition_description``.
    """

    rule_id: str
    proposal: Any
    rationale: str
    matches: Callable[[tuple[Any, ...]], bool]
    condition_description: str = ""
    confidence: float | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.rule_id, str) or not self.rule_id.strip():
            raise RuleReasoningProviderError("rule_id must be non-empty")
        if not isinstance(self.rationale, str) or not self.rationale.strip():
            raise RuleReasoningProviderError("rationale must be non-empty")
        if self.proposal is None or (isinstance(self.proposal, str) and not self.proposal.strip()):
            raise RuleReasoningProviderError("proposal must be non-empty")
        if not callable(self.matches):
            raise RuleReasoningProviderError("matches must be callable")
        if not isinstance(self.condition_description, str):
            raise RuleReasoningProviderError("condition_description must be a string")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise RuleReasoningProviderError("confidence must be between 0 and 1")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "proposal": self.proposal,
            "rationale": self.rationale,
            "condition_description": self.condition_description,
            "confidence": self.confidence,
        }


def when_measurement_below(
    question_id: str,
    key: str,
    threshold: float,
) -> tuple[str, Callable[[tuple[Any, ...]], bool]]:
    """A reusable condition: an observation measurement falls below a threshold.

    Returns ``(description, matches)`` so callers can attach an auditable rule
    description without writing boilerplate predicates.
    """
    def matches(observations: tuple[Any, ...]) -> bool:
        for observation in observations:
            if observation.question_id != question_id:
                continue
            value = observation.value
            if not isinstance(value, Mapping):
                continue
            measurement = value.get(key)
            if isinstance(measurement, (int, float)) and measurement < threshold:
                return True
        return False

    description = f"{question_id}.{key} < {threshold}"
    return description, matches


@dataclass(frozen=True)
class RuleReasoningProvider:
    """Deterministic S368 provider that fires the first matching rule.

    Rules are evaluated in declaration order; the first rule whose condition
    matches produces the output. When no rule matches, ``reason`` fails closed
    by raising, so the governed loop never silently proposes an action.
    """

    provider_id: str
    rules: tuple[ReasoningRule, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.provider_id, str) or not self.provider_id.strip():
            raise RuleReasoningProviderError("provider_id must be non-empty")
        if not self.rules:
            raise RuleReasoningProviderError("rules must not be empty")
        if any(not isinstance(rule, ReasoningRule) for rule in self.rules):
            raise RuleReasoningProviderError("rules must contain only ReasoningRule values")
        rule_ids = [rule.rule_id for rule in self.rules]
        if len(rule_ids) != len(set(rule_ids)):
            raise RuleReasoningProviderError("rule_id must be unique within a provider")

    def reason(self, reasoning_input: ReasoningInput) -> ReasoningOutput:
        """Return the first matching rule's proposal, or fail closed."""
        for rule in self.rules:
            if rule.matches(reasoning_input.observations):
                return ReasoningOutput(
                    context_id=reasoning_input.context_id,
                    proposal=rule.proposal,
                    rationale=f"{rule.rationale} [{rule.rule_id}]",
                    evidence_ids=reasoning_input.evidence_ids,
                    provenance_ids=reasoning_input.provenance_ids,
                    confidence=rule.confidence,
                )
        raise RuleReasoningProviderError(
            "no matching rule; refusing to propose an action for this context"
        )
