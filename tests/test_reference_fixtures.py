import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).parents[1]


def test_reference_fixture_validates_against_canonical_schema() -> None:
    schema = json.loads((ROOT / "schemas" / "canonical-assertion-set.schema.json").read_text())
    fixture = json.loads((ROOT / "examples" / "reference_assertion_set.json").read_text())
    Draft202012Validator(schema).validate(fixture)


def test_reference_fixture_preserves_canonical_context() -> None:
    fixture = json.loads((ROOT / "examples" / "reference_assertion_set.json").read_text())
    assertion = fixture["entity_assertions"][0]
    assert assertion["subject_ref"] == "inventory:001"
    assert assertion["context"]["assertion_ref"] == assertion["assertion_ref"]
    assert assertion["context"]["semantic_context"]["subject_ref"] == assertion["subject_ref"]
