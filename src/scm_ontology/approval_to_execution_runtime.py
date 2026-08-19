"""P9-C — Approval-to-Execution Runtime (controlled real execution).

Advances a governed command from its approved dry-run state to a controlled
external execution and captures the immutable P9-A outcome contract.

P9-C composes the S355 command lifecycle (which already reaches the ``dry_run``
state), the S354 governed audit, the P9-B external execution adapter boundary,
and the P9-A outcome contract. It enforces a fail-closed gate: a command may
only be executed once it has been authorized, approved, and dry-run, and only
through an injected external adapter. It performs no canonical mutation and
records every state transition with actor and reason.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from .command_lifecycle import (
    CommandLifecycle,
    CommandState,
    start_command_lifecycle,
    transition_command,
)
from .execution_command import ExecutionCommand
from .execution_outcome_contract import ExecutionOutcomeContract
from .execution_runtime import DryRunExecutionResult, execute_dry_run
from .external_execution_adapter import ExternalExecutionAdapter, execute_externally


class ApprovalToExecutionError(ValueError):
    """Raised when a command cannot progress from approval to execution."""


@dataclass(frozen=True)
class ApprovalToExecutionResult:
    """Immutable bundle of a command's progress from dry-run to executed outcome.

    The lifecycle is recorded at the ``executed`` (or ``executing``) terminal
    state with the full auditable transition history, and the outcome is the
    immutable P9-A contract returned by the external adapter.
    """

    lifecycle: CommandLifecycle
    outcome: ExecutionOutcomeContract
    dry_run: DryRunExecutionResult
    executed_at: str

    def __post_init__(self) -> None:
        if not isinstance(self.lifecycle, CommandLifecycle):
            raise ApprovalToExecutionError("lifecycle must be a CommandLifecycle")
        if not isinstance(self.outcome, ExecutionOutcomeContract):
            raise ApprovalToExecutionError("outcome must be an ExecutionOutcomeContract")
        if not isinstance(self.dry_run, DryRunExecutionResult):
            raise ApprovalToExecutionError("dry_run must be a DryRunExecutionResult")
        if not self.executed_at.strip():
            raise ApprovalToExecutionError("executed_at must be non-empty")

    @property
    def command_id(self) -> str:
        return self.outcome.command_id

    @property
    def context_id(self) -> str:
        return self.outcome.context_id

    @property
    def verdict(self) -> str:
        return self.outcome.verdict

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P9C.1",
            "command_id": self.command_id,
            "context_id": self.context_id,
            "lifecycle_state": self.lifecycle.state.value,
            "executed_at": self.executed_at,
            "lifecycle": self.lifecycle.to_mapping(),
            "dry_run": self.dry_run.to_mapping(),
            "outcome": self.outcome.to_mapping(),
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def build_approved_lifecycle(
    command_id: str,
    *,
    recorded_at: str,
    actor_id: str,
    reason: str = "",
) -> CommandLifecycle:
    """Build a command lifecycle advanced to the approved state.

    The lifecycle starts at ``proposed`` and is advanced through ``authorized``
    and ``approved`` with an explicit actor on every transition (matching the
    S355 allowed-transition set and the S366 workflow pattern).
    """
    lifecycle = start_command_lifecycle(command_id)
    for state in (CommandState.AUTHORIZED, CommandState.APPROVED):
        lifecycle = transition_command(
            lifecycle,
            to_state=state,
            occurred_at=recorded_at,
            actor_id=actor_id,
            reason=reason,
        )
    return lifecycle


def approve_and_execute(
    command: ExecutionCommand,
    *,
    adapter: ExternalExecutionAdapter,
    executed_at: str,
    actor_id: str,
    external_system: object | None = None,
    lifecycle: CommandLifecycle | None = None,
    dry_run: DryRunExecutionResult | None = None,
) -> ApprovalToExecutionResult:
    """Progress an approved command from dry-run to controlled execution.

    Fails closed unless:

    - ``command`` and ``actor_id`` / ``executed_at`` are valid;
    - the lifecycle is at the ``dry_run`` state (a freshly supplied lifecycle is
      first advanced to ``approved`` then dry-run);
    - the external adapter passes P9-B validation and supports the command;
    - every lifecycle transition (dry_run -> executing -> executed) is allowed.

    The resulting lifecycle is recorded at the ``executed`` state and the
    outcome is the immutable P9-A contract — no canonical mutation occurs.
    """
    if not isinstance(command, ExecutionCommand):
        raise ApprovalToExecutionError("command must be an ExecutionCommand")
    if not executed_at.strip():
        raise ApprovalToExecutionError("executed_at must be non-empty")
    if not actor_id.strip():
        raise ApprovalToExecutionError("actor_id must be non-empty")

    if lifecycle is None:
        lifecycle = build_approved_lifecycle(
            command.command_id, recorded_at=executed_at, actor_id=actor_id
        )
    if dry_run is None:
        if lifecycle.state not in (CommandState.APPROVED, CommandState.DRY_RUN):
            raise ApprovalToExecutionError(
                f"cannot dry-run a command in state {lifecycle.state.value}; "
                "expected approved or dry_run"
            )
        dry_run = execute_dry_run(command, dry_ran_at=executed_at, adapter=None)
        if lifecycle.state == CommandState.APPROVED:
            lifecycle = transition_command(
                lifecycle,
                to_state=CommandState.DRY_RUN,
                occurred_at=executed_at,
                actor_id=actor_id,
                reason="dry run before controlled execution",
            )

    if lifecycle.state != CommandState.DRY_RUN:
        raise ApprovalToExecutionError(
            f"cannot execute a command in state {lifecycle.state.value}; expected dry_run"
        )

    # Controlled execution: advance dry_run -> executing -> executed.
    executing = transition_command(
        lifecycle,
        to_state=CommandState.EXECUTING,
        occurred_at=executed_at,
        actor_id=actor_id,
        reason="controlled external execution started",
    )
    outcome = execute_externally(
        command,
        adapter=adapter,
        executed_at=executed_at,
        external_system=external_system,
    )
    executed = transition_command(
        executing,
        to_state=CommandState.EXECUTED,
        occurred_at=executed_at,
        actor_id=actor_id,
        reason=f"external execution completed with verdict {outcome.verdict}",
    )

    return ApprovalToExecutionResult(
        lifecycle=executed,
        outcome=outcome,
        dry_run=dry_run,
        executed_at=executed_at,
    )
