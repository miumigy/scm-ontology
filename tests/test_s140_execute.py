import pytest

from scm_ontology.s140_execute import (
    Action,
    Execution,
    ExecutionStatus,
    execute_action,
)


def test_action_preserves_intent_separately_from_execution() -> None:
    action = Action(
        ref="action:ship:1",
        subject_ref="order:1",
        action_type="ship",
        decision_ref="decision:1",
        plan_ref="plan:1",
        intended_quantity=100,
    )
    assert action.intended_quantity == 100
    assert action.is_execution is False


def test_partial_execution_does_not_overwrite_intended_quantity() -> None:
    action = Action(
        ref="action:ship:1",
        subject_ref="order:1",
        action_type="ship",
        intended_quantity=100,
    )
    execution = execute_action(
        ref="execution:ship:1",
        action_ref=action.ref,
        status=ExecutionStatus.PARTIALLY_COMPLETED,
        actual_quantity=60,
    )
    assert action.intended_quantity == 100
    assert execution.actual_quantity == 60
    assert execution.status is ExecutionStatus.PARTIALLY_COMPLETED


def test_completed_execution_is_not_automatically_successful_outcome() -> None:
    execution = Execution(
        ref="execution:1",
        action_ref="action:1",
        status=ExecutionStatus.COMPLETED,
    )
    assert execution.is_actual_outcome is False
    assert execution.outcome_refs == ()


def test_execution_is_not_event() -> None:
    execution = Execution(ref="execution:1", action_ref="action:1")
    assert execution.is_event is False


def test_scenario_execution_is_scoped() -> None:
    execution = execute_action(
        ref="execution:scenario:1",
        action_ref="action:scenario:1",
        scenario_ref="scenario:1",
        status=ExecutionStatus.COMPLETED,
    )
    assert execution.is_scenario_execution is True


def test_execution_requires_action() -> None:
    with pytest.raises(ValueError):
        Execution(ref="execution:bad", action_ref="")
