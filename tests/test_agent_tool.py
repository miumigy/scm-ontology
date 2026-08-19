import pytest

from scm_ontology.agent_observation import build_agent_observation
from scm_ontology.agent_tool import (
    AgentProposal,
    AgentToolError,
    AgentToolResult,
    proposal_to_execution_command,
    run_agent_tool,
)
from scm_ontology.execution_command import ExecutionCommand
from scm_ontology.graph_projection import GraphNode, GraphProjection
from scm_ontology.reasoning_input import ReasoningInput


def _observation():
    projection = GraphProjection(
        nodes=(GraphNode("wh-a", "Warehouse", (("on_hand", 5),)),),
        provenance_ids=("p-inv",),
    )
    return build_agent_observation(
        projection,
        question_id="inventory-position",
        agent_id="planner-agent",
        evidence_ids=("e-inv",),
    )


def test_agent_tool_produces_an_immutable_proposal():
    obs = _observation()
    result = run_agent_tool(
        tool_id="replenish-decision",
        agent_id="planner-agent",
        observation=obs,
        propose=lambda o: AgentProposal(
            agent_id="planner-agent",
            context_id="ctx-1",
            action="replenish",
            payload={"quantity": 20},
            rationale="on-hand below reorder point",
            evidence_ids=("e-inv",),
            provenance_ids=("p-inv",),
            confidence=0.9,
        ),
    )
    assert isinstance(result, AgentToolResult)
    assert result.can_mutate is False
    assert result.proposal is not None
    assert result.proposal.action == "replenish"
    assert result.proposal.proposal_id  # content-addressed
    assert result.observation is obs


def test_agent_tool_result_is_deterministic():
    obs = _observation()
    propose = lambda o: AgentProposal(
        agent_id="planner-agent",
        context_id="ctx-1",
        action="replenish",
        payload={"quantity": 20},
        rationale="on-hand low",
        evidence_ids=("e",),
        provenance_ids=("p",),
    )
    kw = dict(tool_id="t", agent_id="planner-agent", observation=obs, propose=propose)
    a = run_agent_tool(**kw)
    b = run_agent_tool(**kw)
    assert a.to_json() == b.to_json()
    assert a.result_id == b.result_id


def test_agent_tool_rejects_non_proposal_return():
    with pytest.raises(AgentToolError):
        run_agent_tool(
            tool_id="t",
            agent_id="planner-agent",
            observation=None,
            propose=lambda o: {"action": "replenish"},  # not an AgentProposal
        )


def test_agent_proposal_requires_context():
    with pytest.raises(AgentToolError):
        AgentProposal(
            agent_id="planner-agent",
            context_id=" ",
            action="replenish",
            payload={},
            rationale="no-op",
        )


def test_proposal_to_execution_command_requires_governance():
    obs = _observation()
    # Build a valid reasoning input from the observation.
    reasoning_input = ReasoningInput(
        context_id="ctx-1",
        observations=(obs.observation,),
        evidence_ids=(obs.observation.evidence_ids),
        provenance_ids=(obs.observation.provenance_ids),
    )
    proposal = AgentProposal(
        agent_id="planner-agent",
        context_id="ctx-1",
        action="replenish",
        payload={"quantity": 20},
        rationale="on-hand below reorder point",
        evidence_ids=obs.observation.evidence_ids,
        provenance_ids=obs.observation.provenance_ids,
        confidence=0.9,
    )
    cmd = proposal_to_execution_command(
        proposal,
        reasoning_input=reasoning_input,
        actor_id="planner",
        authority="supply-chain-manager",
        authorized_at="2026-08-19T01:00:00Z",
        command_type="replenishment",
        command_id="cmd-p10b-1",
    )
    assert isinstance(cmd, ExecutionCommand)
    assert cmd.command_type == "replenishment"
    assert cmd.context_id == "ctx-1"


def test_agent_proposal_payload_is_never_a_mutation():
    proposal = AgentProposal(
        agent_id="planner-agent",
        context_id="ctx-1",
        action="replenish",
        payload={"quantity": 20},
        rationale="low stock",
        evidence_ids=("e",),
        provenance_ids=("p",),
    )
    # The proposal is only a proposed action; it exposes no graph mutation surface.
    mapping = proposal.to_mapping()
    assert "canonical_mutation" not in mapping
    assert "graph" not in mapping
