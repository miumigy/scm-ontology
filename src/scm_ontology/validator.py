"""Lightweight validation for SCM Ontology YAML definitions."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
ONTOLOGY = ROOT / "ontology"


def load(name: str):
    with open(ONTOLOGY / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_entities(data):
    errors = []
    entities = data.get("entities", {})
    for name, spec in entities.items():
        if not isinstance(spec, dict):
            errors.append(f"Entity {name}: definition must be an object")
        if not spec.get("description"):
            errors.append(f"Entity {name}: missing description")
        if not isinstance(spec.get("properties", []), list):
            errors.append(f"Entity {name}: properties must be a list")
    return errors


def validate_relationships(data, entity_names):
    errors = []
    for name, spec in data.get("relationships", {}).items():
        if spec.get("from") not in entity_names and spec.get("from") != "*":
            errors.append(f"Relationship {name}: unknown from entity {spec.get('from')}")
        if spec.get("to") not in entity_names and spec.get("to") != "*":
            errors.append(f"Relationship {name}: unknown to entity {spec.get('to')}")
    return errors


def validate():
    entities = load("entities.yaml")
    relationships = load("relationships.yaml")
    errors = []
    if entities.get("version") != "0.1":
        errors.append("entities.yaml must declare version 0.1")
    if relationships.get("version") != "0.1":
        errors.append("relationships.yaml must declare version 0.1")
    errors.extend(validate_entities(entities))
    errors.extend(validate_relationships(relationships, set(entities.get("entities", {}))))
    return errors


if __name__ == "__main__":
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("SCM Ontology validation passed")
