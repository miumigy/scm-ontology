import json
from pathlib import Path

from jsonschema import Draft202012Validator

from scm_ontology.assertion_context import AssertionContext
from scm_ontology.assertion_model import CanonicalAssertionSet, EntityAssertion
from scm_ontology.semantic_context import EpistemicKind, SemanticContext
from scm_ontology.serialization import serialize_assertion_set


ROOT = Path(__file__).parents[1]
SCHEMA_PATH = ROOT / "schemas" / "canonical-assertion-set.schema.json"


def test_serialized_assertion_payload_validates_against_schema() -> None:
    schema = json.loads(SCHEMA_PATH.read_text())
    validator = Draft202012Validator(schema)
    context = AssertionContext("a:1", SemanticContext("a:1", "inventory:1", EpistemicKind.OBSERVATION))
    assertion = EntityAssertion("a:1", "inventory:1", "quantity_on_hand", 100, context)
    payload = serialize_assertion_set(CanonicalAssertionSet((assertion,)))
    validator.validate(payload)


def test_schema_rejects_missing_assertion_context() -> None:
    schema = json.loads(SCHEMA_PATH.read_text())
    validator = Draft202012Validator(schema)
    invalid = {
        "entity_assertions": [{
            "assertion_ref": "a:1",
            "subject_ref": "inventory:1",
            "attribute_ref": "quantity_on_hand",
            "value": 100,
        }],
        "relation_assertions": [],
        "metadata": {},
    }
    errors = list(validator.iter_errors(invalid))
    assert errors
