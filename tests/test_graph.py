from pathlib import Path

from scm_ontology.graph import validate_graph_dataset

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "examples" / "automotive" / "data.yaml"
RELATIONSHIPS = ROOT / "ontology" / "relationships.yaml"


def test_automotive_graph_dataset_is_valid():
    assert validate_graph_dataset(DATASET, RELATIONSHIPS) == []
