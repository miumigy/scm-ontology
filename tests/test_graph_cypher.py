from pathlib import Path

from scm_ontology.graph import generate_cypher


def test_generated_cypher_uses_id_as_node_identity(tmp_path):
    dataset = tmp_path / "dataset.yaml"
    dataset.write_text(
        """nodes:\n  - type: Product\n    id: P-001\n    properties:\n      name: Vehicle A\nedges: []\n""",
        encoding="utf-8",
    )

    cypher = generate_cypher(dataset)

    assert "MERGE (n:Product {id: 'P-001'})" in cypher
    assert "SET n += {name: 'Vehicle A'}" in cypher
    assert "{id: 'P-001', name: 'Vehicle A'}" not in cypher
