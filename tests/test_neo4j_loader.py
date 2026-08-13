from scm_ontology.neo4j_loader import build_statements


def test_loader_uses_id_as_stable_node_identity():
    dataset = {
        "nodes": [
            {"type": "Product", "id": "P-001", "properties": {"name": "Vehicle A"}}
        ],
        "edges": [],
    }
    statements = build_statements(dataset)
    assert statements == [
        "MERGE (n:Product {id: $node_id}) SET n.name = $p_name"
    ]


def test_loader_creates_relationships_by_canonical_ids():
    dataset = {
        "nodes": [],
        "edges": [
            {"type": "SUPPLIES", "from": "SUP-001", "to": "MAT-001"}
        ],
    }
    statements = build_statements(dataset)
    assert statements == [
        "MATCH (a {id: $from_id}), (b {id: $to_id}) MERGE (a)-[r:SUPPLIES]->(b)"
    ]
