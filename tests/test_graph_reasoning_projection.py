from scm_ontology.decision_context import DecisionObservation
from scm_ontology.graph_projection import GraphNode, GraphProjection, GraphRelationship
from scm_ontology.graph_query import GraphQueryResult
from scm_ontology.graph_reasoning_projection import (
    GraphReasoningProjectionError,
    project_graph_to_observation,
    project_query_result_to_observation,
)


def test_query_result_projection_is_deterministic_and_preserves_provenance():
    result = GraphQueryResult(
        nodes=(
            GraphNode("b", "Location"),
            GraphNode("a", "Warehouse"),
        ),
        relationships=(
            GraphRelationship("r2", "ships_to", "a", "b"),
            GraphRelationship("r1", "contains", "a", "b"),
        ),
        provenance_ids=("p2", "p1"),
    )

    observation = project_query_result_to_observation(
        result,
        question_id="warehouse-network",
        evidence_ids=("e2", "e1"),
        provenance_ids=("p3",),
    )

    assert observation.question_id == "warehouse-network"
    assert [node["node_id"] for node in observation.value["nodes"]] == ["a", "b"]
    assert [rel["relationship_id"] for rel in observation.value["relationships"]] == ["r1", "r2"]
    assert observation.evidence_ids == ("e1", "e2")
    assert observation.provenance_ids == ("p1", "p2", "p3")

    decision_observation = observation.to_decision_observation()
    assert isinstance(decision_observation, DecisionObservation)
    assert decision_observation.question_id == "warehouse-network"


def test_graph_projection_to_observation_merges_provenance():
    projection = GraphProjection(
        nodes=(GraphNode("a", "Warehouse"),),
        provenance_ids=("p2", "p1"),
    )

    observation = project_graph_to_observation(
        projection,
        question_id="warehouse-state",
        provenance_ids=("p3",),
    )

    assert observation.provenance_ids == ("p1", "p2", "p3")
    assert observation.value["contract_version"] == "S337.1"


def test_projection_rejects_empty_question_id():
    projection = GraphProjection()

    try:
        project_graph_to_observation(projection, question_id="")
    except GraphReasoningProjectionError as exc:
        assert str(exc) == "question_id must be non-empty"
    else:
        raise AssertionError("expected GraphReasoningProjectionError")
