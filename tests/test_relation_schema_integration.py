import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).parents[1]


def test_canonical_relation_is_accepted() -> None:
    schema = json.loads((ROOT / "schemas" / "canonical-assertion-set.schema.json").read_text())
    payload = {
        "entity_assertions": [],
        "relation_assertions": [{
            "assertion_ref": "a:1",
            "subject_ref": "order:1",
            "predicate_ref": "fulfills",
            "object_ref": "demand:1",
            "qualifiers": {},
            "context": {
                "assertion_ref": "a:1",
                "semantic_context": {"assertion_ref": "a:1", "subject_ref": "order:1"},
                "qualifiers": {},
            },
        }],
        "metadata": {},
    }
    Draft202012Validator(schema).validate(payload)


def test_non_canonical_relation_is_rejected() -> None:
    schema = json.loads((ROOT / "schemas" / "canonical-assertion-set.schema.json").read_text())
    payload = {
        "entity_assertions": [],
        "relation_assertions": [{
            "assertion_ref": "a:1",
            "subject_ref": "order:1",
            "predicate_ref": "ships_to_customer_system_specific",
            "object_ref": "demand:1",
            "qualifiers": {},
            "context": {
                "assertion_ref": "a:1",
                "semantic_context": {"assertion_ref": "a:1", "subject_ref": "order:1"},
                "qualifiers": {},
            },
        }],
        "metadata": {},
    }
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors
