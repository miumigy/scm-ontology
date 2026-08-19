import pytest

from scm_ontology.agent_observation import build_agent_observation
from scm_ontology.agent_replay import (
    AgentAuditEntry,
    AgentAuditTrail,
    AgentReplayError,
    record_agent_entry,
)
from scm_ontology.agent_tool import AgentProposal
from scm_ontology.graph_projection import GraphNode, GraphProjection
from scm_ontology.human_control import HumanReviewDecision, route_human_control
from scm_ontology.policy_autonomy import (
    AutonomyInput,
    AutonomyLevel,
    AutonomyPolicy,
    evaluate_autonomy,
)


def _observation():
    return build_agent_observation(
        GraphProjection(
            nodes=(GraphNode("wh-a", "Warehouse", (("on_hand", 5),)),),
            provenance_ids=("p-inv",),
        ),
        question_id="inventory-position",
        agent_id="planner-agent",
        evidence_ids=("e-inv",),
    )


def _proposal():
    return AgentProposal(
        agent_id="planner-agent",
        context_id="ctx-1",
        action="replenish",
        payload={"quantity": 20},
        rationale="on-hand below reorder point",
        evidence_ids=("e-inv",),
        provenance_ids=("p-inv",),
        confidence=0.9,
    )


def _autonomy_verdict():
    return evaluate_autonomy(
        _proposal(),
        inputs=AutonomyInput(confidence=0.9, risk=0.1, monetary_impact=100.0, scope="inventory"),
        policy=AutonomyPolicy(
            policy_id="p-inv",
            allowed_by_scope={"inventory": AutonomyLevel.FULLY_AUTONOMOUS},
        ),
    )


def test_record_agent_entry_is_content_addressed():
    entry = record_agent_entry(
        agent_id="planner-agent",
        observation=_observation(),
        proposal=_proposal(),
        autonomy=_autonomy_verdict(),
        outcome_ref="outcome-1",
        recorded_at="2026-08-19T01:00:00Z",
    )
    assert isinstance(entry, AgentAuditEntry)
    assert entry.recorded_at == "2026-08-19T01:00:00Z"
    assert entry.entry_id


def test_agent_audit_trail_is_append_only_and_deterministic():
    trail = AgentAuditTrail(agent_id="planner-agent")
    trail2 = trail.record(
        observation=_observation(),
        proposal=_proposal(),
        recorded_at="2026-08-19T01:00:00Z",
    )
    trail2 = trail2.record(
        outcome_ref="outcome-1",
        recorded_at="2026-08-19T01:00:00Z",
    )
    assert len(trail.entries) == 0  # original unchanged (immutable)
    assert len(trail2.entries) == 2
    assert trail2.agent_id == "planner-agent"
    # Building the same sequence deterministically yields the same trail.
    twin = AgentAuditTrail(agent_id="planner-agent")
    twin = twin.record(observation=_observation(), proposal=_proposal(), recorded_at="2026-08-19T01:00:00Z")
    twin = twin.record(outcome_ref="outcome-1", recorded_at="2026-08-19T01:00:00Z")
    assert trail2.to_json() == twin.to_json()


def test_replay_verifies_content_integrity():
    trail = AgentAuditTrail(agent_id="planner-agent").record(
        observation=_observation(),
        proposal=_proposal(),
        autonomy=_autonomy_verdict(),
        recorded_at="2026-08-19T01:00:00Z",
    )
    replayed = trail.replay()
    assert replayed.to_json() == trail.to_json()
    assert replayed.entries[0].entry_id == trail.entries[0].entry_id


def test_replay_detects_tampering():
    trail = AgentAuditTrail(agent_id="planner-agent").record(
        outcome_ref="outcome-1",
        recorded_at="2026-08-19T01:00:00Z",
    )
    entry = trail.entries[0]
    tampered = AgentAuditEntry(
        entry_id="tampered",
        agent_id=entry.agent_id,
        outcome_ref=entry.outcome_ref,
        recorded_at=entry.recorded_at,
    )
    tampered_trail = AgentAuditTrail(agent_id="planner-agent", entries=(tampered,))
    with pytest.raises(AgentReplayError):
        tampered_trail.replay()


def test_trail_rejects_mixed_agent_entries():
    foreign = record_agent_entry(agent_id="other-agent", recorded_at="t")
    with pytest.raises(AgentReplayError):
        AgentAuditTrail(agent_id="planner-agent", entries=(foreign,))
