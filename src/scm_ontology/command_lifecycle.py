"""SCM OS command lifecycle (Phase R4) — S355 command lifecycle.

S355 is an immutable, governed state machine for a command. It tracks explicit
transitions from proposal to execution with actor and reason on every step and
fails closed on any unauthorized or out-of-order transition. It never performs
an external side effect.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from typing import Any


class CommandLifecycleError(ValueError):
    """Raised when a command lifecycle transition is invalid."""


class CommandState(str, Enum):
    PROPOSED = "proposed"
    AUTHORIZED = "authorized"
    APPROVED = "approved"
    DRY_RUN = "dry_run"
    EXECUTING = "executing"
    EXECUTED = "executed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


# Allowed transitions: (from, to)
_ALLOWED_TRANSITIONS: frozenset[tuple[CommandState, CommandState]] = frozenset(
    {
        (CommandState.PROPOSED, CommandState.AUTHORIZED),
        (CommandState.AUTHORIZED, CommandState.APPROVED),
        (CommandState.APPROVED, CommandState.DRY_RUN),
        (CommandState.DRY_RUN, CommandState.EXECUTING),
        (CommandState.EXECUTING, CommandState.EXECUTED),
        (CommandState.AUTHORIZED, CommandState.REJECTED),
        (CommandState.PROPOSED, CommandState.REJECTED),
        (CommandState.APPROVED, CommandState.CANCELLED),
        (CommandState.PROPOSED, CommandState.CANCELLED),
    }
)

# Terminal states that accept no further transitions.
_TERMINAL_STATES = frozenset({CommandState.EXECUTED, CommandState.REJECTED, CommandState.CANCELLED})


@dataclass(frozen=True)
class CommandTransition:
    """One explicit, recorded transition in a command's lifecycle."""

    from_state: CommandState
    to_state: CommandState
    occurred_at: str
    actor_id: str
    reason: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.occurred_at, str) or not self.occurred_at.strip():
            raise CommandLifecycleError("occurred_at must be non-empty")
        if not isinstance(self.actor_id, str) or not self.actor_id.strip():
            raise CommandLifecycleError("actor_id must be non-empty")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "from": self.from_state.value,
            "to": self.to_state.value,
            "occurred_at": self.occurred_at,
            "actor_id": self.actor_id,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class CommandLifecycle:
    """Immutable, append-only lifecycle state for a single command."""

    command_id: str
    state: CommandState
    transitions: tuple[CommandTransition, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.command_id, str) or not self.command_id.strip():
            raise CommandLifecycleError("command_id must be non-empty")
        object.__setattr__(self, "transitions", tuple(self.transitions))

    @property
    def is_terminal(self) -> bool:
        return self.state in _TERMINAL_STATES

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "S355.1",
            "command_id": self.command_id,
            "state": self.state.value,
            "is_terminal": self.is_terminal,
            "transitions": [transition.to_mapping() for transition in self.transitions],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def start_command_lifecycle(command_id: str) -> CommandLifecycle:
    """Start a command lifecycle in the proposed state."""
    if not isinstance(command_id, str) or not command_id.strip():
        raise CommandLifecycleError("command_id must be non-empty")
    return CommandLifecycle(command_id=command_id, state=CommandState.PROPOSED)


def transition_command(
    lifecycle: CommandLifecycle,
    *,
    to_state: CommandState,
    occurred_at: str,
    actor_id: str,
    reason: str = "",
) -> CommandLifecycle:
    """Move a command to a new state with an explicit, recorded transition.

    Fails closed on invalid target states, transitions from terminal states, or
    transitions not in the allowed set.
    """
    if not isinstance(lifecycle, CommandLifecycle):
        raise CommandLifecycleError("lifecycle must be a CommandLifecycle")
    if not isinstance(to_state, CommandState):
        raise CommandLifecycleError("to_state must be a CommandState")
    if not occurred_at.strip():
        raise CommandLifecycleError("occurred_at must be non-empty")
    if not actor_id.strip():
        raise CommandLifecycleError("actor_id must be non-empty")

    current = lifecycle.state
    if current in _TERMINAL_STATES:
        raise CommandLifecycleError(f"cannot transition a terminal command from {current.value}")
    if (current, to_state) not in _ALLOWED_TRANSITIONS:
        raise CommandLifecycleError(
            f"illegal transition from {current.value} to {to_state.value}"
        )

    transition = CommandTransition(
        from_state=current,
        to_state=to_state,
        occurred_at=occurred_at,
        actor_id=actor_id,
        reason=reason,
    )
    return CommandLifecycle(
        command_id=lifecycle.command_id,
        state=to_state,
        transitions=lifecycle.transitions + (transition,),
    )
