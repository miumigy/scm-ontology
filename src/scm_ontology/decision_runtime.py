"""SCM Decision Runtime v0 — deterministic in-memory governed decision loop.

Phase R1 orchestrates the existing S333..S346 contract boundaries into a
single side-effect-free Python API. It reuses the governed contracts and
introduces no new canonical semantics: reasoning remains a proposal,
authorization is explicit, and the ExecutionCommand is immutable and never
executes a side effect.

This module is intentionally free of LLM, database, ERP, WMS, and TMS
dependencies. Providers are injected through the S368 ``ReasoningProvider``
boundary so rules, optimization, or LLM engines can be swapped later without
changing the governed loop.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import json
from typing import Any

from .decision_authorization import AuthorizedDecision, authorize_decision
from .execution_command import ExecutionCommand, build_execution_command
from .graph_reasoning_projection import GraphReasoningObservation
from .proposal_validation import ValidatedDecisionProposal, validate_decision_proposal
from .reasoning_assembly import assemble_reasoning_input, ReasoningAssemblyError
from .reasoning_input import ReasoningInput
from .reasoning_output import ReasoningOutput
from .reasoning_provider import ReasoningProvider, invoke_reasoning_provider


class DecisionRuntimeError(ValueError):
    """Raised when the governed decision loop cannot safely proceed."""


@dataclass(frozen=True)
class MockReasoningProvider:
    """Deterministic S368 provider that echoes a fixed proposal.

    This is an implementation of the existing reasoning-provider boundary, not
    a new semantic contract. It never inspects external state and performs no
    side effects, so the governed loop is reproducible for tests and demos.
    """

    provider_id: str
    proposal: Any
    rationale: str
    confidence: float | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.provider_id, str) or not self.provider_id.strip():
            raise DecisionRuntimeError("provider_id must be non-empty")
        if not isinstance(self.rationale, str) or not self.rationale.strip():
            raise DecisionRuntimeError("rationale must be non-empty")
        if self.proposal is None or (isinstance(self.proposal, str) and not self.proposal.strip()):
            raise DecisionRuntimeError("proposal must be non-empty")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise DecisionRuntimeError("confidence must be between 0 and 1")

    def reason(self, reasoning_input: ReasoningInput) -> ReasoningOutput:
        """Return a deterministic proposal bound to the input's identifiers."""
        return ReasoningOutput(
            context_id=reasoning_input.context_id,
            proposal=self.proposal,
            rationale=self.rationale,
            evidence_ids=reasoning_input.evidence_ids,
            provenance_ids=reasoning_input.provenance_ids,
            confidence=self.confidence,
        )


@dataclass(frozen=True)
class DecisionRuntimeResult:
    """Immutable, auditable outcome of one governed decision loop run.

    The result bundles every boundary artifact produced by the loop so callers
    and audit trails can inspect reasoning, validation, authorization, and the
    resulting immutable command without re-running the pipeline.
    """

    reasoning_input: ReasoningInput
    reasoning_output: ReasoningOutput
    validated_proposal: ValidatedDecisionProposal
    authorized_decision: AuthorizedDecision
    execution_command: ExecutionCommand

    @property
    def context_id(self) -> str:
        return self.reasoning_input.context_id

    def to_mapping(self) -> dict[str, Any]:
        """Return a deterministic, JSON-safe audit mapping of the whole run."""
        return {
            "contract_version": "S348.1",
            "context_id": self.context_id,
            "reasoning_input": self.reasoning_input.to_mapping(),
            "reasoning_output": self.reasoning_output.to_mapping(),
            "validated_proposal": self.validated_proposal.to_mapping(),
            "authorized_decision": self.authorized_decision.to_mapping(),
            "execution_command": self.execution_command.to_mapping(),
        }

    def to_json(self) -> str:
        """Serialize the complete run deterministically as UTF-8 JSON."""
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def run_decision_loop(
    *,
    context_id: str,
    observations: Iterable[GraphReasoningObservation],
    provider: ReasoningProvider,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_type: str,
    command_id: str,
) -> DecisionRuntimeResult:
    """Run the S333..S346 governed decision loop against a ReasoningInput.

    Executes the canonical path

        observations -> ReasoningInput -> ReasoningOutput -> Validation
            -> Authorization -> ExecutionCommand

    and returns an immutable, auditable result. The loop performs no external
    side effects and fails closed if any boundary is violated (empty context,
    missing evidence/provenance, provider/context mismatch, or unsafe command).
    """
    if not isinstance(context_id, str) or not context_id.strip():
        raise DecisionRuntimeError("context_id must be non-empty")

    try:
        reasoning_input: ReasoningInput = assemble_reasoning_input(
            context_id,
            observations,
        )
    except ReasoningAssemblyError as exc:
        raise DecisionRuntimeError(f"decision loop stopped at context assembly: {exc}") from exc

    try:
        reasoning_output: ReasoningOutput = invoke_reasoning_provider(
            provider,
            reasoning_input,
        )
    except Exception as exc:
        raise DecisionRuntimeError(f"decision loop stopped at reasoning: {exc}") from exc

    try:
        validated_proposal: ValidatedDecisionProposal = validate_decision_proposal(
            reasoning_input,
            reasoning_output,
        )
    except Exception as exc:
        raise DecisionRuntimeError(f"decision loop stopped at proposal validation: {exc}") from exc

    try:
        authorized_decision: AuthorizedDecision = authorize_decision(
            validated_proposal,
            actor_id=actor_id,
            authority=authority,
            authorized_at=authorized_at,
        )
    except Exception as exc:
        raise DecisionRuntimeError(f"decision loop stopped at authorization: {exc}") from exc

    try:
        execution_command: ExecutionCommand = build_execution_command(
            authorized_decision,
            command_type=command_type,
            command_id=command_id,
        )
    except Exception as exc:
        raise DecisionRuntimeError(f"decision loop stopped at command construction: {exc}") from exc

    return DecisionRuntimeResult(
        reasoning_input=reasoning_input,
        reasoning_output=reasoning_output,
        validated_proposal=validated_proposal,
        authorized_decision=authorized_decision,
        execution_command=execution_command,
    )
