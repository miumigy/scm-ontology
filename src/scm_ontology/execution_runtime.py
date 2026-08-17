"""SCM Execution Runtime v0 (Phase R3) — deterministic in-memory dry run.

Phase R3 processes an immutable ``ExecutionCommand`` through a bounded,
injected ``ExecutionAdapter`` and produces an immutable ``DryRunExecutionResult``
describing what would be executed. It performs **no** external side effects and
introduces no canonical semantics: the result is a plan/observation, not an
approval to write to ERP, WMS, TMS, MES, or any other system.
"""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Protocol

from .decision_runtime import DecisionRuntimeResult, run_decision_loop
from .execution_command import ExecutionCommand
from .graph_reasoning_projection import GraphReasoningObservation
from .reasoning_provider import ReasoningProvider


class ExecutionRuntimeError(ValueError):
    """Raised when an execution command cannot be dry-run safely."""


class ExecutionAdapter(Protocol):
    """Bounded boundary from an execution command to a future execution target.

    Implementations MUST be deterministic and MUST NOT cause external side
    effects within ``dry_run``. Real ERP/WMS/TMS adapters may later produce a
    concrete plan here while still deferring the actual write to a runtime.
    """

    adapter_id: str

    def dry_run(self, command: ExecutionCommand) -> dict[str, Any]:
        """Return a deterministic plan mapping for the given command."""
        ...


@dataclass(frozen=True)
class DryRunPlan:
    """Immutable, auditable description of a planned execution action."""

    execution_target: str
    action: str
    payload: dict[str, Any]
    detail: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.execution_target, str) or not self.execution_target.strip():
            raise ExecutionRuntimeError("execution_target must be non-empty")
        if not isinstance(self.action, str) or not self.action.strip():
            raise ExecutionRuntimeError("action must be non-empty")
        object.__setattr__(self, "payload", {k: v for k, v in self.payload.items()})

    def to_mapping(self) -> dict[str, Any]:
        return {
            "execution_target": self.execution_target,
            "action": self.action,
            "payload": self.payload,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class InProcessDryRunAdapter:
    """Default deterministic adapter that derives a plan from the command."""

    adapter_id: str = "in-process-dry-run"
    execution_target: str = "in-memory-dry-run"

    def dry_run(self, command: ExecutionCommand) -> dict[str, Any]:
        proposal = command.decision.proposal.output.proposal
        action = (
            proposal.get("action")
            if isinstance(proposal, dict) and isinstance(proposal.get("action"), str)
            else "apply"
        )
        return {
            "execution_target": self.execution_target,
            "action": action,
            "payload": {
                "proposal": proposal,
                "actor_id": command.decision.actor_id,
                "authority": command.decision.authority,
                "authorized_at": command.decision.authorized_at,
            },
            "detail": f"deterministic dry run for {command.command_type}",
        }


@dataclass(frozen=True)
class DryRunExecutionResult:
    """Immutable result of a dry run; it is a plan, not an executed side effect."""

    command: ExecutionCommand
    plan: DryRunPlan
    result_id: str
    dry_ran_at: str
    status: str = "dry-run"

    def __post_init__(self) -> None:
        if not isinstance(self.result_id, str) or not self.result_id.strip():
            raise ExecutionRuntimeError("result_id must be non-empty")
        if not isinstance(self.dry_ran_at, str) or not self.dry_ran_at.strip():
            raise ExecutionRuntimeError("dry_ran_at must be non-empty")
        if not isinstance(self.status, str) or not self.status.strip():
            raise ExecutionRuntimeError("status must be non-empty")

    @property
    def command_id(self) -> str:
        return self.command.command_id

    @property
    def context_id(self) -> str:
        return self.command.context_id

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "S353.1",
            "result_id": self.result_id,
            "status": self.status,
            "dry_ran_at": self.dry_ran_at,
            "command": self.command.to_mapping(),
            "plan": self.plan.to_mapping(),
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _result_id(command: ExecutionCommand, plan: DryRunPlan) -> str:
    canonical = {
        "command": command.to_mapping(),
        "plan": plan.to_mapping(),
    }
    return sha256(
        json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def execute_dry_run(
    command: ExecutionCommand,
    *,
    dry_ran_at: str,
    adapter: ExecutionAdapter | None = None,
) -> DryRunExecutionResult:
    """Dry-run an immutable command through an adapter, without side effects.

    Fails closed if the command is not an ``ExecutionCommand``, the adapter is
    missing ``adapter_id``/``dry_run``, or the adapter plan is not a valid
    ``DryRunPlan`` mapping.
    """
    if not isinstance(command, ExecutionCommand):
        raise ExecutionRuntimeError("command must be an ExecutionCommand")
    if not dry_ran_at.strip():
        raise ExecutionRuntimeError("dry_ran_at must be non-empty")

    if adapter is None:
        adapter = InProcessDryRunAdapter()
    adapter_id = getattr(adapter, "adapter_id", None)
    if not isinstance(adapter_id, str) or not adapter_id.strip():
        raise ExecutionRuntimeError("adapter must expose a non-empty adapter_id")
    dry_run = getattr(adapter, "dry_run", None)
    if not callable(dry_run):
        raise ExecutionRuntimeError("adapter must expose a callable dry_run method")

    try:
        mapping = dry_run(command)
    except Exception as exc:
        raise ExecutionRuntimeError(f"execution adapter dry run failed: {exc}") from exc
    if not isinstance(mapping, dict):
        raise ExecutionRuntimeError("adapter dry_run must return a mapping")

    plan = DryRunPlan(
        execution_target=mapping.get("execution_target", ""),
        action=mapping.get("action", ""),
        payload=mapping.get("payload", {}),
        detail=mapping.get("detail", ""),
    )
    return DryRunExecutionResult(
        command=command,
        plan=plan,
        result_id=_result_id(command, plan),
        dry_ran_at=dry_ran_at,
    )


@dataclass(frozen=True)
class GovernedExecutionResult:
    """Immutable bundle of the governed decision loop and its dry-run plan."""

    decision: DecisionRuntimeResult
    dry_run: DryRunExecutionResult

    @property
    def context_id(self) -> str:
        return self.decision.context_id

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "S353.2",
            "context_id": self.context_id,
            "decision": self.decision.to_mapping(),
            "dry_run": self.dry_run.to_mapping(),
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def run_governed_loop_and_dry_run(
    *,
    context_id: str,
    observations: Iterable[GraphReasoningObservation],
    provider: ReasoningProvider,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_type: str,
    command_id: str,
    dry_ran_at: str,
    adapter: ExecutionAdapter | None = None,
) -> GovernedExecutionResult:
    """Run the S348 governed loop, then dry-run the resulting command (R3).

    This composes the canonical path end to end without any external side
    effect: observations -> ... -> ExecutionCommand -> DryRunExecutionResult.
    """
    decision = run_decision_loop(
        context_id=context_id,
        observations=observations,
        provider=provider,
        actor_id=actor_id,
        authority=authority,
        authorized_at=authorized_at,
        command_type=command_type,
        command_id=command_id,
    )
    dry_run = execute_dry_run(decision.execution_command, dry_ran_at=dry_ran_at, adapter=adapter)
    return GovernedExecutionResult(decision=decision, dry_run=dry_run)
