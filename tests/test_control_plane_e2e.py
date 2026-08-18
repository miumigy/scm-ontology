from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.control_plane_e2e import (
    ControlPlaneE2EError,
    ControlPlaneE2EResult,
    ControlPlaneRequest,
    ControlPlaneStage,
    run_control_plane_flow,
)


def request(**overrides):
    args = dict(
        context_id="ctx-e2e",
        operator_id="operator-1",
        authority="supply-chain-manager",
        observed_at="2026-08-18T15:00:00Z",
    )
    args.update(overrides)
    return ControlPlaneRequest(**args)


def result(**overrides):
    return run_control_plane_flow(request(**overrides))


def test_result_versioned_and_labeled():
    r = result()
    m = r.to_mapping()
    assert m["contract_version"] == "P6E.1"
    assert m["is_control_plane_e2e"] is True
    assert m["request"]["operator_id"] == "operator-1"


def test_chain_traverses_all_stages_in_order():
    r = result()
    stages = [s["stage"] for s in r.to_mapping()["stages"]]
    assert stages == [
        "state", "decision", "simulation_plan",
        "authorization", "workflow", "audit",
    ]


def test_all_surfaces_composed():
    r = result()
    surfaces = r.to_mapping()["surfaces"]
    assert set(surfaces.keys()) == {
        "cockpit", "decision_inbox", "sim_optim_workspace", "execution_workspace",
    }
    assert surfaces["cockpit"]["is_operational_tool"] is True
    assert surfaces["decision_inbox"]["is_decision_inbox"] is True
    assert surfaces["sim_optim_workspace"]["is_workspace"] is True
    assert surfaces["execution_workspace"]["is_execution_workspace"] is True


def test_summary_counts():
    r = result()
    s = r.to_mapping()["summary"]
    assert s["stage_count"] == 6
    assert s["actionable_decision"] is True
    assert s["exception_count"] == 1
    assert s["simulation_steps"] == 2
    assert s["plan_periods"] == 3
    assert s["workflow_steps"] == 1
    assert s["governance_audits"] == 1


def test_decision_is_actionable_with_governed_result():
    r = result()
    decision_stage = r.to_mapping()["stages"][1]
    assert decision_stage["action"] == "replenish"
    assert decision_stage["governed"] is True


def test_authorization_stage_carries_operator_and_authority():
    r = result()
    auth_stage = r.to_mapping()["stages"][3]
    assert auth_stage["actor_id"] == "operator-1"
    assert auth_stage["authority"] == "supply-chain-manager"


def test_inbox_surface_has_one_actionable_item():
    r = result()
    inbox = r.to_mapping()["surfaces"]["decision_inbox"]
    assert inbox["summary"]["actionable_count"] == 1
    assert inbox["items"][0]["status"] == "dry_run"


def test_workspace_surface_has_scenario_and_plan():
    r = result()
    ws = r.to_mapping()["surfaces"]["sim_optim_workspace"]
    assert ws["summary"]["scenario_count"] == 1
    assert ws["summary"]["plan_count"] == 1
    assert ws["plans"][0]["plan_type"] == "replenishment_plan"


def test_execution_surface_reaches_dry_run_with_audit():
    r = result()
    ex = r.to_mapping()["surfaces"]["execution_workspace"]
    assert ex["steps"][0]["state"] == "dry_run"
    assert ex["summary"]["audit_count"] == 1


def test_run_is_deterministic_and_content_addressed():
    a = result()
    b = result()
    assert a.to_json() == b.to_json()
    assert a.run_id == b.run_id
    c = result(observed_at="2026-08-18T16:00:00Z")
    assert a.run_id != c.run_id


def test_result_is_immutable():
    r = result()
    with pytest.raises(FrozenInstanceError):
        r.run_id = "mutated"


def test_request_rejects_blank_fields():
    with pytest.raises(ControlPlaneE2EError, match="context_id"):
        request(context_id="")
    with pytest.raises(ControlPlaneE2EError, match="operator_id"):
        request(operator_id="")


def test_stage_rejects_unknown_stage():
    with pytest.raises(ControlPlaneE2EError, match="unsupported stage"):
        ControlPlaneStage("bogus", {"x": 1})


def test_flow_rejects_non_request():
    with pytest.raises(ControlPlaneE2EError, match="must be a ControlPlaneRequest"):
        run_control_plane_flow(object())


def test_flow_is_deterministic_across_operator_ids():
    a = result(operator_id="op-a")
    b = result(operator_id="op-b")
    # The same scenario yields equal stage detail; only the run id (which hashes
    # operator) and authorization actor change.
    assert a.to_json() != b.to_json()
    assert a.to_mapping()["summary"] == b.to_mapping()["summary"]
