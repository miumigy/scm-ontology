from scm_ontology.canonical_graph import CanonicalGraph
from scm_ontology.semantic_query import semantic_supply_chain_paths
from scm_ontology.temporal_traversal import TemporalPath


def test_semantic_supply_chain_query_enriches_temporal_path() -> None:
    graph = CanonicalGraph.from_mapping({
        "nodes": [
            {"id": "supplier", "type": "Supplier", "properties": {}},
            {"id": "factory", "type": "Factory", "properties": {}},
        ],
        "relationships": [
            {
                "instance": {
                    "relationship_id": "r1",
                    "predicate": "supplies",
                    "from_id": "supplier",
                    "to_id": "factory",
                },
                "versions": [{"valid_from": "2026-01-01T00:00:00+00:00", "valid_to": None, "qualifiers": {"lead_time_days": 3}}],
            }
        ],
    })
    result = semantic_supply_chain_paths(graph, "2026-06-01T00:00:00+00:00", from_id="supplier", to_id="factory")
    assert len(result) == 1
    assert result[0].steps[0].predicate == "supplies"
    assert result[0].steps[0].qualifiers["lead_time_days"] == 3
