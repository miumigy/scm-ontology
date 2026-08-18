from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.authorization_governance import AuthorizationDecision
from scm_ontology.command_lifecycle import (
    CommandLifecycle,
    CommandState,
    start_command_lifecycle,
    transition_command,
)
from scm_ontology.distribution_application import (
    DistributionObservation,
    run_distribution_application,
)
from scm_ontology.execution_workspace import (
    CommandExecution,
    ExecutionWorkspaceError,
    build_execution_workspace,
    launch_execution_workflow,
    workspace_execution,
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
        context_id="ctx-exec",
        authoritative="supply-chain-manager",
        authorized_at="2026-08-18T14:00:00Z",
        dry_ran_at="2026-08-18T14:00:01Z",
    )
    args.update(overrides)
    return args


def replenish_governed(**overrides):
    args = run_args()
    args.update(overrides)
    return run_replenishment_application(
        ReplenishmentObservation(
            product_id="P-1", location_id="WH-1", on_hand=5.0,
            reorder_point=10.0, reorder_quantity=25.0,
            evidence_ids=("e1",), provenance_ids=("p1",),
        ),
        command_id="cmd-r",
        context_id=args["context_id"], actor_id="planner-1",
        authority=args["authoritative"], authorized_at=args["authorized_at"],
        dry_ran_at=args["dry_ran_at"],
    ).governed


def produce_governed(**overrides):
    args = run_args()
    args.update(overrides)
    return run_production_application(
        ProductionObservation(
            resource_id="LINE-1", required=80.0, capacity=100.0,
            evidence_ids=("e2",), provenance_ids=("p2",),
        ),
        command_id="cmd-p",
        context_id=args["context_id"], actor_id="planner-1",
        authority=args["authoritative"], authorized_at=args["authorized_at"],
        dry_ran_at=args["dry_ran_at"],
    ).governed


def escalate_governed(**overrides):
    args = run_args()
    args.update(overrides)
    return run_distribution_application(
        DistributionObservation(
            shipment_id="S", item_id="I", required_quantity=120.0, capacity=100.0,
            origin_location_id="WH", destination_location_id="DC",
            evidence_ids=("e3",), provenance_ids=("p3",),
        ),
        command_id="cmd-d",
        context_id=args["context_id"], actor_id="planner-1",
        authority=args["authoritative"], authorized_at=args["authorized_at"],
        dry_ran_at=args["dry_ran_at"],
    ).governed


def compose_command(*, command_id="cmd-r", command_type="replenishment", dry_run=True, audit=True, approval=True):
    lifecycle = transition_command(
        transition_command(
            transition_command(
                start_command_lifecycle(command_id),
                to_state=CommandState.AUTHORIZED, occurred_at="T", actor_id="a",
            ),
            to_state=CommandState.APPROVED, occurred_at="T", actor_id="a",
        ),
        to_state=CommandState.DRY_RUN, occurred_at="T", actor_id="a",
    )
    gov = replenish_governed()
    py_dry_run = gov.dry_run if dry_run else None
    py_audit = None
    if audit:
        from scm_ontology.governed_audit import record_governed_decision
        py_audit = record_governed_decision(gov.decision, recorded_at="T", dry_run=py_dry_run)
    py_approval = AuthorizationDecision(
        allowed=True, policy_id="p1", requires_approval=True, reason="ok"
    ) if approval else None
    return CommandExecution(
        command_id=command_id, command_type=command_type,
        lifecycle=lifecycle, dry_run=py_dry_run, audit=py_audit,
        authorization=py_approval,
    )


def workspace(**overrides):
    args = dict(created_at="2026-08-18T14:00:02Z", view_actor_id="operator-1")
    args.update(overrides)
    return build_execution_workspace((compose_command(),), **args)


def test_workspace_versioned_and_labeled():
    ws = workspace()
    m = ws.to_mapping()
    assert m["contract_version"] == "P6D.1"
    assert m["is_execution_workspace"] is True
    assert m["view_actor_id"] == "operator-1"


def test_execution_step_projects_lifecycle_dry_run_audit():
    ws = workspace()
    step = ws.steps[0]
    m = step.to_mapping()
    assert m["kind"] == "execution"
    assert m["state"] == "dry_run"
    assert m["is_terminal"] is False
    assert m["approval"] == "approved"
    assert m["dry_run_status"] == "dry-run"
    assert m["dry_run_result_id"]
    assert m["audit_id"]
    assert len(m["transitions"]) == 3


