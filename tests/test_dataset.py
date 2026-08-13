from pathlib import Path

from scm_ontology.dataset import load_dataset, validate_dataset


ROOT = Path(__file__).resolve().parents[1]


def test_automotive_dataset_is_semantically_valid():
    dataset = load_dataset(ROOT / "examples" / "automotive" / "data.yaml")
    errors = validate_dataset(dataset, ontology_dir=ROOT / "ontology")
    assert errors == []
