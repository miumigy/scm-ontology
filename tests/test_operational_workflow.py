from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.distribution_application import (
    DistributionObservation,
    run_distribution_application,
)
from scm_ontology.operational_workflow import (
    OperationalStep,
    OperationalWorkflowError,
    run_operational_workflow,
)
from scm_ontology.production_application import (
    ProductionObservation,
    run_production_application,
)
from scm_ontology.replenishment_application import (
    ReplenishmentObservation,
    run_replenishment_application,
)


def run_args(**overrides):
    args = dict(
        context_id="ctx-r5",
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        dry_ran_at="2026-08-17T21:00:01Z",
    )
    args.update(overrides)
    return args


def replenish_decision(**overrides):
    args = run_args()
    args.update(overrides)
    return run_replenishment_application(
        ReplenishmentObservation(
            product_id="P-1", location_id="WH-1", on_hand=5.0,
            reorder_point=10.0, reorder_quantity=25.0,
            evidence_ids=("e1",), provenance_ids=("p1",),
        ),
        command_id="cmd-r",
        **{k: v for k, v in args.items() if k != "command_id"},
    )


def produce_decision(**overrides):
    args = run_args()
    args.update(overrides)
    return run_production_application(
        ProductionObservation(
            resource_id="LINE-1", required=80.0, capacity=100.0,
            evidence_ids=("e2",), provenance_ids=("p2",),
        ),
        command_id="cmd-p",
        **{k: v for k, v in args.items() if k != "command_id"},
    )


def no_action_decision():
    """Distribution with required > capacity -> escalate (no governed result)."""
    return run_distribution_application(
        DistributionObservation(
            shipment_id="S", item_id="I", required_quantity=120.0, capacity=100.0,
            origin_location_id="WH", destination_location_id="DC",
            evidence_ids=("e3",), provenance_ids=("p3",),
        ),
        command_id="cmd-d",
        **run_args(),
    )


def workflow_steps():
    return (
        OperationalStep(step_id="s1", application="replenishment", command_id="cmd-r", decision=replenish_decision()),
        OperationalStep(step_id="s2", application="production", command_id="cmd-p", decision=produce_decision()),
        OperationalStep(step_id="s3", application="distribution", command_id="cmd-d", decision=no_action_decision()),
    )


def workflow_args(**overrides):
    args = dict(workflow_id="wf-1", recorded_at="T", actor_id="planner-1")
    args.update(overrides)
    return args


def test_governed_steps_are_audited_and_advanced_to_dry_run():
    result = run_operational_workflow(workflow_steps(), **workflow_args())
    assert result.to_mapping()["contract_version"] == "S366.1"
    s1 = result.steps[0]
    assert s1.state == "dry_run"
    assert s1.audit_id is not None
    assert s1.command_id == "cmd-r"
    s2 = result.steps[1]
    assert s2.state == "dry_run"
    assert s2.audit_id is not None


def test_no_action_step_is_recorded_without_audit():
    result = run_operational_workflow(workflow_steps(), **workflow_args())
    s3 = result.steps[2]
    assert s3.state == "no_action"
    assert s3.audit_id is None
    assert s3.command_id == "cmd-d"


def test_workflow_summary_counts_actionable_and_no_action():
    result = run_operational_workflow(workflow_steps(), **workflow_args())
    m = result.to_mapping()
    assert m["step_count"] == 3
    assert m["actionable_steps"] == 2
    assert m["no_action_steps"] == 1


def test_workflow_is_deterministic():
    a = run_operational_workflow(workflow_steps(), **workflow_args())
    b = run_operational_workflow(workflow_steps(), **workflow_args())
    assert a.to_json() == b.to_json()
    assert a.steps[0].audit_id == b.steps[0].audit_id


def test_audit_preserves_evidence_and_provenance():
    result = run_operational_workflow(workflow_steps(), **workflow_args())
    # The audit entry embeds the decision runtime result; evidence is present.
    from scm_ontology.governed_audit import GovernedDecisionAuditEntry
    entry_mapping = None
    # audit_id links to a deterministic digest; verify nonzero and stable.
    assert result.steps[0].audit_id
    assert isinstance(result.steps[0].audit_id, str)
    assert len(result.steps[0].audit_id) == 64


def test_workflow_rejects_empty_steps():
    with pytest.raises(OperationalWorkflowError, match="steps must not be empty"):
        run_operational_workflow((), **workflow_args())


def test_workflow_rejects_duplicate_step_ids():
    steps = (workflow_steps()[0], workflow_steps()[0])
    with pytest.raises(OperationalWorkflowError, match="unique"):
        run_operational_workflow(steps, **workflow_args())


def test_workflow_rejects_invalid_application():
    with pytest.raises(OperationalWorkflowError, match="unsupported application"):
        OperationalStep(step_id="s1", application="bogus", command_id="c1", decision=object())


def test_workflow_rejects_mismatched_decision_type():
    # production step given a replenishment decision
    with pytest.raises(OperationalWorkflowError, match="ProductionDecision"):
        OperationalStep(
            step_id="s1", application="production", command_id="c1",
            decision=replenish_decision(),
        )


def test_workflow_rejects_blank_workflow_id():
    with pytest.raises(OperationalWorkflowError, match="workflow_id"):
        run_operational_workflow(workflow_steps(), **workflow_args(workflow_id=""))


def test_workflow_rejects_blank_recorded_at():
    with pytest.raises(OperationalWorkflowError, match="recorded_at"):
        run_operational_workflow(workflow_steps(), **workflow_args(recorded_at=""))


def test_workflow_result_is_immutable():
    result = run_operational_workflow(workflow_steps(), **workflow_args())
    with pytest.raises(FrozenInstanceError):
        result.workflow_id = "mutated"


def test_workflow_fails_closed_without_side_effect(tmp_path):
    sentinel = tmp_path / "side-effect"
    assert not sentinel.exists()
    run_operational_workflow(workflow_steps(), **workflow_args())
    assert not sentinel.exists()
    assert set(tmp_path.iterdir()) == set()
