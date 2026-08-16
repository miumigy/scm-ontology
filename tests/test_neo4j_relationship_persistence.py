from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.graph_persistence import CanonicalGraphPersistencePlanner, PersistenceAuthorization
from scm_ontology.neo4j_adapter import Neo4jGraphStoreAdapter
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.relationship_version import RelationshipVersion


def test_neo4j_adapter_transports_relationship_versions() -> None:
    calls = []

    graph = CanonicalGraph(
        nodes=(SemanticNode("p-1", "Product"), SemanticNode("f-1", "Facility")),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("r-1", "p-1", "supplied_by", "f-1"),
                (RelationshipVersion("2026-01-01", "2026-12-31", {"mode": "planned"}),),
            ),
        ),
    )
    plan = CanonicalGraphPersistencePlanner().plan(
        graph, PersistenceAuthorization("d-1", True, "test", "scope-a")
    )

    Neo4jGraphStoreAdapter(lambda query, params: calls.append((query, params))).apply(graph, plan)

    relationships = calls[0][1]["relationships"]
    assert relationships[0]["id"] == "r-1"
    assert relationships[0]["versions"][0]["valid_from"] == "2026-01-01"
    assert relationships[0]["versions"][0]["valid_to"] == "2026-12-31"
