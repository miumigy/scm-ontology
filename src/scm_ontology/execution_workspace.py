"""SCM OS Execution Workflow Workspace (Phase 6, P6-D).

A control-plane workspace to **inspect command lifecycle, dry-run results,
approval gates, and audit trail** for governed executions, without re-running
or executing any command.

P6-D composes the existing governed execution contracts:
  - command lifecycle (S355) -> lifecycle state and recorded transitions;
  - dry-run results (S353) -> dry-run status / result id;
  - governed audit (S354) -> audit id;
  - authorization / approval (S356) -> approval-gate status.

It projects each command into an immutable, deterministic, JSON-safe
``ExecutionStep`` and folds them into a content-addressed ``ExecutionWorkspace``
with an execution summary. ``launch_execution_workflow`` is the deterministic
reference path that composes the existing constructors end to end at the
execution level (it does not re-derive any decision).

P6-D never executes a command, mutates Canonical Truth, or performs an external
side effect.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Iterable, Sequence

from .authorization_governance import AuthorizationDecision
from .command_lifecycle import (
    CommandLifecycle,
    CommandState,
    start_command_lifecycle,
    transition_command,
)
from .execution_runtime import (
    DryRunExecutionResult,
    GovernedExecutionResult,
)
from .governed_audit import (
    GovernedDecisionAuditEntry,
    record_governed_decision,
)


class ExecutionWorkspaceError(ValueError):
    """Raised when a workspace input or invocation is invalid."""


@dataclass(frozen=True)
class CommandExecution:
    """One governed execution composed from its existing artifacts."""

    command_id: str
    command_type: str
    lifecycle: CommandLifecycle
    dry_run: DryRunExecutionResult | None = None
    audit: GovernedDecisionAuditEntry | None = None
    authorization: AuthorizationDecision | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.command_id, str) or not self.command_id.strip():
            raise ExecutionWorkspaceError("command_id must be non-empty")
        if not isinstance(self.command_type, str) or not self.command_type.strip():
            raise ExecutionWorkspaceError("command_type must be non-empty")
        if not isinstance(self.lifecycle, CommandLifecycle):
            raise ExecutionWorkspaceError("lifecycle must be a CommandLifecycle")
        if self.lifecycle.command_id != self.command_id:
            raise ExecutionWorkspaceError(
                "lifecycle.command_id must match command_id"
            )
        if self.dry_run is not None and not isinstance(
            self.dry_run, DryRunExecutionResult
        ):
            raise ExecutionWorkspaceError("dry_run must be a DryRunExecutionResult")
        if self.audit is not None and not isinstance(
            self.audit, GovernedDecisionAuditEntry
        ):
            raise ExecutionWorkspaceError("audit must be a GovernedDecisionAuditEntry")
        if self.authorization is not None and not isinstance(
            self.authorization, AuthorizationDecision
        ):
            raise ExecutionWorkspaceError(
                "authorization must be an AuthorizationDecision"
            )


def _approval_status(
    lifecycle: CommandLifecycle, authorization: AuthorizationDecision | None
) -> str:
    """Derive a deterministic approval-gate status from the composed artifacts."""
    if authorization is not None and not authorization.allowed:
        return "denied"
    state = lifecycle.state
    if state in (CommandState.APPROVED, CommandState.DRY_RUN,
                 CommandState.EXECUTING, CommandState.EXECUTED):
        return "approved"
    if state in (CommandState.REJECTED, CommandState.CANCELLED):
        return "denied"
    return "pending"


@dataclass(frozen=True)
class ExecutionStep:
    """Immutable inspectable record for one governed command execution."""

    command_id: str
    command_type: str
    state: str
    is_terminal: bool
    approval: str
    dry_run_status: str | None
    dry_run_result_id: str | None
    audit_id: str | None
    transitions: tuple[dict[str, Any], ...]

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "contract_version": "P6D.1",
            "kind": "execution",
            "command_id": self.command_id,
            "command_type": self.command_type,
            "state": self.state,
            "is_terminal": self.is_terminal,
            "approval": self.approval,
            "transitions": [dict(t) for t in self.transitions],
        }
        for name in ("dry_run_status", "dry_run_result_id", "audit_id"):
            val = getattr(self, name)
            if val is not None:
                value[name] = val
        return value


@dataclass(frozen=True)
class ExecutionWorkspaceSummary:
    """Deterministic aggregate counts across an execution workspace."""

    command_count: int
    approved_count: int
    pending_count: int
    denied_count: int
    terminal_count: int
    dry_run_count: int
    audit_count: int

    def to_mapping(self) -> dict[str, Any]:
        return {
            "command_count": self.command_count,
            "approved_count": self.approved_count,
            "pending_count": self.pending_count,
            "denied_count": self.denied_count,
            "terminal_count": self.terminal_count,
            "dry_run_count": self.dry_run_count,
            "audit_count": self.audit_count,
        }


@dataclass(frozen=True)
class ExecutionWorkspace:
    """Immutable, content-addressed execution workspace snapshot."""

    workspace_id: str
    created_at: str
    view_actor_id: str
    steps: tuple[ExecutionStep, ...]
    summary: ExecutionWorkspaceSummary

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P6D.1",
            "is_execution_workspace": True,
            "workspace_id": self.workspace_id,
            "created_at": self.created_at,
            "view_actor_id": self.view_actor_id,
            "summary": self.summary.to_mapping(),
            "steps": [step.to_mapping() for step in self.steps],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _project(command: CommandExecution) -> ExecutionStep:
    lifecycle = command.lifecycle
    transitions = tuple(t.to_mapping() for t in lifecycle.transitions)
    dry_run = command.dry_run
    audit = command.audit
    return ExecutionStep(
        command_id=command.command_id,
        command_type=command.command_type,
        state=lifecycle.state.value,
        is_terminal=lifecycle.is_terminal,
        approval=_approval_status(lifecycle, command.authorization),
        dry_run_status=None if dry_run is None else dry_run.status,
        dry_run_result_id=None if dry_run is None else dry_run.result_id,
        audit_id=None if audit is None else audit.audit_id,
        transitions=transitions,
    )


def workspace_execution(
    lifecycle: CommandLifecycle,
    *,
    command_type: str,
    dry_run: DryRunExecutionResult | None = None,
    audit: GovernedDecisionAuditEntry | None = None,
    authorization: AuthorizationDecision | None = None,
) -> ExecutionStep:
    """Project an already-produced command execution into an inspectable step."""
    command = CommandExecution(
        command_id=lifecycle.command_id,
        command_type=command_type,
        lifecycle=lifecycle,
        dry_run=dry_run,
        audit=audit,
        authorization=authorization,
    )
    return _project(command)


def build_execution_workspace(
    commands: Iterable[CommandExecution],
    *,
    created_at: str,
    view_actor_id: str,
) -> ExecutionWorkspace:
    """Fold composed command executions into an immutable workspace snapshot."""
    if not isinstance(created_at, str) or not created_at.strip():
        raise ExecutionWorkspaceError("created_at must be non-empty")
    if not isinstance(view_actor_id, str) or not view_actor_id.strip():
        raise ExecutionWorkspaceError("view_actor_id must be non-empty")

    try:
        commands_tuple = tuple(commands)
    except TypeError as exc:
        raise ExecutionWorkspaceError("commands must be iterable") from exc
    if not commands_tuple:
        raise ExecutionWorkspaceError("commands must not be empty")
    for command in commands_tuple:
        if not isinstance(command, CommandExecution):
            raise ExecutionWorkspaceError("every command must be a CommandExecution")

    command_ids = [command.command_id for command in commands_tuple]
    if len(command_ids) != len(set(command_ids)):
        raise ExecutionWorkspaceError("command ids must be unique within the workspace")

    steps = tuple(_project(command) for command in commands_tuple)

    approved = sum(1 for s in steps if s.approval == "approved")
    pending = sum(1 for s in steps if s.approval == "pending")
    denied = sum(1 for s in steps if s.approval == "denied")
    terminal = sum(1 for s in steps if s.is_terminal)
    dry_run = sum(1 for s in steps if s.dry_run_result_id is not None)
    audit = sum(1 for s in steps if s.audit_id is not None)
    summary = ExecutionWorkspaceSummary(
        command_count=len(steps),
        approved_count=approved,
        pending_count=pending,
        denied_count=denied,
        terminal_count=terminal,
        dry_run_count=dry_run,
        audit_count=audit,
    )

    payload = {
        "created_at": created_at,
        "view_actor_id": view_actor_id,
        "steps": [step.to_mapping() for step in steps],
    }
    workspace_id = sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return ExecutionWorkspace(
        workspace_id=workspace_id,
        created_at=created_at,
        view_actor_id=view_actor_id,
        steps=steps,
        summary=summary,
    )


def launch_execution_workflow(
    *,
    governed_runs: Sequence[GovernedExecutionResult],
    actor_id: str,
    recorded_at: str,
    view_actor_id: str | None = None,
    created_at: str | None = None,
) -> ExecutionWorkspace:
    """Deterministic reference path composing the existing execution contracts.

    For each governed run (S353) it starts and advances a command lifecycle
    through the dry-run state (S355), and folds the run's dry-run result (S353)
    and governed audit entry (S354) into the workspace. It never re-derives any
    decision.
    """
    if not isinstance(actor_id, str) or not actor_id.strip():
        raise ExecutionWorkspaceError("actor_id must be non-empty")
    if not isinstance(recorded_at, str) or not recorded_at.strip():
        raise ExecutionWorkspaceError("recorded_at must be non-empty")
    if not governed_runs:
        raise ExecutionWorkspaceError("governed_runs must not be empty")

    created = created_at or recorded_at
    viewer = view_actor_id or actor_id

    executions: list[CommandExecution] = []
    for run in governed_runs:
        if not isinstance(run, GovernedExecutionResult):
            raise ExecutionWorkspaceError("every governed run must be a GovernedExecutionResult")
        dry_run = run.dry_run
        command = dry_run.command
        command_id = command.command_id
        command_type = command.command_type

        lifecycle = start_command_lifecycle(command_id)
        for to_state, reason in (
            (CommandState.AUTHORIZED, "authorize in workflow"),
            (CommandState.APPROVED, "approve in workflow"),
            (CommandState.DRY_RUN, "dry run in workflow"),
        ):
            lifecycle = transition_command(
                lifecycle,
                to_state=to_state,
                occurred_at=recorded_at,
                actor_id=actor_id,
                reason=reason,
            )

        audit = record_governed_decision(
            run.decision,
            recorded_at=recorded_at,
            dry_run=dry_run,
        )
        executions.append(
            CommandExecution(
                command_id=command_id,
                command_type=command_type,
                lifecycle=lifecycle,
                dry_run=dry_run,
                audit=audit,
            )
        )

    return build_execution_workspace(
        executions,
        created_at=created,
        view_actor_id=viewer,
    )
