from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "mappings" / "apics-scor.yaml"


def test_apics_scor_mapping_is_framework_to_canonical_crosswalk():
    document = yaml.safe_load(MAPPING.read_text(encoding="utf-8"))

    assert document["version"] == "0.1"
    assert document["mappings"]
    assert all("sourceConcept" in item and "ontology" in item for item in document["mappings"])
    assert all(isinstance(item["ontology"], list) and item["ontology"] for item in document["mappings"])

    principles = document["principles"]
    assert any("not ontology entities" in principle for principle in principles)
    assert any("framework-independent" in principle for principle in principles)


def test_core_apics_scor_concepts_map_to_existing_canonical_types():
    document = yaml.safe_load(MAPPING.read_text(encoding="utf-8"))
    mapping = {item["sourceConcept"]: item["ontology"] for item in document["mappings"]}

    assert "Material Requirements Planning" in mapping
    assert set(["Plan", "BOM", "Material", "Demand", "InventoryPosition", "Constraint"]).issubset(
        mapping["Material Requirements Planning"]
    )
    assert set(["InventoryPosition", "Policy", "Constraint", "KPI"]).issubset(
        mapping["Safety Stock"]
    )
