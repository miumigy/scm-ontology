from scm_ontology.canonical_graph import CanonicalGraph


def test_from_mapping_accepts_current_and_legacy_relationship_shapes() -> None:
    graph = CanonicalGraph.from_mapping(
        {
            "nodes": [{"id": "supplier", "type": "Supplier", "properties": {}}],
            "relationships": [
                {
                    "id": "r-current",
                    "from": "supplier",
                    "predicate": "supplies",
                    "to": "factory",
                    "versions": [{"valid_from": "2026-01-01T00:00:00+00:00"}],
                },
                {
                    "instance": {
                        "relationship_id": "r-legacy",
                        "from_id": "supplier",
                        "predicate": "supplies",
                        "to_id": "factory",
                    },
                    "versions": [{
                        "valid_from": "2026-02-01T00:00:00+00:00",
                        "qualifiers": {"lead_time_days": 3},
                    }],
                },
            ],
        }
    )

    assert len(graph.relationships) == 2
    assert graph.relationships[0].instance.relationship_id == "r-current"
    assert graph.relationships[1].instance.relationship_id == "r-legacy"
    assert graph.relationships[1].versions[0].qualifiers["lead_time_days"] == 3
