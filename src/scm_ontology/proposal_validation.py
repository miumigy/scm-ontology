"""Governance boundary for validating reasoning proposals before authorization."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .reasoning_input import ReasoningInput
from .reasoning_output import ReasoningOutput


class ProposalValidationError(ValueError):
    """Raised when a reasoning proposal is not eligible for governance."""


@dataclass(frozen=True)
class ValidatedDecisionProposal:
    """An immutable, validated proposal; it is not an authorization or execution."""

    output: ReasoningOutput

    def to_mapping(self) -> dict[str, object]:
        return {
            "contract_version": "S344.1",
            "output": self.output.to_mapping(),
        }


def validate_decision_proposal(
    reasoning_input: ReasoningInput,
    output: ReasoningOutput,
) -> ValidatedDecisionProposal:
    """Validate a reasoning output against the input context without mutating it."""
    if output.context_id != reasoning_input.context_id:
        raise ProposalValidationError("context_id must match reasoning input")
    if output.proposal is None or (isinstance(output.proposal, str) and not output.proposal.strip()):
        raise ProposalValidationError("proposal must be non-empty")
    if not output.evidence_ids:
        raise ProposalValidationError("proposal must include evidence_ids")
    if not output.provenance_ids:
        raise ProposalValidationError("proposal must include provenance_ids")
    if not set(output.evidence_ids).issubset(set(reasoning_input.evidence_ids)):
        raise ProposalValidationError("proposal evidence_ids must come from reasoning input")
    if not set(output.provenance_ids).issubset(set(reasoning_input.provenance_ids)):
        raise ProposalValidationError("proposal provenance_ids must come from reasoning input")
    return ValidatedDecisionProposal(output=output)
