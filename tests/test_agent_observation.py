import pytest

from scm_ontology.agent_observation import (
    AgentObservation,
    AgentObservationError,
    AgentScope,
    build_agent_observation,
)
from scm_ontology.graph_projection import GraphNode, GraphProjection, GraphRelationship


def _projection() -> GraphProjection:
    return GraphProjection(
        nodes=(
            GraphNode("wh-a", "Warehouse", (("capacity", 100),)),
            GraphNode("loc-b", "Location", (("zone", "north"),)),
        ),
        relationships=(
            GraphRelationship("r1", "ships_to", "wh-a", "loc-b", (("lead_days", 2),)),
        ),
        provenance_ids=("p1", "p2"),
    )


def test_agent_observation_is_scoped_and_read_only():
    observation = build_agent_observation(
        _projection(),
        question_id="warehouse-net",
        agent_id="planner-agent",
        node_type="Warehouse",
    )
    assert isinstance(observation, AgentObservation)
    assert observation.scope.agent_id == "planner-agent"
    assert observation.scope.question_id == "warehouse-net"
    assert observation.scope.node_type == "Warehouse"
    assert observation.can_write is False
    # Only warehouse nodes are observed under the scope; the location is excluded.
    assert [n["node_id"] for n in observation.observation.value["nodes"]] == ["wh-a"]


def test_agent_observation_preserves_provenance_and_evidence():
    projection = GraphProjection(
        nodes=(GraphNode("n1", "Warehouse"),),
        provenance_ids=("p-a", "p-b"),
    )
    observation = build_agent_observation(
        projection,
        question_id="inventory-position",
        agent_id="planner-agent",
    )
    assert observation.observation.provenance_ids == ("p-a", "p-b")


def test_agent_observation_is_content_addressed_and_deterministic():
    kw = dict(
        projection=_projection(),
        question_id="warehouse-net",
        agent_id="planner-agent",
        node_type="Warehouse",
    )
    a = build_agent_observation(**kw)
    b = build_agent_observation(**kw)
    assert a.observation_id == b.observation_id
    assert a.to_json() == b.to_json()
    assert a.observation_id  # non-empty content address for audit/replay


def test_agent_observation_rejects_empty_scope():
    with pytest.raises(AgentObservationError):
        build_agent_observation(
            _projection(),
            question_id=" ",
            agent_id="planner-agent",
        )


def test_agent_scope_rejects_missing_agent():
    with pytest.raises(AgentObservationError):
        AgentScope(question_id="q1", agent_id=" ")


def test_no_write_method_on_observation():
    observation = build_agent_observation(
        _projection(),
        question_id="warehouse-net",
        agent_id="planner-agent",
    )
    # The observation exposes only the read envelopes: scope + observation.
    assert set(observation.to_mapping().keys()) == {
        "contract_version",
        "observation_id",
        "can_write",
        "scope",
        "observation",
    }
