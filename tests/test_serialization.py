from scm_ontology.assertion_context import AssertionContext
from scm_ontology.assertion_model import CanonicalAssertionSet, EntityAssertion
from scm_ontology.semantic_context import EpistemicKind, SemanticContext
from scm_ontology.serialization import is_json_compatible, serialize_assertion_set


def test_serialization_is_json_compatible() -> None:
    context = AssertionContext("a:1", SemanticContext("a:1", "inventory:1", EpistemicKind.OBSERVATION))
    assertion = EntityAssertion("a:1", "inventory:1", "quantity_on_hand", 100, context)
    payload = serialize_assertion_set(CanonicalAssertionSet((assertion,)))
    assert payload["entity_assertions"][0]["value"] == 100
    assert is_json_compatible(payload)


def test_json_compatibility_rejects_domain_objects() -> None:
    assert not is_json_compatible(object())
