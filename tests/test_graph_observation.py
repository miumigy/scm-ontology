from scm_ontology.decision_context import DecisionObservation
from scm_ontology.graph_observation import graph_query_to_observation
from scm_ontology.graph_projection import GraphNode, GraphProjection, GraphRelationship
from scm_ontology.graph_query import query_nodes


def projection():
    a = GraphNode("a", "Location", (("name", "東京"),))
    b = GraphNode("b", "Location", (("name", "大阪"),))
    r = GraphRelationship("r1", "LANE", "a", "b")
    return GraphProjection((b, a), (r,), ("p2", "p1"))


def test_graph_query_becomes_existing_decision_observation():
    result = query_nodes(projection(), node_type="Location")
    observation = graph_query_to_observation(result, question_id="q1", query_id="query-1")

    assert isinstance(observation, DecisionObservation)
    assert observation.question_id == "q1"
    assert observation.value["query_id"] == "query-1"
    assert observation.value["result"]["nodes"][0]["node_id"] == "a"
    assert observation.evidence_ids == ("a", "b")
    assert observation.provenance_ids == ("p1", "p2")


def test_graph_query_observation_rejects_blank_identifiers():
    result = query_nodes(projection(), node_type="Location")
    try:
        graph_query_to_observation(result, question_id=" ", query_id="q")
    except ValueError:
        pass
    else:
        raise AssertionError("blank question_id must fail")
