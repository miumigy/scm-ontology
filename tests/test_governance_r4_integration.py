"""Phase R4 integration: governed loop + audit + replay + policy + lifecycle."""
from scm_ontology.authorization_governance import (
    ApprovalRecord,
    DefaultAuthorizationPolicy,
    authorize_under_policy,
)
from scm_ontology.command_lifecycle import (
    CommandState,
    start_command_lifecycle,
    transition_command,
)
from scm_ontology.decision_runtime import MockReasoningProvider, run_decision_loop
from scm_ontology.execution_runtime import execute_dry_run
from scm_ontology.governed_audit import record_governed_decision, replay_governed_decision
from scm_ontology.graph_reasoning_projection import GraphReasoningObservation


def observation():
    return GraphReasoningObservation(
        question_id="warehouse-stock",
        value={"warehouse": "WH-1", "stock": 5, "threshold": 10},
        evidence_ids=("e-stock-1",),
        provenance_ids=("p-erp-1",),
    )


def test_governed_loop_with_full_governance():
    result = run_decision_loop(
        context_id="ctx-r4-e2e",
        observations=(observation(),),
        provider=MockReasoningProvider(
            provider_id="mock",
            proposal={"action": "replenish", "quantity": 20},
            rationale="low stock",
            confidence=0.9,
        ),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_type="payment-release",
        command_id="cmd-r4-e2e",
    )

    # 1. Policy requires human approval for high-value command type.
    policy = DefaultAuthorizationPolicy(
        policy_id="policy-r4-e2e",
        allowed_authorities=("supply-chain-manager",),
        require_approval_for=("payment-release",),
    )
    approval = ApprovalRecord(
        approval_id="ap-e2e",
        context_id="ctx-r4-e2e",
        command_type="payment-release",
        approver_id="treasury-1",
        approved_at="2026-08-17T19:00:00Z",
    )
    decision = authorize_under_policy(
        result.validated_proposal,
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_type="payment-release",
        policy=policy,
        approvals=(approval,),
    )
    assert decision.context_id == "ctx-r4-e2e"

    # 2. Dry-run the command and record the audit entry.
    dry_run = execute_dry_run(result.execution_command, dry_ran_at="2026-08-17T21:00:01Z")
    entry = record_governed_decision(result, recorded_at="2026-08-17T21:00:00Z", dry_run=dry_run)
    assert entry.audit_id
    assert entry.dry_run.plan.action == "replenish"

    # 3. Replay reproduces the authorized decision.
    replayed = replay_governed_decision(
        entry,
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_type="payment-release",
        command_id="cmd-r4-e2e",
    )
    assert replayed.to_mapping() == decision.to_mapping()

    # 4. Drive the command lifecycle end to end.
    lifecycle = start_command_lifecycle("cmd-r4-e2e")
    for to_state, at, reason in (
        (CommandState.AUTHORIZED, "t1", "authorized"),
        (CommandState.APPROVED, "t2", "approved"),
        (CommandState.DRY_RUN, "t3", "dry-run complete"),
        (CommandState.EXECUTING, "t4", "sent to adapter"),
        (CommandState.EXECUTED, "t5", "completed"),
    ):
        lifecycle = transition_command(
            lifecycle, to_state=to_state, occurred_at=at, actor_id="planner-1", reason=reason
        )
    assert lifecycle.state == CommandState.EXECUTED
    assert lifecycle.is_terminal is True
    assert len(lifecycle.transitions) == 5


def test_governance_denies_without_approval():
    result = run_decision_loop(
        context_id="ctx-r4-noapproval",
        observations=(observation(),),
        provider=MockReasoningProvider(
            provider_id="mock",
            proposal={"action": "replenish", "quantity": 20},
            rationale="low stock",
        ),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_type="payment-release",
        command_id="cmd-r4-noapproval",
    )
    policy = DefaultAuthorizationPolicy(
        policy_id="policy-pay",
        allowed_authorities=("supply-chain-manager",),
        require_approval_for=("payment-release",),
    )
    from scm_ontology.authorization_governance import AuthorizationGovernanceError
    try:
        authorize_under_policy(
            result.validated_proposal,
            actor_id="planner-1",
            authority="supply-chain-manager",
            authorized_at="2026-08-17T21:00:00Z",
            command_type="payment-release",
            policy=policy,
        )
        raise AssertionError("expected deny without approval")
    except AuthorizationGovernanceError:
        pass
