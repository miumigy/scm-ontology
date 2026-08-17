from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.replenishment_application import (
    ReplenishmentApplicationError,
    ReplenishmentObservation,
    build_replenishment_provider,
    run_replenishment_application,
)


def observation(on_hand=5.0):
    return ReplenishmentObservation(
        product_id="P-1",
        location_id="WH-1",
        on_hand=on_hand,
        reorder_point=10.0,
        reorder_quantity=25.0,
        unit="unit",
        evidence_ids=("e-stock-1",),
        provenance_ids=("p-erp-1",),
    )


def run_args(**overrides):
    args = dict(
        context_id="ctx-r5-replenish",
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_id="cmd-r5-replenish",
        dry_ran_at="2026-08-17T21:00:01Z",
    )
    args.update(overrides)
    return args


def test_below_reorder_point_drives_governed_loop_to_command_and_dry_run():
    decision = run_replenishment_application(observation(on_hand=5.0), **run_args())
    assert decision.is_replenish is True
    assert decision.product_id == "P-1"
    assert decision.location_id == "WH-1"
    assert decision.quantity == 25.0
    governed = decision.governed
    assert governed is not None
    # The governed loop produced an immutable command bound to the context.
    command = governed.decision.execution_command
    assert command.context_id == "ctx-r5-replenish"
    assert command.command_type == "replenishment"
    assert command.command_id == "cmd-r5-replenish"
    # The dry run reflects the proposed action.
    assert governed.dry_run.plan.action == "replenish"
    assert governed.dry_run.plan.execution_target == "in-memory-dry-run"


def test_replenish_preserves_evidence_and_provenance():
    decision = run_replenishment_application(observation(on_hand=5.0), **run_args())
    command_mapping = decision.governed.decision.execution_command.to_mapping()
    assert command_mapping["evidence_ids"] == ["e-stock-1"]
    assert command_mapping["provenance_ids"] == ["p-erp-1"]


def test_at_or_above_reorder_point_returns_no_replenishment():
    decision = run_replenishment_application(observation(on_hand=10.0), **run_args())
    assert decision.action == "no_replenishment"
    assert decision.is_replenish is False
    assert decision.quantity == 0.0
    assert decision.governed is None


def test_above_reorder_point_returns_no_replenishment():
    decision = run_replenishment_application(observation(on_hand=20.0), **run_args())
    assert decision.action == "no_replenishment"
    assert decision.governed is None


def test_application_is_deterministic():
    a = run_replenishment_application(observation(on_hand=5.0), **run_args())
    b = run_replenishment_application(observation(on_hand=5.0), **run_args())
    # Re-runs share context/command ids and serialized mappings.
    assert a.to_mapping()["governed"]["dry_run"]["result_id"] == b.to_mapping()["governed"]["dry_run"]["result_id"]


def test_provider_replenishes_below_reorder_point_only():
    from scm_ontology.reasoning_assembly import assemble_reasoning_input
    low = observation(on_hand=5.0)
    high = observation(on_hand=20.0)
    provider = build_replenishment_provider(low)
    low_input = assemble_reasoning_input("ctx-1", (low.to_observation("ctx-1"),))
    assert provider.reason(low_input).proposal["action"] == "replenish"
    # The provider fails closed when on-hand is at/above the reorder point.
    from scm_ontology.rule_reasoning_provider import RuleReasoningProviderError
    high_input = assemble_reasoning_input("ctx-2", (high.to_observation("ctx-2"),))
    with pytest.raises(RuleReasoningProviderError):
        provider.reason(high_input)


def test_observation_projection_is_deterministic():
    obs = observation(on_hand=5.0)
    projected = obs.to_observation("ctx-x")
    assert projected.question_id == "inventory-position"
    assert projected.value["on_hand"] == 5.0
    assert projected.evidence_ids == ("e-stock-1",)
    assert projected.provenance_ids == ("p-erp-1",)


def test_application_validates_inputs():
    with pytest.raises(ReplenishmentApplicationError, match="product_id"):
        ReplenishmentObservation(product_id="", location_id="L", on_hand=1.0, reorder_point=2.0, reorder_quantity=3.0)
    with pytest.raises(ReplenishmentApplicationError, match="on_hand"):
        ReplenishmentObservation(product_id="P", location_id="L", on_hand="x", reorder_point=2.0, reorder_quantity=3.0)
    with pytest.raises(ReplenishmentApplicationError, match="context_id"):
        run_replenishment_application(observation(), **run_args(context_id=""))
    with pytest.raises(ReplenishmentApplicationError, match="ReplenishmentObservation"):
        run_replenishment_application(object(), **run_args())


def test_decision_is_immutable():
    decision = run_replenishment_application(observation(on_hand=5.0), **run_args())
    with pytest.raises(FrozenInstanceError):
        decision.action = "stop"
