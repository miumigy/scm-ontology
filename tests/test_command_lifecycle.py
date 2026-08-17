from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.command_lifecycle import (
    CommandLifecycle,
    CommandLifecycleError,
    CommandState,
    start_command_lifecycle,
    transition_command,
)


def test_starts_in_proposed_state():
    lifecycle = start_command_lifecycle("cmd-1")
    assert lifecycle.command_id == "cmd-1"
    assert lifecycle.state == CommandState.PROPOSED
    assert lifecycle.is_terminal is False


def test_happy_path_command_lifecycle():
    lifecycle = start_command_lifecycle("cmd-1")
    lifecycle = transition_command(
        lifecycle, to_state=CommandState.AUTHORIZED, occurred_at="t1", actor_id="a", reason="auth"
    )
    lifecycle = transition_command(
        lifecycle, to_state=CommandState.APPROVED, occurred_at="t2", actor_id="a", reason="ok"
    )
    lifecycle = transition_command(
        lifecycle, to_state=CommandState.DRY_RUN, occurred_at="t3", actor_id="a", reason="dry"
    )
    lifecycle = transition_command(
        lifecycle, to_state=CommandState.EXECUTING, occurred_at="t4", actor_id="a", reason="go"
    )
    lifecycle = transition_command(
        lifecycle, to_state=CommandState.EXECUTED, occurred_at="t5", actor_id="a", reason="done"
    )
    assert lifecycle.state == CommandState.EXECUTED
    assert lifecycle.is_terminal is True
    assert len(lifecycle.transitions) == 5
    assert lifecycle.to_mapping()["contract_version"] == "S355.1"


def test_lifecycle_is_append_only_and_immutable():
    lifecycle = start_command_lifecycle("cmd-1")
    next_lifecycle = transition_command(
        lifecycle, to_state=CommandState.AUTHORIZED, occurred_at="t", actor_id="a"
    )
    # The original is unchanged.
    assert lifecycle.state == CommandState.PROPOSED
    assert next_lifecycle.state == CommandState.AUTHORIZED
    with pytest.raises(FrozenInstanceError):
        next_lifecycle.state = CommandState.EXECUTED


def test_rejects_illegal_transition():
    lifecycle = start_command_lifecycle("cmd-1")
    with pytest.raises(CommandLifecycleError, match="illegal transition"):
        transition_command(
            lifecycle, to_state=CommandState.EXECUTED, occurred_at="t", actor_id="a"
        )


def test_rejects_transition_from_terminal_state():
    lifecycle = start_command_lifecycle("cmd-1")
    lifecycle = transition_command(
        lifecycle, to_state=CommandState.REJECTED, occurred_at="t1", actor_id="a", reason="no"
    )
    assert lifecycle.is_terminal is True
    with pytest.raises(CommandLifecycleError, match="terminal"):
        transition_command(
            lifecycle, to_state=CommandState.AUTHORIZED, occurred_at="t2", actor_id="a"
        )


def test_rejects_blank_command_id():
    with pytest.raises(CommandLifecycleError, match="command_id"):
        start_command_lifecycle("  ")


def test_transition_validates_inputs():
    lifecycle = start_command_lifecycle("cmd-1")
    with pytest.raises(CommandLifecycleError, match="occurred_at"):
        transition_command(
            lifecycle, to_state=CommandState.AUTHORIZED, occurred_at="", actor_id="a"
        )
    with pytest.raises(CommandLifecycleError, match="actor_id"):
        transition_command(
            lifecycle, to_state=CommandState.AUTHORIZED, occurred_at="t", actor_id=""
        )


def test_proposed_can_be_rejected_or_cancelled():
    rejected = start_command_lifecycle("cmd-1")
    rejected = transition_command(rejected, to_state=CommandState.REJECTED, occurred_at="t", actor_id="a")
    assert rejected.state == CommandState.REJECTED

    cancelled = start_command_lifecycle("cmd-2")
    cancelled = transition_command(cancelled, to_state=CommandState.CANCELLED, occurred_at="t", actor_id="a")
    assert cancelled.state == CommandState.CANCELLED
