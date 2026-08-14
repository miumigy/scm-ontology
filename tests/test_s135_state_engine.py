import pytest

from scm_ontology.s135_state_engine import (
    State,
    StateEpistemicStatus,
    StateTransition,
    reconstruct_state,
)


def test_state_preserves_temporal_and_provenance_context() -> None:
    state = reconstruct_state(
        ref="state:inventory:1",
        subject_ref="inventory:sku-1:warehouse-a",
        state_type="inventory_quantity",
        value=120,
        effective_from="2026-08-15T09:00:00Z",
        transaction_time="2026-08-15T09:05:00Z",
        provenance_refs=("event:receipt:1",),
        epistemic_status=StateEpistemicStatus.OBSERVED,
    )
    assert state.effective_from != state.transaction_time
    assert state.provenance_refs == ("event:receipt:1",)


def test_scenario_state_isolated_from_actual_state() -> None:
    state = State(
        ref="state:scenario:1",
        subject_ref="inventory:sku-1:warehouse-a",
        state_type="inventory_quantity",
        value=180,
        scenario_ref="scenario:capacity-up",
        epistemic_status=StateEpistemicStatus.PREDICTED,
    )
    assert state.is_scenario_state is True
    assert state.epistemic_status is StateEpistemicStatus.PREDICTED


def test_unknown_is_not_zero() -> None:
    state = reconstruct_state(
        ref="state:unknown",
        subject_ref="inventory:sku-2:warehouse-b",
        state_type="inventory_quantity",
        value=None,
        epistemic_status=StateEpistemicStatus.UNKNOWN,
    )
    assert state.value is None
    assert state.epistemic_status is StateEpistemicStatus.UNKNOWN


def test_transition_is_distinct_from_action() -> None:
    transition = StateTransition(
        ref="transition:1",
        prior_state_ref="state:before",
        resulting_state_ref="state:after",
        triggering_event_ref="event:1",
        actor_ref="system:wms",
    )
    assert transition.resulting_state_ref == "state:after"
    assert transition.triggering_event_ref != "action:1"


def test_state_requires_subject_and_type() -> None:
    with pytest.raises(ValueError):
        State(ref="state:bad", subject_ref="", state_type="", value=0)
