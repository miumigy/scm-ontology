from pathlib import Path
import yaml

from scm_ontology.validator import validate

ROOT = Path(__file__).resolve().parents[1]


def test_ontology_valid():
    assert validate() == []


def test_required_entity_families_exist():
    data = yaml.safe_load((ROOT / "ontology/entities.yaml").read_text(encoding="utf-8"))
    entities = set(data["entities"])
    required = {"Party", "Site", "Product", "Demand", "Plan", "Shipment", "Event", "Decision", "KPI"}
    assert required <= entities


def test_required_relationship_families_exist():
    data = yaml.safe_load((ROOT / "ontology/relationships.yaml").read_text(encoding="utf-8"))
    relationships = set(data["relationships"])
    required = {"SUPPLIES", "STOCKS", "REQUIRES", "PLANS", "AFFECTS", "CAUSES", "IMPACTS", "CONSIDERS"}
    assert required <= relationships
