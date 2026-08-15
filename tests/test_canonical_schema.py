import json
from pathlib import Path

from jsonschema import Draft202012Validator


def test_canonical_assertion_schema_is_valid() -> None:
    path = Path(__file__).parents[1] / "schemas" / "canonical-assertion-set.schema.json"
    schema = json.loads(path.read_text())
    Draft202012Validator.check_schema(schema)


def test_canonical_assertion_schema_accepts_minimal_payload() -> None:
    path = Path(__file__).parents[1] / "schemas" / "canonical-assertion-set.schema.json"
    schema = json.loads(path.read_text())
    payload = {"entity_assertions": [], "relation_assertions": [], "metadata": {}}
    Draft202012Validator(schema).validate(payload)
