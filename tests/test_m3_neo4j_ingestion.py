from pathlib import Path

from scm_ontology.graph import load_yaml
from scm_ontology.neo4j_loader import build_statements


ROOT = Path(__file__).resolve().parents[1]


def test_automotive_dataset_builds_idempotent_node_and_relationship_merges():
    dataset = load_yaml(ROOT / "examples" / "automotive" / "data.yaml")
    statements = build_statements(dataset)

    node_count = len(dataset["nodes"])
    node_statements = statements[:node_count]
    edge_statements = statements[node_count:]

    assert len(node_statements) == node_count
    assert len(edge_statements) == len(dataset["edges"])
    assert all("MERGE (n:" in s and "{id: $node_id}" in s for s in node_statements)
    assert all("MERGE (a)-[r:" in s for s in edge_statements)


def test_mutable_property_change_preserves_canonical_identity():
    first = {
        "nodes": [{"type": "Product", "id": "P-001", "properties": {"name": "Vehicle A"}}],
        "edges": [],
    }
    second = {
        "nodes": [{"type": "Product", "id": "P-001", "properties": {"name": "Vehicle B"}}],
        "edges": [],
    }

    first_statement = build_statements(first)[0]
    second_statement = build_statements(second)[0]

    assert first_statement.split(" SET ", 1)[0] == second_statement.split(" SET ", 1)[0]
    assert "{id: $node_id}" in first_statement
    assert "{id: $node_id}" in second_statement
