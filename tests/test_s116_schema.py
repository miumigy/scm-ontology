from __future__ import annotations

import json
from pathlib import Path


SCHEMA = Path(__file__).parents[1] / "schemas" / "canonical-ontology.schema.json"


def test_schema_is_valid_json() -> None:
    schema = json.loads(SCHEMA.read_text())
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["required"] == ["ontology", "version", "concepts", "relationships"]


def test_schema_preserves_s113_dimensions() -> None:
    schema = json.loads(SCHEMA.read_text())
    concept = schema["$defs"]["concept"]
    assert set(concept["properties"]["layer"]["enum"]) == {
        "primitive", "core", "derived", "contextual"
    }
    assert set(concept["properties"]["dimension"]["enum"]) == {
        "physical", "information", "decision", "semantic"
    }


def test_schema_preserves_s114_attribute_semantics() -> None:
    schema = json.loads(SCHEMA.read_text())
    attribute = schema["$defs"]["attribute"]
    assert "value_type" in attribute["required"]
    assert "role" in attribute["required"]
    assert "cardinality" in attribute["required"]


def test_schema_preserves_relationship_signature() -> None:
    schema = json.loads(SCHEMA.read_text())
    relationship = schema["$defs"]["relationship"]
    assert relationship["required"] == ["predicate", "source", "target", "category"]
