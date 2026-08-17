import pytest

from scm_ontology.authorization_governance import (
    ApprovalRecord,
    AuthorizationGovernanceError,
    DecisionOverride,
    DefaultAuthorizationPolicy,
    authorize_under_policy,
    evaluate_authorization_policy,
)
from scm_ontology.decision_runtime import MockReasoningProvider, run_decision_loop
from scm_ontology.graph_reasoning_projection import GraphReasoningObservation


def validated_proposal():
    observation = GraphReasoningObservation(
        question_id="warehouse-stock",
        value={"warehouse": "WH-1", "stock": 5, "threshold": 10},
        evidence_ids=("e-stock-1",),
        provenance_ids=("p-erp-1",),
    )
    return run_decision_loop(
        context_id="ctx-r4-authz",
        observations=(observation,),
        provider=MockReasoningProvider(
            provider_id="mock",
            proposal={"action": "replenish", "quantity": 10},
            rationale="low stock",
        ),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_type="replenishment",
        command_id="cmd-r4-authz",
    ).validated_proposal


def policy():
    return DefaultAuthorizationPolicy(
        policy_id="policy-r4",
        allowed_authorities=("supply-chain-manager",),
        require_approval_for=("payment-release",),
    )


def test_policy_allows_authorized_authority():
    proposal = validated_proposal()
    decision = evaluate_authorization_policy(
        policy(),
        proposal=proposal,
        actor_id="planner-1",
        authority="supply-chain-manager",
        command_type="replenishment",
    )
    assert decision.allowed is True
    assert decision.requires_approval is False


def test_policy_denies_unknown_authority():
    proposal = validated_proposal()
    decision = evaluate_authorization_policy(
        policy(),
        proposal=proposal,
        actor_id="intern-1",
        authority="intern",
        command_type="replenishment",
    )
    assert decision.allowed is False


def test_policy_marks_high_value_command_for_approval():
    proposal = validated_proposal()
    decision = evaluate_authorization_policy(
        policy(),
        proposal=proposal,
        actor_id="planner-1",
        authority="supply-chain-manager",
        command_type="payment-release",
    )
    assert decision.allowed is True
    assert decision.requires_approval is True


def test_authorize_under_policy_allows_routine_decision():
    proposal = validated_proposal()
    decision = authorize_under_policy(
        proposal,
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_type="replenishment",
        policy=policy(),
    )
    assert decision.context_id == "ctx-r4-authz"


def test_authorize_under_policy_fails_closed_on_denied_authority():
    proposal = validated_proposal()
    with pytest.raises(AuthorizationGovernanceError, match="denied by policy-r4"):
        authorize_under_policy(
            proposal,
            actor_id="intern-1",
            authority="intern",
            authorized_at="t",
            command_type="replenishment",
            policy=policy(),
        )


def test_authorize_requires_approval_for_high_value():
    proposal = validated_proposal()
    with pytest.raises(AuthorizationGovernanceError, match="approval"):
        authorize_under_policy(
            proposal,
            actor_id="planner-1",
            authority="supply-chain-manager",
            authorized_at="t",
            command_type="payment-release",
            policy=policy(),
        )

    approval = ApprovalRecord(
        approval_id="ap-1",
        context_id="ctx-r4-authz",
        command_type="payment-release",
        approver_id="treasury-1",
        approved_at="2026-08-17T19:00:00Z",
    )
    decision = authorize_under_policy(
        proposal,
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="t",
        command_type="payment-release",
        policy=policy(),
        approvals=(approval,),
    )
    assert decision.context_id == "ctx-r4-authz"


def test_authorize_allows_override_of_denied_authority():
    proposal = validated_proposal()
    with pytest.raises(AuthorizationGovernanceError):
        authorize_under_policy(
            proposal,
            actor_id="intern-1",
            authority="intern",
            authorized_at="t",
            command_type="replenishment",
            policy=policy(),
        )
    override = DecisionOverride(
        override_id="ov-1",
        context_id="ctx-r4-authz",
        actor_id="intern-1",
        authority="intern",
        overridden_at="2026-08-17T20:00:00Z",
        reason="approved in writing by country head",
    )
    decision = authorize_under_policy(
        proposal,
        actor_id="intern-1",
        authority="intern",
        authorized_at="t",
        command_type="replenishment",
        policy=policy(),
        overrides=(override,),
    )
    assert decision.context_id == "ctx-r4-authz"


def test_approval_and_override_validate_required_fields():
    with pytest.raises(AuthorizationGovernanceError, match="approval_id"):
        ApprovalRecord(approval_id="", context_id="c", command_type="t", approver_id="a", approved_at="t")
    with pytest.raises(AuthorizationGovernanceError, match="context_id"):
        DecisionOverride(override_id="o", context_id="", actor_id="a", authority="x", overridden_at="t")


def test_default_policy_validates_construction():
    with pytest.raises(AuthorizationGovernanceError, match="allowed_authorities"):
        DefaultAuthorizationPolicy(policy_id="p", allowed_authorities=())
