"""Procured governance (Phase R4) — S354 command lifecycle, approval, override.

S354 adds governed post-reasoning governance to the SCM OS loop. It records
the auditable trail of one governed decision, replays the deterministic
governance chain to prove reproducibility, and applies authorization policy,
human approval, and senior override gates before a command may proceed to the
R3 execution runtime.

It reuses the S345 authorization, S346 command, S348 decision runtime, and
S353 execution runtime contracts. It introduces no new canonical semantics and
never performs an external side effect.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import json
from typing import Any

from .decision_authorization import AuthorizedDecision, authorize_decision
from .decision_runtime import DecisionRuntimeResult
from .execution_command import ExecutionCommand, build_execution_command
from .execution_runtime import DryRunExecutionResult
from .proposal_validation import ValidatedDecisionProposal, validate_decision_proposal


class DecisionGovernanceError(ValueError):
    """Raised when a governed decision cannot be recorded or replayed."""


@dataclass(frozen=True)
class GovernedDecisionAuditEntry:
    """Immutable, content-addressed record of one governed decision run.

    ``audit_id`` is the deterministic hash of the serialized runtime result
    (context, evidence, provenance, proposal, authorization, and command), so
    any tampering is detectable on replay.
    """

    audit_id: str
    recorded_at: str
    result: DecisionRuntimeResult
    dry_run: DryRunExecutionResult | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.audit_id, str) or not self.audit_id.strip():
            raise DecisionGovernanceError("audit_id must be non-empty")
        if not isinstance(self.recorded_at, str) or not self.recorded_at.strip():
            raise DecisionGovernanceError("recorded_at must be non-empty")

    @property
    def context_id(self) -> str:
        return self.result.context_id

    @property
    def command_id(self) -> str:
        return self.result.execution_command.command_id

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "S354.1",
            "audit_id": self.audit_id,
            "recorded_at": self.recorded_at,
            "context_id": self.context_id,
            "command_id": self.command_id,
            "decision": self.result.to_mapping(),
            "dry_run": self.dry_run.to_mapping() if self.dry_run is not None else None,
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _content_digest(result: DecisionRuntimeResult, dry_run: DryRunExecutionResult | None) -> str:
    from hashlib import sha256

    canonical = {
        "decision": result.to_mapping(),
        "dry_run": dry_run.to_mapping() if dry_run is not None else None,
    }
    return sha256(
        json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def record_governed_decision(
    result: DecisionRuntimeResult,
    *,
    recorded_at: str,
    dry_run: DryRunExecutionResult | None = None,
) -> GovernedDecisionAuditEntry:
    """Record one governed decision run as a content-addressed audit entry."""
    if not isinstance(result, DecisionRuntimeResult):
        raise DecisionGovernanceError("result must be a DecisionRuntimeResult")
    if not recorded_at.strip():
        raise DecisionGovernanceError("recorded_at must be non-empty")
    return GovernedDecisionAuditEntry(
        audit_id=_content_digest(result, dry_run),
        recorded_at=recorded_at,
        result=result,
        dry_run=dry_run,
    )


@dataclass(frozen=True)
class GovernedAuditTrail:
    """Immutable, ordered collection of governed decision audit entries."""

    entries: tuple[GovernedDecisionAuditEntry, ...]

    def __post_init__(self) -> None:
        if not self.entries:
            raise DecisionGovernanceError("audit trail must not be empty")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "S354.2",
            "entry_count": len(self.entries),
            "entries": [entry.to_mapping() for entry in self.entries],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def build_audit_trail(
    entries: Sequence[GovernedDecisionAuditEntry],
) -> GovernedAuditTrail:
    """Build an immutable audit trail, preserving the given order."""
    return GovernedAuditTrail(tuple(entries))


def replay_governed_decision(
    entry: GovernedDecisionAuditEntry,
    *,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_type: str,
    command_id: str,
) -> AuthorizedDecision:
    """Replay the deterministic governed chain and verify it reproduces the record.

    Re-running the reasoning provider is intentionally out of scope: providers
    (especially LLM) are not deterministic. Replay instead re-runs the
    deterministic governance steps — proposal validation, authorization, and
    command construction — and fails closed if the reproduced artifacts drift
    from the recorded decision.
    """
    if not isinstance(entry, GovernedDecisionAuditEntry):
        raise DecisionGovernanceError("entry must be a GovernedDecisionAuditEntry")

    result = entry.result
    try:
        reproduced_proposal: ValidatedDecisionProposal = validate_decision_proposal(
            result.reasoning_input,
            result.reasoning_output,
        )
        reproduced_decision: AuthorizedDecision = authorize_decision(
            reproduced_proposal,
            actor_id=actor_id,
            authority=authority,
            authorized_at=authorized_at,
        )
        reproduced_command: ExecutionCommand = build_execution_command(
            reproduced_decision,
            command_type=command_type,
            command_id=command_id,
        )
    except Exception as exc:
        raise DecisionGovernanceError(f"decision replay failed: {exc}") from exc

    # Verify the reproduced artifacts match the recorded ones.
    if reproduced_proposal.to_mapping() != result.validated_proposal.to_mapping():
        raise DecisionGovernanceError("replay drifted from the recorded proposal")
    if reproduced_decision.to_mapping() != result.authorized_decision.to_mapping():
        raise DecisionGovernanceError("replay drifted from the recorded authorization")
    if reproduced_command.to_mapping() != result.execution_command.to_mapping():
        raise DecisionGovernanceError("replay drifted from the recorded command")

    # Confirm the recorded decision is still content-integrity-valid.
    expected_id = _content_digest(result, entry.dry_run)
    if expected_id != entry.audit_id:
        raise DecisionGovernanceError("audit entry content digest mismatch")

    return reproduced_decision
