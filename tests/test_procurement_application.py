from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.procurement_application import (
    ProcurementApplicationError,
    ProcurementObservation,
    run_procurement_application,
)


def observation(shortage=10.0):
    return ProcurementObservation(
        item_id="ITEM-1",
        shortage=shortage,
        unit="unit",
        supplier_id="SUP-7",
        evidence_ids=("e-gap-1",),
        provenance_ids=("p-erp-1",),
    )


def run_args(**overrides):
    args = dict(
        context_id="ctx-r5-procure",
        actor_id="buyer-1",
        authority="procurement-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_id="cmd-r5-procure",
        dry_ran_at="2026-08-17T21:00:01Z",
    )
    args.update(overrides)
    return args


def test_shortage_drives_governed_loop_to_command_and_dry_run():
    decision = run_procurement_application(observation(shortage=10.0), **run_args())
    assert decision.is_procure is True
    assert decision.item_id == "ITEM-1"
    assert decision.quantity == 10.0
    governed = decision.governed
    assert governed is not None
    command = governed.decision.execution_command
    assert command.context_id == "ctx-r5-procure"
    assert command.command_type == "procurement-order"
    assert command.command_id == "cmd-r5-procure"
    assert governed.dry_run.plan.action == "procure"


def test_procure_preserves_evidence_and_provenance():
    decision = run_procurement_application(observation(shortage=10.0), **run_args())
    command_mapping = decision.governed.decision.execution_command.to_mapping()
    assert command_mapping["evidence_ids"] == ["e-gap-1"]
    assert command_mapping["provenance_ids"] == ["p-erp-1"]


def test_zero_shortage_returns_no_procurement():
    decision = run_procurement_application(observation(shortage=0.0), **run_args())
    assert decision.action == "no_procurement"
    assert decision.is_procure is False
    assert decision.quantity == 0.0
    assert decision.governed is None


def test_application_is_deterministic():
    a = run_procurement_application(observation(shortage=10.0), **run_args())
    b = run_procurement_application(observation(shortage=10.0), **run_args())
    assert a.to_mapping()["governed"]["dry_run"]["result_id"] == b.to_mapping()["governed"]["dry_run"]["result_id"]


def test_application_validates_inputs():
    with pytest.raises(ProcurementApplicationError, match="item_id"):
        ProcurementObservation(item_id="", shortage=1.0)
    with pytest.raises(ProcurementApplicationError, match="shortage"):
        ProcurementObservation(item_id="I", shortage=-1.0)
    with pytest.raises(ProcurementApplicationError, match="context_id"):
        run_procurement_application(observation(), **run_args(context_id=""))
    with pytest.raises(ProcurementApplicationError, match="ProcurementObservation"):
        run_procurement_application(object(), **run_args())


def test_observation_projection_is_deterministic():
    obs = observation(shortage=10.0)
    projected = obs.to_observation("ctx-x")
    assert projected.question_id == "demand-supply-shortage"
    assert projected.value["shortage"] == 10.0
    assert projected.evidence_ids == ("e-gap-1",)
    assert projected.provenance_ids == ("p-erp-1",)


def test_decision_is_immutable():
    decision = run_procurement_application(observation(shortage=10.0), **run_args())
    with pytest.raises(FrozenInstanceError):
        decision.action = "cancel"
