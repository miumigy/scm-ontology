import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).parents[1]


def test_end_to_end_fixture_validates() -> None:
    schema = json.loads((ROOT / "schemas" / "canonical-assertion-set.schema.json").read_text())
    fixture = json.loads((ROOT / "examples" / "reference-canonicalization" / "reference_end_to_end_scm.json").read_text())
    Draft202012Validator(schema).validate(fixture)


def test_end_to_end_fixture_covers_core_scm_objects() -> None:
    fixture = json.loads((ROOT / "examples" / "reference-canonicalization" / "reference_end_to_end_scm.json").read_text())
    subjects = {item["subject_ref"] for item in fixture["entity_assertions"]}
    assert {"demand:001", "order:001", "supply:001", "inventory:001"} <= subjects
