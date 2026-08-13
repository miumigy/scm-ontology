from pathlib import Path

from scm_ontology.graph import validate_graph_dataset

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "examples" / "automotive" / "data.yaml"
RELATIONSHIPS = ROOT / "ontology" / "relationships.yaml"
ENTITIES = ROOT / "ontology" / "entities.yaml"


def test_automotive_graph_dataset_is_valid():
    assert validate_graph_dataset(DATASET, RELATIONSHIPS, ENTITIES) == []


def test_inherited_relationship_endpoint_is_valid(tmp_path):
    dataset = tmp_path / "dataset.yaml"
    dataset.write_text(
        "nodes:\n"
        "  - id: SUP-1\n"
        "    type: Party\n"
        "  - id: MAT-1\n"
        "    type: Material\n"
        "edges:\n"
        "  - type: SUPPLIES\n"
        "    from: SUP-1\n"
        "    to: MAT-1\n",
        encoding="utf-8",
    )
    assert validate_graph_dataset(dataset, RELATIONSHIPS, ENTITIES) == []


def test_unknown_node_property_is_rejected(tmp_path):
    dataset = tmp_path / "dataset.yaml"
    dataset.write_text(
        "nodes:\n"
        "  - id: P-1\n"
        "    type: Product\n"
        "    properties:\n"
        "      notAnOntologyProperty: true\n"
        "edges: []\n",
        encoding="utf-8",
    )
    errors = validate_graph_dataset(dataset, RELATIONSHIPS, ENTITIES)
    assert any("unknown properties" in error for error in errors)