def test_approval_pending_when_not_approved():
    cmd = compose_command(command_id="cmd-x", approval=False)
    cmd = CommandExecution(
        command_id="cmd-x", command_type="replenishment",
        lifecycle=CommandLifecycle(
            command_id="cmd-x", state=CommandState.AUTHORIZED,
            transitions=(),
        ),
    )
    ws = build_execution_workspace((cmd,), **{"created_at": "T", "view_actor_id": "a"})
    assert ws.steps[0].approval == "pending"


def test_approval_denied_when_policy_denies():
    cmd = CommandExecution(
        command_id="cmd-x", command_type="replenishment",
        lifecycle=CommandLifecycle(command_id="cmd-x", state=CommandState.APPROVED, transitions=()),
        authorization=AuthorizationDecision(allowed=False, policy_id="p", reason="denied"),
    )
    ws = build_execution_workspace((cmd,), **{"created_at": "T", "view_actor_id": "a"})
    assert ws.steps[0].approval == "denied"


def test_summary_counts():
    ws = launch_execution_workflow(
        governed_runs=(replenish_governed(),),
        actor_id="planner-1", recorded_at="2026-08-18T14:00:02Z",
    )
    s = ws.to_mapping()["summary"]
    assert s["command_count"] == 1
    assert s["approved_count"] == 1
    assert s["dry_run_count"] == 1
    assert s["audit_count"] == 1
    assert s["terminal_count"] == 0


def test_workspace_is_deterministic_and_content_addressed():
    a = workspace()
    b = workspace()
    assert a.to_json() == b.to_json()
    assert a.workspace_id == b.workspace_id
    c = build_execution_workspace((compose_command(),), **{"created_at": "2026-08-18T15:00:00Z", "view_actor_id": "x"})
    assert a.workspace_id != c.workspace_id


def test_workspace_is_immutable():
    ws = workspace()
    with pytest.raises(FrozenInstanceError):
        ws.created_at = "mutated"


def test_reference_path_composes_runs():
    ws = launch_execution_workflow(
        governed_runs=(replenish_governed(), produce_governed()),
        actor_id="planner-1", recorded_at="2026-08-18T14:00:02Z",
    )
    assert len(ws.steps) == 2
    assert ws.steps[0].command_type == "replenishment"
    assert ws.steps[1].command_type == "production-order"


def test_rejects_empty_commands():
    with pytest.raises(ExecutionWorkspaceError, match="commands must not be empty"):
        build_execution_workspace((), **{"created_at": "T", "view_actor_id": "a"})


def test_rejects_duplicate_command_ids():
    a = compose_command()
    b = compose_command(command_id="cmd-r")
    with pytest.raises(ExecutionWorkspaceError, match="command ids must be unique"):
        build_execution_workspace((a, b), **{"created_at": "T", "view_actor_id": "a"})


def test_rejects_blank_created_at():
    with pytest.raises(ExecutionWorkspaceError, match="created_at"):
        build_execution_workspace((compose_command(),), **{"created_at": "", "view_actor_id": "a"})


def test_command_execution_rejects_mismatched_lifecycle():
    with pytest.raises(ExecutionWorkspaceError, match="must match command_id"):
        CommandExecution(
            command_id="cmd-a", command_type="t",
            lifecycle=CommandLifecycle(command_id="cmd-b", state=CommandState.PROPOSED, transitions=()),
        )


def test_command_execution_rejects_bad_dry_run():
    with pytest.raises(ExecutionWorkspaceError, match="dry_run must be"):
        CommandExecution(
            command_id="cmd-a", command_type="t",
            lifecycle=CommandLifecycle(command_id="cmd-a", state=CommandState.PROPOSED, transitions=()),
            dry_run=object(),
        )


def test_workspace_execution_projects_read_only():
    gov = replenish_governed()
    lifecycle = start_command_lifecycle("cmd-r")
    step = workspace_execution(
        lifecycle, command_type="replenishment",
        dry_run=gov.dry_run,
    )
    assert step.dry_run_result_id == gov.dry_run.result_id
    assert step.audit_id is None
